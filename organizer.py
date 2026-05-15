#!/usr/bin/env python3
"""
Smart File Organizer
Author: Parth Korgaonkar
GitHub: Drusus03

Sorts files in a target folder into categorized subfolders.
Supports one-time sort, real-time --watch mode, --undo, --duplicates, and --stats.
"""

import os
import sys
import json
import shutil
import hashlib
import logging
import argparse
import time
from pathlib import Path

try:
    from watchdog.observers import Observer
    from watchdog.events import FileSystemEventHandler
    WATCHDOG_AVAILABLE = True
except ImportError:
    WATCHDOG_AVAILABLE = False
    class FileSystemEventHandler:
        pass
    Observer = None


# ── Default config ────────────────────────────────────────────────────────────

DEFAULT_CONFIG = {
    "categories": {
        "Images":      [".jpg", ".jpeg", ".png", ".gif", ".bmp", ".svg", ".webp", ".ico", ".tiff"],
        "Videos":      [".mp4", ".mkv", ".avi", ".mov", ".wmv", ".flv", ".webm"],
        "Audio":       [".mp3", ".wav", ".flac", ".aac", ".ogg", ".m4a"],
        "Documents":   [".pdf", ".doc", ".docx", ".xls", ".xlsx", ".ppt", ".pptx", ".odt", ".txt", ".rtf"],
        "Code":        [".py", ".js", ".ts", ".html", ".css", ".c", ".cpp", ".h", ".java", ".go", ".rs", ".sh", ".json", ".xml", ".yaml", ".yml", ".md"],
        "Archives":    [".zip", ".tar", ".gz", ".rar", ".7z", ".bz2", ".xz"],
        "Data":        [".csv", ".tsv", ".sql", ".db", ".sqlite"],
        "Executables": [".exe", ".msi", ".apk", ".deb", ".rpm", ".dmg"],
        "Misc":        []
    },
    "ignore": [".DS_Store", "Thumbs.db", "desktop.ini"],
    "misc_folder": "Misc",
    "log_file": "organizer.log"
}

SESSION_MARKER = "=== SESSION START ==="


# ── Logging setup ─────────────────────────────────────────────────────────────

def setup_logger(log_path: Path) -> logging.Logger:
    logger = logging.getLogger("FileOrganizer")
    if logger.handlers:
        logger.handlers.clear()
    logger.setLevel(logging.DEBUG)
    fmt = logging.Formatter("[%(asctime)s] %(levelname)s — %(message)s", "%Y-%m-%d %H:%M:%S")
    fh = logging.FileHandler(log_path, encoding="utf-8")
    fh.setFormatter(fmt)
    logger.addHandler(fh)
    ch = logging.StreamHandler(sys.stdout)
    ch.setFormatter(fmt)
    logger.addHandler(ch)
    return logger


def write_session_marker(log_path: Path) -> None:
    with open(log_path, "a", encoding="utf-8") as f:
        f.write(f"\n{SESSION_MARKER}\n")


# ── Config loader ─────────────────────────────────────────────────────────────

def load_config(config_path: Path) -> dict:
    if config_path.exists():
        with open(config_path, "r", encoding="utf-8") as f:
            user_config = json.load(f)
        merged = DEFAULT_CONFIG.copy()
        merged.update(user_config)
        return merged
    return DEFAULT_CONFIG.copy()


# ── Core: resolve category ────────────────────────────────────────────────────

def get_category(file_path: Path, config: dict) -> str:
    ext = file_path.suffix.lower()
    for category, extensions in config["categories"].items():
        if ext in extensions:
            return category
    return config.get("misc_folder", "Misc")


# ── Core: move a single file ──────────────────────────────────────────────────

def move_file(file_path: Path, target_root: Path, config: dict, logger: logging.Logger) -> bool:
    filename = file_path.name
    if filename in config.get("ignore", []):
        logger.debug(f"Skipped (ignored): {filename}")
        return False
    if file_path.is_dir():
        return False
    if filename == config.get("log_file", "organizer.log"):
        return False

    category = get_category(file_path, config)
    dest_dir = target_root / category
    dest_dir.mkdir(parents=True, exist_ok=True)
    dest_path = dest_dir / filename

    if dest_path.exists():
        stem = file_path.stem
        suffix = file_path.suffix
        counter = 1
        while dest_path.exists():
            dest_path = dest_dir / f"{stem}_{counter}{suffix}"
            counter += 1

    shutil.move(str(file_path), str(dest_path))
    logger.info(f"Moved: {filename}  ->  {category}/{dest_path.name}")
    return True


# ── One-time sort ─────────────────────────────────────────────────────────────

def sort_folder(target: Path, config: dict, logger: logging.Logger) -> dict:
    files = [f for f in target.iterdir() if f.is_file()]
    if not files:
        logger.info("No files to organize.")
        return {}

    moved = 0
    skipped = 0
    stats = {}

    for f in files:
        cat = get_category(f, config)
        result = move_file(f, target, config, logger)
        if result:
            moved += 1
            stats[cat] = stats.get(cat, 0) + 1
        else:
            skipped += 1

    logger.info(f"Done — {moved} file(s) moved, {skipped} skipped.")
    return stats


# ── Stats mode ────────────────────────────────────────────────────────────────

def show_stats(target: Path) -> None:
    print(f"\nStats for: {target}\n")
    total = 0
    rows = []

    for item in sorted(target.iterdir()):
        if item.is_dir():
            count = len([f for f in item.iterdir() if f.is_file()])
            if count > 0:
                rows.append((item.name, count))
                total += count

    if not rows:
        print("  No organized subfolders found.")
        return

    max_name = max(len(r[0]) for r in rows)
    max_count = max(r[1] for r in rows)

    for name, count in rows:
        bar_len = int((count / max_count) * 30)
        bar = "#" * bar_len
        print(f"  {name:<{max_name}}  {bar:<30}  {count} file(s)")

    print(f"\n  Total: {total} file(s) across {len(rows)} categories\n")


# ── Undo last session ─────────────────────────────────────────────────────────

def undo_last_session(target: Path, config: dict) -> None:
    log_path = target / config.get("log_file", "organizer.log")

    if not log_path.exists():
        print("[ERROR] No log file found. Nothing to undo.")
        sys.exit(1)

    lines = log_path.read_text(encoding="utf-8").splitlines()

    last_marker_idx = -1
    for i, line in enumerate(lines):
        if SESSION_MARKER in line:
            last_marker_idx = i

    if last_marker_idx == -1:
        print("[ERROR] No session found in log. Run the organizer at least once first.")
        sys.exit(1)

    session_lines = lines[last_marker_idx + 1:]

    moves = []
    for line in session_lines:
        if "INFO" in line and "Moved:" in line and "->" in line:
            try:
                part = line.split("Moved:")[1].strip()
                original_name, dest_rel = [x.strip() for x in part.split("->")]
                moves.append((original_name.strip(), dest_rel.strip()))
            except Exception:
                continue

    if not moves:
        print("Nothing to undo in the last session.")
        return

    print(f"\nUndoing {len(moves)} move(s)...\n")
    restored = 0
    failed = 0

    for original_name, dest_rel in reversed(moves):
        src = target / dest_rel
        dst = target / original_name

        if not src.exists():
            print(f"  [SKIP] Not found: {dest_rel}")
            failed += 1
            continue

        if dst.exists():
            stem = Path(original_name).stem
            suffix = Path(original_name).suffix
            counter = 1
            while dst.exists():
                dst = target / f"{stem}_restored_{counter}{suffix}"
                counter += 1

        shutil.move(str(src), str(dst))
        print(f"  Restored: {dest_rel}  ->  {dst.name}")
        restored += 1

    # Clean up empty category folders
    for item in target.iterdir():
        if item.is_dir():
            try:
                item.rmdir()
            except OSError:
                pass

    # Trim log — remove last session
    new_lines = lines[:last_marker_idx]
    log_path.write_text("\n".join(new_lines) + "\n", encoding="utf-8")

    print(f"\nDone — {restored} restored, {failed} skipped.\n")


# ── Duplicate detector ────────────────────────────────────────────────────────

def hash_file(path: Path, chunk_size: int = 65536) -> str:
    h = hashlib.md5()
    with open(path, "rb") as f:
        while True:
            chunk = f.read(chunk_size)
            if not chunk:
                break
            h.update(chunk)
    return h.hexdigest()


def find_duplicates(target: Path) -> None:
    print(f"\nScanning for duplicates in: {target}\n")

    hash_map = {}
    scanned = 0

    for file in target.rglob("*"):
        if file.is_file() and file.name != "organizer.log":
            try:
                h = hash_file(file)
                hash_map.setdefault(h, []).append(file)
                scanned += 1
            except (PermissionError, OSError):
                continue

    duplicates = {h: paths for h, paths in hash_map.items() if len(paths) > 1}

    if not duplicates:
        print(f"  No duplicates found. ({scanned} files scanned)\n")
        return

    total_dupes = sum(len(p) - 1 for p in duplicates.values())
    print(f"  Found {len(duplicates)} duplicate group(s), {total_dupes} redundant file(s):\n")

    for i, (h, paths) in enumerate(duplicates.items(), 1):
        print(f"  Group {i} (MD5: {h[:12]}...):")
        for j, p in enumerate(paths):
            label = "KEEP" if j == 0 else "DUPE"
            rel = p.relative_to(target)
            size_kb = p.stat().st_size / 1024
            print(f"    [{label}] {rel}  ({size_kb:.1f} KB)")
        print()

    print(f"  Tip: Delete the [DUPE] files manually to free up space.\n")


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
        time.sleep(0.5)
        if file_path.exists():
            move_file(file_path, self.target, self.config, self.logger)


def watch_folder(target: Path, config: dict, logger: logging.Logger) -> None:
    if not WATCHDOG_AVAILABLE:
        logger.error("watchdog not installed. Run: pip install watchdog")
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
        description="Smart File Organizer — Sort, undo, find duplicates, and view stats.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python organizer.py ~/Downloads
  python organizer.py ~/Downloads --watch
  python organizer.py ~/Downloads --undo
  python organizer.py ~/Downloads --stats
  python organizer.py ~/Downloads --duplicates
  python organizer.py --generate-config
        """
    )
    parser.add_argument("folder", nargs="?", default=".",
                        help="Target folder (default: current directory)")
    parser.add_argument("--watch", "-w", action="store_true",
                        help="Watch and auto-sort new files in real-time")
    parser.add_argument("--undo", action="store_true",
                        help="Reverse the last sort session")
    parser.add_argument("--stats", action="store_true",
                        help="Show file count per category")
    parser.add_argument("--duplicates", action="store_true",
                        help="Find files with identical content")
    parser.add_argument("--config", "-c", default="config.json",
                        help="Path to config JSON (default: config.json)")
    parser.add_argument("--generate-config", action="store_true",
                        help="Generate default config.json and exit")
    return parser.parse_args()


# ── Entry point ───────────────────────────────────────────────────────────────

def main():
    args = parse_args()

    if args.generate_config:
        out = Path("config.json")
        with open(out, "w", encoding="utf-8") as f:
            json.dump(DEFAULT_CONFIG, f, indent=2)
        print(f"config.json written to {out.resolve()}")
        sys.exit(0)

    target = Path(args.folder).resolve()
    if not target.exists():
        print(f"[ERROR] Folder not found: {target}")
        sys.exit(1)
    if not target.is_dir():
        print(f"[ERROR] Not a directory: {target}")
        sys.exit(1)

    script_dir = Path(__file__).resolve().parent
    if target == script_dir:
        print("[ERROR] You are trying to organize the folder that contains organizer.py itself.")
        print("        Run it on a different folder, e.g: python organizer.py ~/Downloads")
        sys.exit(1)

    config_path = Path(args.config).resolve()
    config = load_config(config_path)

    if args.stats:
        show_stats(target)
        return

    if args.duplicates:
        find_duplicates(target)
        return

    if args.undo:
        undo_last_session(target, config)
        return

    log_path = target / config.get("log_file", "organizer.log")
    write_session_marker(log_path)
    logger = setup_logger(log_path)

    logger.info(f"Target folder: {target}")
    logger.info(f"Config: {config_path if config_path.exists() else 'defaults'}")

    if args.watch:
        logger.info("Sorting existing files before entering watch mode...")
        sort_folder(target, config, logger)
        watch_folder(target, config, logger)
    else:
        stats = sort_folder(target, config, logger)
        if stats:
            logger.info("Stats: " + ", ".join(f"{k}: {v}" for k, v in sorted(stats.items())))


if __name__ == "__main__":
    main()
