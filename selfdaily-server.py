from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import unquote, urlparse
import json
import re
import sys


BASE_DIR = Path(__file__).resolve().parent
NOTE_DIR = BASE_DIR / "DailyNote"
DATE_RE = re.compile(r"^\d{4}-\d{2}-\d{2}$")


def json_response(handler, status, payload):
    body = json.dumps(payload, ensure_ascii=False).encode("utf-8")
    handler.send_response(status)
    handler.send_header("Content-Type", "application/json; charset=utf-8")
    handler.send_header("Content-Length", str(len(body)))
    handler.send_header("Cache-Control", "no-store")
    handler.send_header("Access-Control-Allow-Origin", "*")
    handler.send_header("Access-Control-Allow-Methods", "GET, PUT, OPTIONS")
    handler.send_header("Access-Control-Allow-Headers", "Content-Type")
    handler.end_headers()
    handler.wfile.write(body)


def read_request_json(handler):
    length = int(handler.headers.get("Content-Length", "0"))
    raw = handler.rfile.read(length).decode("utf-8")
    return json.loads(raw or "null")


def normalize_entry(entry):
    date = str(entry.get("date", "")).strip()
    if not DATE_RE.match(date):
      raise ValueError(f"Invalid date: {date}")
    tags = entry.get("tags", [])
    if isinstance(tags, str):
        tags = [tag.strip() for tag in re.split(r"[,，]", tags) if tag.strip()]
    if not isinstance(tags, list):
        tags = []
    return {
        "date": date,
        "title": str(entry.get("title") or f"{date} 日记"),
        "mood": str(entry.get("mood") or "平静"),
        "energy": str(entry.get("energy") or "中等"),
        "tags": [str(tag) for tag in tags],
        "content": str(entry.get("content") or ""),
        "createdAt": str(entry.get("createdAt") or ""),
        "updatedAt": str(entry.get("updatedAt") or ""),
    }


def note_path(date):
    if not DATE_RE.match(date):
        raise ValueError(f"Invalid date: {date}")
    return NOTE_DIR / f"{date}.md"


def encode_frontmatter(entry):
    fields = ["date", "title", "mood", "energy", "tags", "createdAt", "updatedAt"]
    lines = ["---"]
    for field in fields:
        lines.append(f"{field}: {json.dumps(entry[field], ensure_ascii=False)}")
    lines.append("---")
    lines.append("")
    lines.append(entry["content"])
    return "\n".join(lines)


def decode_frontmatter(path):
    text = path.read_text(encoding="utf-8")
    fallback = {
        "date": path.stem,
        "title": f"{path.stem} 日记",
        "mood": "平静",
        "energy": "中等",
        "tags": [],
        "content": text,
        "createdAt": "",
        "updatedAt": "",
    }
    if not text.startswith("---\n"):
        title_match = re.search(r"^#\s+(.+)$", text, re.MULTILINE)
        if title_match:
            fallback["title"] = title_match.group(1).strip()
        return normalize_entry(fallback)

    end = text.find("\n---\n", 4)
    if end == -1:
        return normalize_entry(fallback)

    meta_text = text[4:end]
    content = text[end + 5:].lstrip("\n")
    meta = {}
    for line in meta_text.splitlines():
        if ":" not in line:
            continue
        key, value = line.split(":", 1)
        key = key.strip()
        value = value.strip()
        try:
            meta[key] = json.loads(value)
        except json.JSONDecodeError:
            meta[key] = value.strip('"')
    meta["date"] = meta.get("date") or path.stem
    meta["content"] = content
    return normalize_entry(meta)


def read_entries():
    NOTE_DIR.mkdir(exist_ok=True)
    entries = []
    for path in sorted(NOTE_DIR.glob("*.md")):
        if DATE_RE.match(path.stem):
            entries.append(decode_frontmatter(path))
    return sorted(entries, key=lambda entry: entry["date"], reverse=True)


def write_entries(entries):
    NOTE_DIR.mkdir(exist_ok=True)
    normalized = [normalize_entry(entry) for entry in entries if isinstance(entry, dict)]
    seen_dates = {entry["date"] for entry in normalized}
    for path in NOTE_DIR.glob("*.md"):
        if DATE_RE.match(path.stem) and path.stem not in seen_dates:
            path.unlink()
    for entry in normalized:
        note_path(entry["date"]).write_text(encode_frontmatter(entry), encoding="utf-8")
    return sorted(normalized, key=lambda entry: entry["date"], reverse=True)


class SelfDailyHandler(SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=str(BASE_DIR), **kwargs)

    def redirect_to_app(self):
        self.send_response(302)
        self.send_header("Location", "/daily-journal-ui.html")
        self.end_headers()

    def do_GET(self):
        path = unquote(urlparse(self.path).path)
        if path == "/api/entries":
            json_response(self, 200, {"entries": read_entries()})
            return
        if path in ("", "/", "/note"):
            self.redirect_to_app()
            return
        super().do_GET()

    def do_HEAD(self):
        path = unquote(urlparse(self.path).path)
        if path in ("", "/", "/note"):
            self.redirect_to_app()
            return
        super().do_HEAD()

    def do_PUT(self):
        path = unquote(urlparse(self.path).path)
        if path != "/api/entries":
            json_response(self, 404, {"error": "Not found"})
            return
        try:
            payload = read_request_json(self)
            entries = payload.get("entries", []) if isinstance(payload, dict) else []
            json_response(self, 200, {"entries": write_entries(entries)})
        except Exception as exc:
            json_response(self, 400, {"error": str(exc)})

    def do_OPTIONS(self):
        self.send_response(204)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, PUT, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.end_headers()

    def log_message(self, format, *args):
        sys.stdout.write("%s - %s\n" % (self.address_string(), format % args))


def main():
    NOTE_DIR.mkdir(exist_ok=True)
    port = int(sys.argv[1]) if len(sys.argv) > 1 else 5177
    server = ThreadingHTTPServer(("127.0.0.1", port), SelfDailyHandler)
    print(f"SelfDaily running at http://127.0.0.1:{port}/daily-journal-ui.html")
    print(f"Daily notes folder: {NOTE_DIR}")
    server.serve_forever()


if __name__ == "__main__":
    main()
