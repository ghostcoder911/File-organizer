import os
import shutil
import argparse
import logging
from pathlib import Path

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')
logger = logging.getLogger(__name__)

# Extension mapping
EXTENSION_MAP = {
    'Documents': ['.pdf', '.docx', '.doc', '.txt', '.md', '.xlsx', '.pptx', '.odt'],
    'Images': ['.jpg', '.jpeg', '.png', '.gif', '.svg', '.webp', '.bmp', '.tiff'],
    'Media': ['.mp4', '.mkv', '.mov', '.avi', '.mp3', '.wav', '.flac'],
    'Archives': ['.zip', '.tar', '.gz', '.7z', '.rar'],
    'Code': ['.py', '.js', '.html', '.css', '.cpp', '.c', '.java', '.go', '.rs', '.ts', '.json', '.yaml', '.yml'],
    'Executables': ['.exe', '.sh', '.bin', '.msi', '.deb', '.rpm'],
    'Data': ['.csv', '.sql', '.db', '.sqlite']
}

def get_category(extension):
    """Returns the category for a given file extension."""
    extension = extension.lower()
    for category, extensions in EXTENSION_MAP.items():
        if extension in extensions:
            return category
    return 'Others'

def organize_directory(directory, dry_run=False):
    """Organizes files in the specified directory into categories."""
    path = Path(directory)
    if not path.is_dir():
        logger.error(f"Error: {directory} is not a valid directory.")
        return

    logger.info(f"Organizing directory: {path.absolute()}")
    if dry_run:
        logger.info("DRY RUN: No files will be moved.")

    files = [f for f in path.iterdir() if f.is_file() and f.name != 'organizer.py']

    if not files:
        logger.info("No files found to organize.")
        return

    for file in files:
        category = get_category(file.suffix)
        category_path = path / category

        if not dry_run:
            category_path.mkdir(exist_ok=True)

        target_path = category_path / file.name

        # Handle filename collisions
        counter = 1
        while target_path.exists():
            name = f"{file.stem}_{counter}{file.suffix}"
            target_path = category_path / name
            counter += 1

        if dry_run:
            logger.info(f"WOULD MOVE: {file.name} -> {category}/{target_path.name}")
        else:
            try:
                shutil.move(str(file), str(target_path))
                logger.info(f"MOVED: {file.name} -> {category}/{target_path.name}")
            except Exception as e:
                logger.error(f"FAILED to move {file.name}: {e}")

    logger.info("Organization complete.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Organize files in a directory by type.")
    parser.add_argument("directory", nargs="?", default=".", help="The directory to organize (default: current directory)")
    parser.add_argument("--dry-run", action="store_true", help="Preview changes without moving files")
    
    args = parser.parse_args()
    
    organize_directory(args.directory, dry_run=args.dry_run)
