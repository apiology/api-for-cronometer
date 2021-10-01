"""Console script for api_for_cronometer."""
import argparse
import sys
from typing import List


def options_provided(args: argparse.Namespace) -> bool:
    options = vars(args).copy()
    options.pop('operation')
    return any([
        value is not None
        for name, value in options.items()
    ])


def parse_argv(argv: List[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    # https://docs.python.org/3/library/argparse.html
    # https://docs.python.org/3/library/argparse.html#argparse.ArgumentParser.add_subparsers
    subparsers = parser.add_subparsers(dest='operation')
    update_parser = subparsers.add_parser('update-macro-targets',
                                          description='Update macronutrient targets',
                                          help='Update macronutrient targets')
    update_parser.add_argument('--energy', metavar='TARGET_KCALS,MAX_KCALS', type=str,
                               help='Energy in (kilo-)calories (target and max, comma separated)')
    update_parser.add_argument('--protein', metavar='TARGET_GRAMS,MAX_GRAMS', type=str,
                               help='Protein in grams (target and max, comma separated)')
    update_parser.add_argument('--net-carbs', metavar='TARGET_GRAMS,MAX_GRAMS', type=str,
                               help='Net carbs in grams (target and max, comma separated)')
    update_parser.add_argument('--fat', metavar='TARGET_GRAMS,MAX_GRAMS', type=str,
                               help='Fat in grams (target and max, comma separated)')
    args = parser.parse_args(argv[1:])
    if args.operation == 'update-macro-targets' and not options_provided(args):
        update_parser.error('Please provide an argument to update-macro-targets')
    if args.operation is None:
        # Not sure why coverage doesn't recognize this, but it is in fact tested
        parser.error('Please provide a command')  # pragma: no cover
    return args


def process_args(args: argparse.Namespace) -> int:
    print("Arguments: " + str(args))
    print("Replace this message by putting your code into "
          "api_for_cronometer.cli.process_args")
    return 0


def main(argv: List[str] = sys.argv) -> int:
    """Console script for api_for_cronometer."""

    args = parse_argv(argv)

    return process_args(args)


if __name__ == "__main__":
    sys.exit(main())  # pragma: no cover
