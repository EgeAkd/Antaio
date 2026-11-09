"""Preview-first file organization. Standard library only."""
import argparse
import json
import os
from pathlib import Path

GROUPS = {
    'Images': {'.jpg', '.jpeg', '.png', '.gif', '.webp', '.svg', '.heic'},
    'Documents': {'.pdf', '.txt', '.docx', '.xlsx', '.csv', '.md', '.pptx'},
    'Archives': {'.zip', '.tar', '.gz', '.7z', '.rar'},
    'Audio': {'.mp3', '.wav', '.flac', '.m4a'},
    'Video': {'.mp4', '.mov', '.mkv', '.webm'},
}


def plan(root):
    """Only consider visible regular files directly inside root."""
    root = Path(root).resolve(strict=True)
    if not root.is_dir():
        raise ValueError('Source must be a directory')
    result = []
    for source in sorted(root.iterdir()):
        if source.name.startswith('.') or source.is_symlink() or not source.is_file():
            continue
        group = next((g for g, exts in GROUPS.items() if source.suffix.lower() in exts), 'Other')
        folder = root / group
        if folder.is_symlink() or (folder.exists() and not folder.is_dir()):
            raise ValueError(f'Unsafe destination: {folder}')
        target = folder / source.name
        number = 1
        while target.exists() or target.is_symlink():
            target = folder / f'{source.stem} ({number}){source.suffix}'
            number += 1
        result.append((source, target))
    return result


def apply(moves):
    """Use exclusive creation so an existing destination is never overwritten."""
    completed = []
    for source, target in moves:
        if source.is_symlink() or not source.is_file():
            raise ValueError(f'Source changed: {source}')
        if target.parent.is_symlink():
            raise ValueError(f'Unsafe destination: {target.parent}')
        target.parent.mkdir(exist_ok=True)
        # Hard links provide atomic no-clobber behavior on the same filesystem.
        os.link(source, target, follow_symlinks=False)
        source.unlink()
        completed.append({'source': str(source), 'destination': str(target)})
    return completed


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('directory', type=Path)
    parser.add_argument('--apply', action='store_true', help='Move files; default is preview only')
    args = parser.parse_args()
    try:
        moves = plan(args.directory)
        if args.apply:
            print(json.dumps(apply(moves), indent=2, ensure_ascii=False))
        else:
            for source, target in moves:
                print(f'{source.name} -> {target.relative_to(source.parent)}')
            print(f'{len(moves)} file(s). Preview only. Add --apply to organize.')
    except (OSError, ValueError) as error:
        parser.exit(1, f'Error: {error}\n')


if __name__ == '__main__':
    main()
