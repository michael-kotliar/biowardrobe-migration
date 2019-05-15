#! /usr/bin/env python3
import sys
import logging
from json import dumps
from biowardrobe_migration.components.parser import parse_arguments
from biowardrobe_migration.components.logger import reset_root_logger
from biowardrobe_migration.components.connection import Connect
from biowardrobe_migration.components.processor import get_broken_experiments, get_statistics


def main(argsl=None):
    if argsl is None:
        argsl = sys.argv[1:]
    args = parse_arguments(argsl)

    # Set logger level
    if args.debug:
        reset_root_logger(logging.DEBUG)
    elif args.quiet:
        reset_root_logger(logging.ERROR)
    else:
        reset_root_logger(logging.INFO)

    connection = Connect(args.config)
    broken_experiments = get_broken_experiments(connection)
    logging.info(dumps(get_statistics(broken_experiments), indent=4))


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))