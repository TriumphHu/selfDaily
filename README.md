# selfDaily

[English](README.md) | [简体中文](README.zh.md)

selfDaily is a local-first daily journal web app built around Markdown writing.
It now supports local Markdown file storage through a small Python server, so
your journal can be shared across browsers without relying on browser cache.

## What Changed Today

- Added `selfdaily-server.py` to serve the app and save notes to local files.
- Added private local storage in `DailyNote/YYYY-MM-DD.md`.
- Added `.gitignore` so `DailyNote/` never goes to GitHub.
- Added startup/open scripts for daily use:
  - `start-selfdaily.ps1`
  - `open-selfdaily.ps1`
  - `install-selfdaily-startup.ps1`
- Added short paths:
  - `http://localhost:5177/`
  - `http://localhost:5177/note`
- Kept browser `localStorage` as a fallback and migration source when the server
  is not running.

## Start Locally

```powershell
python selfdaily-server.py
```

Then open:

```text
http://localhost:5177/
```

These paths also work:

```text
http://localhost:5177/note
http://localhost:5177/daily-journal-ui.html
```

## Daily Use

Install the current-user startup shortcut:

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File .\install-selfdaily-startup.ps1
```

After installation, Windows starts the SelfDaily server after login. To open the
journal manually:

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File .\open-selfdaily.ps1
```

To use `note` from the browser address bar, add a browser site-search shortcut:

```text
Shortcut: note
URL: http://localhost:5177/
```

Some browsers require typing `note`, then pressing `Tab` or space before Enter.

## Data And Privacy

Journal files are saved locally:

```text
DailyNote/YYYY-MM-DD.md
```

`DailyNote/` is ignored by Git. Your private journal files stay on your computer
and are not uploaded to GitHub.

If the server is not running, the app falls back to browser `localStorage`. When
the server runs again, opening the same HTML file in the same browser can merge
cached notes back into `DailyNote/`.

## Current Features

- One journal entry per date
- Local Markdown file storage in `DailyNote/`
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
