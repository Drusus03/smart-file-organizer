# 🗂️ Smart File Organizer

**A Python tool that automatically sorts your messy folders into neat categories.**  
Drop it on your Downloads, Desktop, or any folder — it handles the rest.

> By [Parth Korgaonkar](https://github.com/Drusus03)

---

## ✨ Features

- **One-time sort** — instantly organizes all files in a target folder
- **Watch mode** (`--watch`) — monitors folder in real-time, auto-sorts new files as they arrive
- **Collision handling** — renames duplicates automatically (`file_1.jpg`, `file_2.jpg`, ...)
- **Timestamped logs** — every move is logged to `organizer.log` inside the target folder
- **Fully configurable** — customize categories and extensions via `config.json`
- **Cross-platform** — works on Windows, macOS, Linux and Android (Termux)

---

## 📦 Installation Guide

> **Complete beginner?** Follow every step for your device below. Don't skip anything.

---

### 🪟 Windows

#### Step 1 — Install Python

1. Go to [python.org/downloads](https://www.python.org/downloads/)
2. Click the big yellow **Download Python** button
3. Run the installer
4. ⚠️ **IMPORTANT:** On the first screen, check the box that says **"Add Python to PATH"** before clicking Install
5. Click **Install Now** and wait for it to finish

**Verify it worked** — open Command Prompt (press `Win + R`, type `cmd`, hit Enter) and type:
```
python --version
```
You should see something like `Python 3.12.3`. If you see an error, repeat Step 1.

#### Step 2 — Install Git

1. Go to [git-scm.com/download/win](https://git-scm.com/download/win)
2. Download and run the installer
3. Keep clicking **Next** with default settings — no changes needed
4. Click **Install**

**Verify it worked:**
```
git --version
```

#### Step 3 — Download this project

Open Command Prompt and run:
```cmd
git clone https://github.com/Drusus03/smart-file-organizer.git
cd smart-file-organizer
```

#### Step 4 — Install dependencies

```cmd
pip install -r requirements.txt
```

#### Step 5 — Generate config and run

```cmd
python organizer.py --generate-config
python organizer.py C:\Users\YourName\Downloads
```
> Replace `YourName` with your actual Windows username.

---

### 🍎 macOS

#### Step 1 — Install Homebrew (package manager)

Open **Terminal** (press `Cmd + Space`, type `terminal`, hit Enter) and paste:
```bash
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
```
This may take a few minutes. Follow any on-screen instructions.

#### Step 2 — Install Python and Git

```bash
brew install python git
```

**Verify:**
```bash
python3 --version
git --version
```

#### Step 3 — Download this project

```bash
git clone https://github.com/Drusus03/smart-file-organizer.git
cd smart-file-organizer
```

#### Step 4 — Install dependencies

```bash
pip3 install -r requirements.txt
```

#### Step 5 — Generate config and run

```bash
python3 organizer.py --generate-config
python3 organizer.py ~/Downloads
```

---

### 🐧 Linux (Ubuntu/Debian)

#### Step 1 — Install Python and Git

Open Terminal and run:
```bash
sudo apt update
sudo apt install python3 python3-pip git -y
```

#### Step 2 — Download this project

```bash
git clone https://github.com/Drusus03/smart-file-organizer.git
cd smart-file-organizer
```

#### Step 3 — Install dependencies

```bash
pip3 install -r requirements.txt
```

#### Step 4 — Generate config and run

```bash
python3 organizer.py --generate-config
python3 organizer.py ~/Downloads
```

---

### 🤖 Android (Termux)

> iOS is not supported — Apple restricts file system access for third-party apps.

#### Step 1 — Install Termux

**Option A — Via F-Droid** (recommended)
- Download Termux from [F-Droid](https://f-droid.org/packages/com.termux/)
- ⚠️ Do **NOT** use the Play Store version — it's outdated and broken

**Option B — Direct APK from GitHub** (no F-Droid needed)
- Go to [github.com/termux/termux-app/releases](https://github.com/termux/termux-app/releases)
- Tap the **Latest release** (marked with green badge, not Pre-release) → scroll to **Assets** → download `termux-app_v0.118.3+github-debug_universal.apk`
- Open the downloaded APK and tap **Install**
- If prompted, enable **"Install from unknown sources"** in your phone settings

#### ⚠️ Before You Start — Important Termux Tips

Users often face installation failures due to Android battery optimization killing Termux in the background. Follow these to avoid issues:

1. Enable **unrestricted battery / background usage** for Termux in your phone settings
2. Before running long installs or upgrades, run:
   ```bash
   termux-wake-lock
   ```
3. Do **NOT** close or minimize Termux during `apt` or `pip` installs
4. Never run multiple `apt` / `pkg` commands at the same time
5. Use a **stable internet connection** (Wi-Fi preferred)
6. After finishing all installs, release the wake lock:
   ```bash
   termux-wake-unlock
   ```

#### Step 2 — Setup Termux

Open Termux and run these one by one:
```bash
pkg update && pkg upgrade
```
Press `Y` when asked. Then:
```bash
pkg install python git
```
Then give Termux access to your phone storage:
```bash
termux-setup-storage
```
A permission popup will appear — tap **Allow**.

#### Step 3 — Download this project

```bash
git clone https://github.com/Drusus03/smart-file-organizer.git
cd smart-file-organizer
```

#### Step 4 — Install dependencies

```bash
pip install -r requirements.txt
```

#### Step 5 — Generate config and run

```bash
python organizer.py --generate-config
python organizer.py /sdcard/Download
```

---

## 🚀 How to Use

### Sort a folder once
```bash
# Windows
python organizer.py C:\Users\YourName\Downloads

# macOS / Linux
python3 organizer.py ~/Downloads

# Android (Termux)
python organizer.py /sdcard/Download
```

### Watch mode — auto-sort new files in real time
```bash
python organizer.py ~/Downloads --watch
```
New files dropped into the folder get sorted instantly. Stop with `Ctrl + C`.

### Sort your Desktop
```bash
# Windows
python organizer.py C:\Users\YourName\Desktop

# macOS
python3 organizer.py ~/Desktop
```

### Use a custom config file
```bash
python organizer.py ~/Downloads --config my_config.json
```

---

## 🗂️ Default Categories

After running, your messy folder becomes:

```
Downloads/
├── Images/        → .jpg .jpeg .png .gif .svg .webp
├── Videos/        → .mp4 .mkv .avi .mov .wmv
├── Audio/         → .mp3 .wav .flac .aac .ogg
├── Documents/     → .pdf .docx .xlsx .txt .pptx
├── Code/          → .py .js .c .cpp .html .sh
├── Archives/      → .zip .tar .gz .rar .7z
├── Data/          → .csv .sql .db .sqlite
├── Executables/   → .exe .apk .deb .dmg
├── Misc/          → everything else
└── organizer.log  → history of all moves
```

---

## ⚙️ Custom Categories

Want your own folder names? Run:
```bash
python organizer.py --generate-config
```

Then open `config.json` and edit it:
```json
{
  "categories": {
    "Images":    [".jpg", ".png", ".jpeg"],
    "APKs":      [".apk"],
    "Canva":     [".svg", ".ai"],
    "MyProject": [".kicad", ".sch"]
  },
  "ignore": [".DS_Store", "Thumbs.db"],
  "misc_folder": "Misc",
  "log_file": "organizer.log"
}
```

Save the file and run the organizer again — files will now go into your custom folders.

---

## ⚠️ Common Mistakes

**❌ Running it inside the project folder**
```bash
cd ~/smart-file-organizer
python organizer.py        # WRONG — tries to sort its own files!
python organizer.py .      # WRONG — same problem
```
The script detects this automatically and shows an error.

**✅ Always point it at a different target folder**
```bash
python organizer.py ~/Downloads
python organizer.py /sdcard/Download
```

---

## 📋 Sample Output

```
[2026-05-14 10:23:01] INFO — Target folder: /home/parth/Downloads
[2026-05-14 10:23:01] INFO — Moved: resume.pdf      →  Documents/resume.pdf
[2026-05-14 10:23:01] INFO — Moved: wallpaper.png   →  Images/wallpaper.png
[2026-05-14 10:23:01] INFO — Moved: backup.zip      →  Archives/backup.zip
[2026-05-14 10:23:01] INFO — Moved: song.mp3        →  Audio/song.mp3
[2026-05-14 10:23:01] INFO — Moved: app.apk         →  Executables/app.apk
[2026-05-14 10:23:01] INFO — Done — 5 file(s) moved, 0 skipped.
```

---

## 📄 License

MIT License — free to use, modify, and distribute.
