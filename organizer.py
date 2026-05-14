#!/usr/bin/env python3
"""
Smart File Organizer
Author: Parth Korgaonkar
GitHub: Drusus03

Sorts files in a target folder into categorized subfolders.
Supports one-time sort and real-time --watch mode.
"""

import os
import sys
import json
import shutil
import logging
import argparse
import time
from datetime import datetime
from pathlib import Path

try:
    from watchdog.observers import Observer
    from watchdog.events import FileSystemEventHandler
    WATCHDOG_AVAILABLE = True
except ImportError:
    WATCHDOG_AVAILABLE = False


# ── Default config (used if config.json is missing) ──────────────────────────

DEFAULT_CONFIG = {
    "categories": {
        "Images":     [".jpg", ".jpeg", ".png", ".gif", ".bmp", ".svg", ".webp", ".ico", ".tiff"],
        "Videos":     [".mp4", ".mkv", ".avi", ".mov", ".wmv", ".flv", ".webm"],
        "Audio":      [".mp3", ".wav", ".flac", ".aac", ".ogg", ".m4a"],
        "Documents":  [".pdf", ".doc", ".docx", ".xls", ".xlsx", ".ppt", ".pptx", ".odt", ".txt", ".rtf"],
        "Code":       [".py", ".js", ".ts", ".html", ".css", ".c", ".cpp", ".h", ".java", ".go", ".rs", ".sh", ".json", ".xml", ".yaml", ".yml", ".md"],
        "Archives":   [".zip", ".tar", ".gz", ".rar", ".7z", ".bz2", ".xz"],
        "Data":       [".csv", ".tsv", ".sql", ".db", ".sqlite"],
        "Executables":[".exe", ".msi", ".apk", ".deb", ".rpm", ".dmg"],
        "Misc":       []
    },
    "ignore": [".DS_Store", "Thumbs.db", "desktop.ini"],
    "misc_folder": "Misc",
    "log_file": "organizer.log"
}


# ── Logging setup ─────────────────────────────────────────────────────────────

def setup_logger(log_path: Path) -> logging.Logger:
    logger = logging.getLogger("FileOrganizer")
    logger.setLevel(logging.DEBUG)
    fmt = logging.Formatter("[%(asctime)s] %(levelname)s — %(message)s", "%Y-%m-%d %H:%M:%S")

    # File handler
    fh = logging.FileHandler(log_path, encoding="utf-8")
    fh.setFormatter(fmt)
    logger.addHandler(fh)

    # Console handler
    ch = logging.StreamHandler(sys.stdout)
    ch.setFormatter(fmt)
    logger.addHandler(ch)

    return logger


# ── Config loader ─────────────────────────────────────────────────────────────

def load_config(config_path: Path) -> dict:
    if config_path.exists():
        with open(config_path, "r", encoding="utf-8") as f:
            user_config = json.load(f)
        # Merge with defaults so missing keys are filled in
        merged = DEFAULT_CONFIG.copy()
        merged.update(user_config)
        return merged
    return DEFAULT_CONFIG.copy()


# ── Core: resolve category for a file ────────────────────────────────────────

def get_category(file_path: Path, config: dict) -> str:
    ext = file_path.suffix.lower()
    for category, extensions in config["categories"].items():
        if ext in extensions:
            return category
    return config.get("misc_folder", "Misc")


# ── Core: move a single file ──────────────────────────────────────────────────

def move_file(file_path: Path, target_root: Path, config: dict, logger: logging.Logger) -> bool:
    """
    Moves file_path into the appropriate subfolder under target_root.
    Returns True if moved, False if skipped.
    """
    filename = file_path.name

    # Skip ignored files
    if filename in config.get("ignore", []):
        logger.debug(f"Skipped (ignored): {filename}")
        return False

    # Skip directories and the log file itself
    if file_path.is_dir():
        return False
    if filename == config.get("log_file", "organizer.log"):
        return False

    category = get_category(file_path, config)
    dest_dir = target_root / category
    dest_dir.mkdir(parents=True, exist_ok=True)

    dest_path = dest_dir / filename

    # Handle name collisions: append _1, _2, ...
    if dest_path.exists():
        stem = file_path.stem
        suffix = file_path.suffix
        counter = 1
        while dest_path.exists():
            dest_path = dest_dir / f"{stem}_{counter}{suffix}"
            counter += 1

    shutil.move(str(file_path), str(dest_path))
    logger.info(f"Moved: {filename}  →  {category}/{dest_path.name}")
    return True


# ── One-time sort ─────────────────────────────────────────────────────────────

def sort_folder(target: Path, config: dict, logger: logging.Logger) -> None:
    files = [f for f in target.iterdir() if f.is_file()]
    if not files:
        logger.info("No files to organize.")
        return

    moved = 0
    skipped = 0
    for f in files:
        result = move_file(f, target, config, logger)
        if result:
            moved += 1
        else:
            skipped += 1

    logger.info(f"Done — {moved} file(s) moved, {skipped} skipped.")


# ── Watch mode ────────────────────────────────────────────────────────────────

class FolderEventHandler(FileSystemEventHandler):
    def __init__(self, target: Path, config: dict, logger: logging.Logger):
        super().__init__()
        self.target = target
        self.config = config
        self.logger = logger

    def on_created(self, event):
        if event.is_directory:
            return
        file_path = Path(event.src_path)
        # Brief wait to ensure file write is complete
        time.sleep(0.5)
        if file_path.exists():
            move_file(file_path, self.target, self.config, self.logger)


def watch_folder(target: Path, config: dict, logger: logging.Logger) -> None:
    if not WATCHDOG_AVAILABLE:
        logger.error("watchdog library not installed. Run: pip install watchdog")
        sys.exit(1)

    handler = FolderEventHandler(target, config, logger)
    observer = Observer()
    observer.schedule(handler, str(target), recursive=False)
    observer.start()
    logger.info(f"Watching '{target}' for new files. Press Ctrl+C to stop.")

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        logger.info("Watch mode stopped by user.")
        observer.stop()
    observer.join()


# ── CLI ───────────────────────────────────────────────────────────────────────

def parse_args():
    parser = argparse.ArgumentParser(
        description="Smart File Organizer — Sort files into categorized subfolders.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python organizer.py ~/Downloads
  python organizer.py ~/Downloads --watch
  python organizer.py ~/Downloads --config my_config.json
        """
    )
    parser.add_argument(
        "folder",
        nargs="?",
        default=".",
        help="Path to the folder to organize (default: current directory)"
    )
    parser.add_argument(
        "--watch", "-w",
        action="store_true",
        help="Watch folder in real-time and auto-sort new files"
    )
    parser.add_argument(
        "--config", "-c",
        default="config.json",
        help="Path to custom config JSON file (default: config.json)"
    )
    parser.add_argument(
        "--generate-config",
        action="store_true",
        help="Generate a default config.json in the current directory and exit"
    )
    return parser.parse_args()


# ── Entry point ───────────────────────────────────────────────────────────────

def main():
    args = parse_args()

    # Generate config and exit
    if args.generate_config:
        out = Path("config.json")
        with open(out, "w", encoding="utf-8") as f:
            json.dump(DEFAULT_CONFIG, f, indent=2)
        print(f"config.json written to {out.resolve()}")
        sys.exit(0)

    # Validate target folder
    target = Path(args.folder).resolve()
    if not target.exists():
        print(f"[ERROR] Folder not found: {target}")
        sys.exit(1)
    if not target.is_dir():
        print(f"[ERROR] Not a directory: {target}")
        sys.exit(1)

    # Load config
    config_path = Path(args.config).resolve()
    config = load_config(config_path)

    # Setup logger inside target folder
    log_path = target / config.get("log_file", "organizer.log")
    logger = setup_logger(log_path)

    logger.info(f"Target folder: {target}")
    logger.info(f"Config: {config_path if config_path.exists() else 'defaults'}")

    if args.watch:
        # Sort existing files first, then watch
        logger.info("Sorting existing files before entering watch mode...")
        sort_folder(target, config, logger)
        watch_folder(target, config, logger)
    else:
        sort_folder(target, config, logger)


if __name__ == "__main__":
    main()
