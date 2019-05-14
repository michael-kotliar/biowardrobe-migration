#! /usr/bin/env python3
import sys
import logging
from json import dumps
from biowardrobe_migration.components.parser import parse_arguments
from biowardrobe_migration.components.connection import Connect
from biowardrobe_migration.components.processor import scan_outputs


logger = logging.getLogger(__name__)


def main(argsl=None):
    if argsl is None:
        argsl = sys.argv[1:]
    args = parse_arguments(argsl)

    connection = Connect(args.config)

    collected_broken_outputs = scan_outputs(connection)
    print(dumps(collected_broken_outputs, indent=4))


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))