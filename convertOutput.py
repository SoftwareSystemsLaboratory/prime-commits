import pandas
from argparse import ArgumentParser


def get_argparse() -> ArgumentParser:
    parser: ArgumentParser = ArgumentParser(
        prog="Git All Python (CLI Only)",
        usage="This program outputs the lines of code (LOC) per commit and the delta LOC of a Git repository in JSON format.",
    )
    parser.add_argument(
        "-d",
        "--directory",
        help="Directory containing repository root folder (.git)",
        default=".",
        type=str,
        required=False,
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
