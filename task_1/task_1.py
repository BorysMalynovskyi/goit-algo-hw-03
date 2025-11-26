import argparse
import shutil
from pathlib import Path


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Recursively copy files from source into destination grouped by extension.",
    )
    parser.add_argument("source", help="Path to source directory.")
    parser.add_argument(
        "destination",
        nargs="?",
        default="dist",
        help="Path to destination directory (default: dist).",
    )
    return parser.parse_args()


class FileSorter:
    def __init__(self, source: Path, destination: Path):
        self.source = source
        self.destination = destination
        self._validate_paths()

    def run(self):
        self.destination.mkdir(parents=True, exist_ok=True)
        self._walk(self.source)

    def _validate_paths(self):
        if not self.source.exists():
            raise FileNotFoundError(f"Source directory not found: {self.source}")
        if not self.source.is_dir():
            raise NotADirectoryError(f"Source path is not a directory: {self.source}")
        if self.destination.resolve().is_relative_to(self.source.resolve()):
            raise shutil.Error("Destination is within source; operation would recurse.")

    def _walk(self, current_directory: Path):
        for directory_or_file in current_directory.iterdir():
            if directory_or_file.is_dir():
                if self._is_destination(directory_or_file):
                    continue
                self._walk(directory_or_file)
            elif directory_or_file.is_file():
                self._copy_file(directory_or_file)

    def _copy_file(self, file_path: Path):
        target_directory = self.destination / self._extension_name(file_path)
        target_directory.mkdir(parents=True, exist_ok=True)
        target_path = target_directory / file_path.name
        shutil.copy2(file_path, target_path)

    def _extension_name(self, file_path: Path) -> str:
        return file_path.suffix.lstrip(".").lower() or "no_extension"

    def _is_destination(self, path: Path) -> bool:
        dest_resolved = self.destination.resolve()
        path_resolved = path.resolve()
        return path_resolved == dest_resolved or path_resolved.is_relative_to(
            dest_resolved
        )


def main():
    args = parse_args()
    sorter = FileSorter(Path(args.source), Path(args.destination))
    sorter.run()


if __name__ == "__main__":
    main()
