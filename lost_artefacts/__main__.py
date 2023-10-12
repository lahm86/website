import argparse

from lost_artefacts.builder import build
from lost_artefacts.watcher import watch


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("-w", "--watch", action="store_true")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    if args.watch:
        watch()
    else:
        build()


if __name__ == "__main__":
    main()
