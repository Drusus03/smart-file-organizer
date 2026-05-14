# 🗂️ Smart File Organizer

**A Python CLI tool that automatically sorts files into categorized subfolders.**  
Supports one-time sorting and real-time watch mode. Fully configurable via JSON.

> By [Parth Korgaonkar](https://github.com/Drusus03)

---

## ✨ Features

- **One-time sort** — instantly organizes all files in a target folder
- **Watch mode** (`--watch`) — monitors folder in real-time, auto-sorts new files as they arrive
- **Collision handling** — renames duplicates automatically (`file_1.jpg`, `file_2.jpg`, ...)
- **Timestamped logs** — every move is logged to `organizer.log` inside the target folder
- **Fully configurable** — customize categories and extensions via `config.json`
- **Cross-platform** — works on Windows, macOS, Linux, and Android (Termux)

---

## 📦 Installation

### Prerequisites
- Python 3.8 or higher
- pip (Python package manager)

---

### 🪟 Windows

1. **Install Python**  
   Download from [python.org](https://www.python.org/downloads/)  
   ✅ During install, check **"Add Python to PATH"**

2. **Verify installation**
   ```cmd
   python --version
   pip --version
   ```

3. **Download the project**  
   Click **Code → Download ZIP** on this page, then extract it.  
   Or clone via Git:
   ```cmd
   git clone https://github.com/Drusus03/smart-file-organizer.git
   cd smart-file-organizer
   ```

4. **Install dependencies**
   ```cmd
   pip install -r requirements.txt
   ```

---

### 🍎 macOS

1. **Install Python** (macOS may have Python 2 by default)
   ```bash
   brew install python
   ```
   > Don't have Homebrew? Install it from [brew.sh](https://brew.sh)

2. **Clone the project**
   ```bash
   git clone https://github.com/Drusus03/smart-file-organizer.git
   cd smart-file-organizer
   ```

3. **Install dependencies**
   ```bash
   pip3 install -r requirements.txt
   ```

---

### 🐧 Linux

1. **Install Python and pip**
   ```bash
   sudo apt update
   sudo apt install python3 python3-pip   # Debian/Ubuntu
   ```

2. **Clone the project**
   ```bash
   git clone https://github.com/Drusus03/smart-file-organizer.git
   cd smart-file-organizer
   ```

3. **Install dependencies**
   ```bash
   pip3 install -r requirements.txt
   ```

---

### 🤖 Android (Termux)

1. **Install Termux** from [F-Droid](https://f-droid.org/packages/com.termux/)  
   *(Avoid Play Store version — it's outdated)*

2. **Setup Termux**
   ```bash
   pkg update && pkg upgrade
   pkg install python git
   termux-setup-storage
   ```

3. **Clone the project**
   ```bash
   git clone https://github.com/Drusus03/smart-file-organizer.git
   cd smart-file-organizer
   ```

4. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

> **Note:** iOS is not supported. Python cannot run natively on iOS without jailbreak or special apps, and file system access is heavily restricted.

---

## 🚀 Usage

### Step 1 — Generate your config (first time only)
```bash
python organizer.py --generate-config
```
This creates a `config.json` in the current directory with all default settings.

---

### Step 2 — One-time sort

Sort a specific folder:
```bash
python organizer.py /path/to/your/folder
```

**Examples:**

| Platform | Command |
|----------|---------|
| Windows | `python organizer.py C:\Users\YourName\Downloads` |
| macOS/Linux | `python organizer.py ~/Downloads` |
| Android (Termux) | `python organizer.py /sdcard/Download` |

Sort the **current directory:**
```bash
python organizer.py .
```

---

### Step 3 — Watch mode (real-time auto-sort)

```bash
python organizer.py ~/Downloads --watch
```

- Sorts existing files first, then monitors for new ones
- Any file dropped into the folder gets sorted instantly
- Stop with `Ctrl + C`

---

### Step 4 — Use a custom config

```bash
python organizer.py ~/Downloads --config my_config.json
```

---

## ⚙️ Customizing Categories

Edit `config.json` to define your own folders and file types:

```json
{
  "categories": {
    "Images":     [".jpg", ".jpeg", ".png", ".gif", ".webp"],
    "Videos":     [".mp4", ".mkv", ".avi"],
    "Audio":      [".mp3", ".wav", ".flac"],
    "Documents":  [".pdf", ".docx", ".txt"],
    "Code":       [".py", ".js", ".c", ".cpp", ".html"],
    "Archives":   [".zip", ".tar", ".gz", ".rar"],
    "Data":       [".csv", ".sql", ".db"],
    "MyFolder":   [".kicad", ".sch", ".gerber"]
  },
  "ignore": [".DS_Store", "Thumbs.db", "desktop.ini"],
  "misc_folder": "Misc",
  "log_file": "organizer.log"
}
```

- Add a new key under `"categories"` for a custom folder
- Files with unknown extensions go to `Misc` automatically

---

## 🗂️ Default Folder Structure

After running, your messy folder becomes:

```
Downloads/
├── Images/
│   ├── photo1.jpg
│   └── wallpaper.png
├── Videos/
│   └── tutorial.mp4
├── Documents/
│   ├── resume.pdf
│   └── notes.txt
├── Code/
│   ├── script.py
│   └── index.html
├── Archives/
│   └── backup.zip
├── Misc/
│   └── unknownfile.xyz
└── organizer.log
```

---

## 📋 Sample Output

```
[2026-05-14 10:23:01] INFO — Target folder: /home/parth/Downloads
[2026-05-14 10:23:01] INFO — Moved: resume.pdf        →  Documents/resume.pdf
[2026-05-14 10:23:01] INFO — Moved: wallpaper.png     →  Images/wallpaper.png
[2026-05-14 10:23:01] INFO — Moved: backup.zip        →  Archives/backup.zip
[2026-05-14 10:23:01] INFO — Moved: tutorial.mp4      →  Videos/tutorial.mp4
[2026-05-14 10:23:01] INFO — Done — 4 file(s) moved, 0 skipped.
```

---

## ⚡ Quick Reference

```
python organizer.py <folder>                  → Sort folder once
python organizer.py <folder> --watch          → Real-time watch mode
python organizer.py --generate-config         → Create config.json
python organizer.py <folder> --config <file>  → Use custom config
```

---

## 📄 License

MIT License — free to use, modify, and distribute.
