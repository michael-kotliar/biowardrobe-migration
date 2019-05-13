#! /usr/bin/env python3
import sys
import logging
from biowardrobe_migration.components.parser import parse_arguments


logger = logging.getLogger(__name__)


def main(argsl=None):
    if argsl is None:
        argsl = sys.argv[1:]
    args = parse_arguments(argsl)


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))