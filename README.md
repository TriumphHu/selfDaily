# selfDaily

selfDaily is a local-first daily journal web app built around Markdown writing.

It currently runs as a single-page frontend app. Entries are saved in the
browser with `localStorage`, so you can write, preview, search, export, import,
and back up your daily notes without a backend service.

## Preview Locally

```powershell
python -m http.server 5177 --bind 127.0.0.1
```

Then open:

```text
http://localhost:5177/daily-journal-ui.html
```

## Current Features

- One journal entry per date
- Markdown editor with live preview
- Calendar and entry list
- Title, mood, energy, and tags
- Search by date, title, tags, or content
- Daily and review templates
- Export current entry as Markdown
- Backup and import journal data
- Light and dark themes

## Origin

This project started from `woyin2024/lengyi-markdown-editor` and is being
adapted into a personal daily journal project.
