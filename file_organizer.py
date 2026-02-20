import os
import shutil
from pathlib import Path
from typing import Dict


FILE_CATEGORIES: Dict[str, list] = {
    "Images": [".jpg", ".jpeg", ".png", ".gif", ".bmp", ".svg", ".webp"],
    "Documents": [".pdf", ".doc", ".docx", ".txt", ".xlsx", ".pptx", ".csv"],
    "Videos": [".mp4", ".avi", ".mkv", ".mov", ".wmv"],
    "Audio": [".mp3", ".wav", ".flac", ".aac", ".ogg"],
    "Archives": [".zip", ".rar", ".7z", ".tar", ".gz"],
    "Code": [".py", ".js", ".ts", ".html", ".css", ".json", ".yaml"],
}


def organize_files(target_path: str, dry_run: bool = False) -> dict:
    target = Path(target_path)
    if not target.exists():
        raise FileNotFoundError(f"Path not found: {target_path}")

    moved = {}
    for file in target.iterdir():
        if file.is_file():
            ext = file.suffix.lower()
            category = "Other"
            for cat, extensions in FILE_CATEGORIES.items():
                if ext in extensions:
                    category = cat
                    break

            dest_dir = target / category
            if not dry_run:
                dest_dir.mkdir(exist_ok=True)
                shutil.move(str(file), str(dest_dir / file.name))

            moved[file.name] = category

    return moved


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Organize files by type")
    parser.add_argument("--path", required=True, help="Target directory")
    parser.add_argument("--dry-run", action="store_true", help="Preview only")
    args = parser.parse_args()

    results = organize_files(args.path, args.dry_run)
    for fname, cat in results.items():
        print(f"  {fname} -> {cat}/")
    print(f"\nTotal: {len(results)} files organized")
