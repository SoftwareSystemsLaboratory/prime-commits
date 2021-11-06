from argparse import ArgumentParser, Namespace
from os import path

import matplotlib.pyplot as plt
import pandas
from matplotlib.figure import Figure
from numpy.polynomial import Polynomial as poly
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
    parser.add_argument(
        "-b",
        "--graph-best-fit-loc",
        help="The filename to output the Line of Best Fit for the LOC graph",
        type=str,
        required=True,
    )
    return parser.parse_args()


def plot_LOC(df: DataFrame, filename: str) -> None:
    figure: Figure = plt.figure()
    plt.ylabel("LOC")
    plt.xlabel("Commit Number")
    plt.title("Lines of Code (LOC) Over Commits")
    plt.scatter([x for x in range(len(df["loc_sum"]))], df["loc_sum"])
    plt.tight_layout()
    figure.savefig(filename)
    figure.clf()


def plot_DeltaLOC(df: DataFrame, filename: str) -> None:
    figure: Figure = plt.figure()
    plt.ylabel("Delta LOC")
    plt.xlabel("Commit Number")
    plt.title("Change of Lines of Code (Delta LOC) Over Commits")
    plt.plot([x for x in range(len(df["delta_loc"]))], df["delta_loc"])
    plt.tight_layout()
    figure.savefig(filename)
    figure.clf()


def plot_KLOC(df: DataFrame, filename: str) -> None:
    figure: Figure = plt.figure()
    plt.ylabel("KLOC")
    plt.xlabel("Commit Number")
    plt.title("Thousands of Lines of Code (KLOC) Over Commits")
    plt.plot([x for x in range(len(df["kloc"]))], df["kloc"])
    plt.tight_layout()
    figure.savefig(filename)


def plot_BestFit_LOC(df: DataFrame, filename: str) -> None:
    figure: Figure = plt.figure()
    plt.ylabel("?")
    plt.xlabel("Commit Number")
    plt.title("Line of Best Fit for LOC Graph")

    x: list = [x for x in range(len(df["loc_sum"]))]
    yActual = df["loc_sum"]

    p = poly.fit(x, yActual, 3).convert().coef
    pLength: int = len(p) 
    yBestFit: list = []

    xValue: int
    for xValue in x:
        sum: float = 0

        pointer: int
        for pointer in range(pLength):
            sum += (xValue ** (pLength - (pointer + 1))) * p[pointer]
        
        sum += p[-1]
        yBestFit.append(sum)

    equation:str = ""
    for pointer in range(pLength):
        equation += f"{p[pointer]}x^{pLength - (pointer + 1)} + "
   
    plt.plot(x, yBestFit)
    # plt.plot(x, yActual, color="black")

    plt.tight_layout()
    figure.savefig(filename)
    figure.clf()
    print(equation)

def main() -> None:
    args: Namespace = get_argparse()

    if args.input[-5::] != ".json":
        print("Invalid input file type. Input file must be JSON")
        quit(1)

    df: DataFrame = pandas.read_json(args.input)

    plot_LOC(df, filename=args.graph_loc)
    plot_DeltaLOC(df, filename=args.graph_delta_loc)
    plot_KLOC(df, filename=args.graph_k_loc)
    plot_BestFit_LOC(df, args.graph_best_fit_loc)


if __name__ == "__main__":
    main()
