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
        "--csv",
        help="Flag to set the output of the conversion to a .csv file",
        default=None,
        type=bool,
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
