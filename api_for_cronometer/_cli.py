"""Console script for api_for_cronometer."""
import argparse
import sys
from typing import Dict, List

import requests

from .api_for_cronometer import update_macro_target
from .login import login


def options_provided(args: argparse.Namespace) -> bool:
    options: Dict[str, object] = vars(args).copy()
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
    update_parser.add_argument('--saturated', metavar='TARGET_GRAMS,MAX_GRAMS', type=str,
                               help='Saturated fat in grams (target and max, comma separated)')
    args = parser.parse_args(argv[1:])
    if args.operation == 'update-macro-targets' and not options_provided(args):
        update_parser.error('Please provide an argument to update-macro-targets')
    if args.operation is None:
        # Not sure why coverage doesn't recognize this, but it is in fact tested
        parser.error('Please provide a command')  # pragma: no cover
    return args


def process_args(args: argparse.Namespace) -> int:
    if args.operation == 'update-macro-targets':
        requests_session = login()
        update_macro_targets(requests_session, args)
    else:
        raise NotImplementedError(f"implement {args}")
    return 0


def update_macro_targets(requests_session: requests.Session, args: argparse.Namespace) -> None:
    if args.energy is not None:
        target, max_ = args.energy.split(',')
        update_macro_target(requests_session, 'energy', target, max_)
    if args.protein is not None:
        target, max_ = args.protein.split(',')
        update_macro_target(requests_session, 'protein', target, max_)
    if args.net_carbs is not None:
        target, max_ = args.net_carbs.split(',')
        update_macro_target(requests_session, 'net_carbs', target, max_)
    if args.saturated is not None:
        target, max_ = args.saturated.split(',')
        update_macro_target(requests_session, 'saturated', target, max_)


def main(argv: List[str] = sys.argv) -> int:
    """Console script for api_for_cronometer."""

    args = parse_argv(argv)

    return process_args(args)


if __name__ == "__main__":
    sys.exit(main())  # pragma: no cover
