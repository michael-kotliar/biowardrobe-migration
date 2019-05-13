import os
import logging
import argparse


logger = logging.getLogger(__name__)


def normalize_args(args, skip_list=[]):
    """ Converts all relative path arguments to absolute ones relatively to the current working directory """
    normalized_args = {}
    for key,value in args.__dict__.items():
        if key not in skip_list:
            normalized_args[key] = value if not value or os.path.isabs(value) else os.path.normpath(os.path.join(os.getcwd(), value))
        else:
            normalized_args[key]=value
    return argparse.Namespace (**normalized_args)


def get_parser():
    """ Return parser """
    parser = argparse.ArgumentParser(description='BioWardrobe Migration', add_help=True)
    parser.add_argument("-c", "--config", help="Path to the BioWardrobe config file", default="/etc/wardrobe/wardrobe")
    return parser


def parse_arguments(argsl):
    """ Parses and normalizes arguments """
    args,_ = get_parser().parse_known_args(argsl)
    return normalize_args(args)