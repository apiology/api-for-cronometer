"""Console script for api_for_cronometer."""
import argparse
import sys
from typing import List


def parse_argv(argv: List[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument('_', nargs='*')
    return parser.parse_args(argv[1:])


def process_args(args: argparse.Namespace) -> int:
    print("Arguments: " + str(args._))
    print("Replace this message by putting your code into "
          "api_for_cronometer.cli.process_args")
    return 0


def main(argv: List[str] = sys.argv) -> int:
    """Console script for api_for_cronometer."""

    args = parse_argv(argv)

    return process_args(args)


if __name__ == "__main__":
    sys.exit(main())  # pragma: no cover