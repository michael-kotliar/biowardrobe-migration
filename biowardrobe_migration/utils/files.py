#! /usr/bin/env python3
import os


def norm_path(path):
    return os.path.abspath(os.path.normpath(os.path.normcase(path)))


def open_file(filename):
    """Returns list of lines from the text file. \n at the end of the lines are trimmed. Empty lines are excluded"""
    lines = []
    with open(filename, 'r') as infile:
        for line in infile:
            if line.strip():
                lines.append(line.strip())
    return lines


def get_broken_locations(outputs):
    broken, correct = {}, {}
    for k, v in outputs.items():
        try:
            correct.update({k: v}) if os.path.exists(v["location"]) else broken.update({k: v})
        except:
            correct.update({k: v})
    return broken, correct
