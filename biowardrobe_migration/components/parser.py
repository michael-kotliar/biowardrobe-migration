#! /usr/bin/env python3
import os
import argparse
from biowardrobe_migration.utils.files import norm_path


def normalize_args(args, skip_list=[]):
    """ Converts all relative path arguments to absolute ones relatively to the current working directory """
    normalized_args = {}
    for key,value in args.__dict__.items():
        if key not in skip_list:
            normalized_args[key] = value if not value or os.path.isabs(value) else norm_path(os.path.join(os.getcwd(), value))
        else:
            normalized_args[key]=value
    return argparse.Namespace (**normalized_args)


def get_parser():
    """ Return parser """
    parser = argparse.ArgumentParser(description='BioWardrobe Migration', add_help=True)
    parser.add_argument("-c", "--config", help="Path to the BioWardrobe config file", default="/etc/wardrobe/wardrobe")
    logging_level = parser.add_mutually_exclusive_group()
    logging_level.add_argument("-d", "--debug",    help="Output debug information", action="store_true")
    logging_level.add_argument("-q", "--quiet",    help="Suppress all outputs except errors", action="store_true")
    return parser


def parse_arguments(argsl, skip_list=["debug", "quiet"]):
    """ Parses and normalizes arguments """
    args,_ = get_parser().parse_known_args(argsl)
    return normalize_args(args, skip_list)