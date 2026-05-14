# 🗂️ Smart File Organizer

**A Python CLI tool that automatically sorts files in any folder into categorized subfolders.**  
Supports one-time sorting and real-time watch mode. Fully configurable via JSON.

> By [Parth Korgaonkar](https://github.com/Drusus03)

---

## ✨ Features

- **One-time sort** — instantly organizes all files in a target folder
- **Watch mode** (`--watch`) — monitors folder in real-time, auto-sorts new files as they arrive
- **Collision handling** — renames duplicates automatically (`file_1.jpg`, `file_2.jpg`, ...)
- **Timestamped logs** — every move is logged to `organizer.log` inside the target folder
- **Fully configurable** — customize categories and extensions via `config.json`
- **Cross-platform** — works on Windows, macOS, Linux

---

## 📁 Project Structure

```
file_organizer/
├── organizer.py      # Main script
├── config.json       # Extension → category mappings (auto-generated)
└── README.md
```

---

## 🚀 Usage

### Basic sort
```bash
python organizer.py ~/Downloads
```

### Watch mode (real-time)
```bash
python organizer.py ~/Downloads --watch
```

### Use a custom config
```bash
python organizer.py ~/Downloads --config my_config.json
```

### Generate a default config.json
```bash
python organizer.py --generate-config
```

---

## 🗂️ Default Categories

| Folder       | Extensions                                      |
|--------------|-------------------------------------------------|
| Images       | `.jpg` `.jpeg` `.png` `.gif` `.svg` `.webp` ... |
| Videos       | `.mp4` `.mkv` `.avi` `.mov` ...                 |
| Audio        | `.mp3` `.wav` `.flac` `.aac` ...                |
| Documents    | `.pdf` `.docx` `.xlsx` `.txt` `.pptx` ...       |
| Code         | `.py` `.js` `.c` `.cpp` `.html` `.sh` ...       |
| Archives     | `.zip` `.tar` `.gz` `.rar` `.7z` ...            |
| Data         | `.csv` `.tsv` `.sql` `.db` ...                  |
| Executables  | `.exe` `.apk` `.deb` `.dmg` ...                 |
| Misc         | Everything else                                 |

---

## ⚙️ Configuration

Run `--generate-config` to create a `config.json`, then customize it:

```json
{
  "categories": {
    "Images": [".jpg", ".png"],
    "MyCustomFolder": [".kicad", ".sch"]
  },
  "ignore": [".DS_Store", "Thumbs.db"],
  "misc_folder": "Misc",
  "log_file": "organizer.log"
}
```

---

## 📦 Requirements

```bash
pip install watchdog
```

> `watchdog` is only required for `--watch` mode. One-time sort works with stdlib only.

---

## 📋 Sample Output

```
[2026-05-14 10:23:01] INFO — Target folder: /home/parth/Downloads
[2026-05-14 10:23:01] INFO — Moved: report.pdf        →  Documents/report.pdf
[2026-05-14 10:23:01] INFO — Moved: wallpaper.png     →  Images/wallpaper.png
[2026-05-14 10:23:01] INFO — Moved: backup.zip        →  Archives/backup.zip
[2026-05-14 10:23:01] INFO — Moved: notes.txt         →  Documents/notes.txt
[2026-05-14 10:23:01] INFO — Done — 4 file(s) moved, 0 skipped.
```
