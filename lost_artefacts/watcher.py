import hashlib
import sys
import time
from pathlib import Path

from lost_artefacts.builder import build
from lost_artefacts.common import SRC_DIR


def get_file_hash(file_path: Path) -> str:
    return hashlib.md5(file_path.read_bytes()).hexdigest()


def get_file_hashes(directories: list[Path]) -> dict[Path, str]:
    result = {}
    for directory in directories:
        for path in directory.rglob("*"):
            if path.is_file():
                result[path] = get_file_hash(path)
    return result


def watch() -> None:
    directories = [SRC_DIR]
    hashes = {}

    while True:
        if (new_hashes := get_file_hashes(directories)) != hashes:
            print("Detected change, rebuilding")
            try:
                build()
            except Exception as ex:
                print(ex, file=sys.stderr)
            else:
                hashes = new_hashes

        time.sleep(1)
