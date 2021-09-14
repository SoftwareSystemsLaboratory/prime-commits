from argparse import ArgumentParser, Namespace
from os import path

import matplotlib.pyplot as plt
import pandas
from matplotlib.figure import Figure
from pandas import DataFrame


def get_argparse() -> Namespace:
    parser: ArgumentParser = ArgumentParser(
        prog="Convert Output",
        usage="This program converts a JSON file into various different formats.",
    )
    parser.add_argument(
        "-i",
        "--input",
        help="The input data file that will be read to create the graphs",
        type=str,
        required=True,
    )
    parser.add_argument(
        "-o",
        "--output",
        help="The filename to output the graph to",
        type=str,
        required=True,
    )
    return parser.parse_args()


# delta_loc over time where time is spaced by commit
def plot(df: DataFrame, filename: str) -> None:
    figure: Figure = plt.figure()
    plt.ylabel("delta_loc")
    plt.xlabel("Commit Number")
    plt.title("delta_loc Over Commits")
    plt.plot([x for x in range(len(df["delta_loc"]))], df["delta_loc"])
    figure.savefig(filename)


def main():
    args: Namespace = get_argparse()

    if args.input[-5::] != ".json":
        print("Invalid input file type. Input file must be JSON")
        quit(1)

    df: DataFrame = pandas.read_json(args.input)

    plot(df, filename=args.output)


if __name__ == "__main__":
    main()
