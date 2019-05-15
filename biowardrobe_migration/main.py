#! /usr/bin/env python3
import sys
import logging
from json import dumps
from biowardrobe_migration.components.parser import parse_arguments
from biowardrobe_migration.components.connection import Connect
from biowardrobe_migration.components.processor import get_broken_experiments, get_statistics


logger = logging.getLogger(__name__)


def main(argsl=None):
    if argsl is None:
        argsl = sys.argv[1:]
    args = parse_arguments(argsl)

    connection = Connect(args.config)

    broken_experiments = get_broken_experiments(connection)
    logger.info(dumps(get_statistics(broken_experiments), indent=4))


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))