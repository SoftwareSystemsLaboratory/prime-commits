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
        "-l",
        "--graph-loc",
        help="The filename to output the LOC graph to",
        type=str,
        required=True,
    )
    parser.add_argument(
        "-d",
        "--graph-delta-loc",
        help="The filename to output the Delta LOC graph to",
        type=str,
        required=True,
    )
    parser.add_argument(
        "-k",
        "--graph-k-loc",
        help="The filename to output the K LOC graph to",
        type=str,
        required=True,
    )
    return parser.parse_args()


def plot_LOC(df: DataFrame, filename: str) -> None:
    figure: Figure = plt.figure()
    plt.ylabel("LOC")
    plt.xlabel("Commit Number")
    plt.title("Lines of Code (LOC) Over Commits")
    plt.plot([x for x in range(len(df["loc_sum"]))], df["loc_sum"])
    figure.savefig(filename)
    figure.clf()


def plot_DeltaLOC(df: DataFrame, filename: str) -> None:
    figure: Figure = plt.figure()
    plt.ylabel("Delta LOC")
    plt.xlabel("Commit Number")
    plt.title("Change of Lines of Code (Delta LOC) Over Commits")
    plt.plot([x for x in range(len(df["delta_loc"]))], df["delta_loc"])
    figure.savefig(filename)
    figure.clf()


def plot_KLOC(df: DataFrame, filename: str) -> None:
    figure: Figure = plt.figure()
    plt.ylabel("KLOC")
    plt.xlabel("Commit Number")
    plt.title("Thousands of Lines of Code (KLOC) Over Commits")
    plt.plot([x for x in range(len(df["kloc"]))], df["kloc"])
    figure.savefig(filename)


def main() -> None:
    args: Namespace = get_argparse()

    if args.input[-5::] != ".json":
        print("Invalid input file type. Input file must be JSON")
        quit(1)

    df: DataFrame = pandas.read_json(args.input)

    plot_LOC(df, filename=args.graph_loc)
    plot_DeltaLOC(df, filename=args.graph_delta_loc)
    plot_KLOC(df, filename=args.graph_k_loc)


if __name__ == "__main__":
    main()
