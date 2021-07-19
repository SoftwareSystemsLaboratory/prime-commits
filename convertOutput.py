from typing import Tuple
import pandas
from argparse import ArgumentParser


def get_argparse() -> ArgumentParser:
    parser: ArgumentParser = ArgumentParser(
        prog="Convert Output",
        usage="This program converts a JSON file into various different formats.",
    )
    parser.add_argument(
        "-i",
        "--input",
        help="The input JSON file that is to be converted",
        type=str,
        required=True,
    )
    parser.add_argument(
        "-b",
        "--branch",
        help="Default branch for analysis to be ran on",
        default="main",
        type=str,
        required=False,
    )
    parser.add_argument(
        "-s",
        "--save-json",
        help="Save analysis to JSON file (EX: --save-json=output.json)",
        default=True,
        type=str,
        required=False,
    )
    return parser
