🗂️ Smart File Organizer
A Python CLI tool that automatically sorts files into categorized subfolders.
Supports one-time sorting and real-time watch mode. Fully configurable via JSON.
By Parth Korgaonkar
✨ Features
One-time sort — instantly organizes all files in a target folder
Watch mode (--watch) — monitors folder in real-time, auto-sorts new files as they arrive
Collision handling — renames duplicates automatically (file_1.jpg, file_2.jpg, ...)
Timestamped logs — every move is logged to organizer.log inside the target folder
Fully configurable — customize categories and extensions via config.json
Cross-platform — works on Windows, macOS, Linux, and Android (Termux)
📦 Installation
Prerequisites
Python 3.8 or higher
pip (Python package manager)
🪟 Windows
Install Python
Download from python.org
✅ During install, check "Add Python to PATH"
Verify installation
Cmd
Download the project
Click Code → Download ZIP on this page, then extract it.
Or clone via Git:
Cmd
Install dependencies
Cmd
🍎 macOS
Install Python (macOS may have Python 2 by default)
Bash
Don't have Homebrew? Install it from brew.sh
Clone the project
Bash
Install dependencies
Bash
🐧 Linux
Install Python and pip
Bash
Clone the project
Bash
Install dependencies
Bash
🤖 Android (Termux)
Install Termux from F-Droid
(Avoid Play Store version — it's outdated)
Setup Termux
Bash
Clone the project
Bash
Install dependencies
Bash
Note: iOS is not supported. Python cannot run natively on iOS without jailbreak or special apps, and file system access is heavily restricted.
🚀 Usage
Step 1 — Generate your config (first time only)
Bash
This creates a config.json in the current directory with all default settings.
Step 2 — One-time sort
Sort a specific folder:
Bash
Examples:
Platform
Command
Windows
python organizer.py C:\Users\YourName\Downloads
macOS/Linux
python organizer.py ~/Downloads
Android (Termux)
python organizer.py /sdcard/Download
Sort the current directory:
Bash
Step 3 — Watch mode (real-time auto-sort)
Bash
Sorts existing files first, then monitors for new ones
Any file dropped into the folder gets sorted instantly
Stop with Ctrl + C
Step 4 — Use a custom config
Bash
⚙️ Customizing Categories
Edit config.json to define your own folders and file types:
Json
Add a new key under "categories" for a custom folder
Files with unknown extensions go to Misc automatically
🗂️ Default Folder Structure
After running, your messy folder becomes:
Code
📋 Sample Output
Code
⚡ Quick Reference
Code
📄 License
MIT License — free to use, modify, and distribute.
