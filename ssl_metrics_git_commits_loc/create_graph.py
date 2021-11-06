from argparse import ArgumentParser, Namespace
from os import path

import matplotlib.pyplot as plt
import numpy as np
import pandas
from matplotlib.figure import Figure
from pandas import DataFrame
from sklearn.metrics import r2_score


def getArgparse() -> Namespace:
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


def findBestFitLine(x: list, y: list, maximumDegrees: int)   ->  dict:
        # https://www.w3schools.com/Python/python_ml_polynomial_regression.asp
        data: dict = {}

        degree: int
        for degree in maximumDegrees:
            temp: dict = {}
            model: np.poly1d = np.poly1d(np.polyfit(x, y, degree))
            temp["model"] = model
            temp["r2Score"] = r2_score(y, model(x))
            data[degree] = temp

        return data


def plotLOC(df: DataFrame, filename: str) -> tuple:
    x: list = [x for x in range(len(df["loc_sum"]))]
    y: list = df["loc_sum"].tolist()

    figure: Figure = plt.figure()

    plt.ylabel("LOC")
    plt.xlabel("Commit Number")
    plt.title("Lines of Code (LOC) Over Commits")
    plt.plot(x, y)
    plt.tight_layout()

    figure.savefig(filename)
    figure.clf()
    return (x, y)

def plotDeltaLOC(df: DataFrame, filename: str) -> tuple:
    x: list = [x for x in range(len(df["delta_loc"]))]
    y: list = df["delta_loc"].tolist()

    figure: Figure = plt.figure()

    plt.ylabel("Delta LOC")
    plt.xlabel("Commit Number")
    plt.title("Change of Lines of Code (Delta LOC) Over Commits")
    plt.plot(x, y)
    plt.tight_layout()

    figure.savefig(filename)
    figure.clf()
    return (x,y)


def plotKLOC(df: DataFrame, filename: str) -> tuple:
    x: list = [x for x in range(len(df["kloc"]))]
    y: list = df["kloc"].to_list()

    figure: Figure = plt.figure()

    plt.ylabel("KLOC")
    plt.xlabel("Commit Number")
    plt.title("Thousands of Lines of Code (KLOC) Over Commits")
    plt.plot(x, y)
    plt.tight_layout()

    figure.savefig(filename)
    figure.clf()

    return (x,y)

def plotBestFitLine(x: list, y:list, maximumDegree:int, filename: str) -> None:

    model = np.poly1d(np.polyfit(x, y, 15))
    print(r2_score(y, model(x)))
    myLine: np.ndarray = np.linspace(0, max(x), 100)

    figure: Figure = plt.figure()
    plt.ylabel("?")
    plt.xlabel("Commit Number")
    plt.title("Line of Best Fit for LOC Graph")

    plt.plot(x, y)
    plt.plot(myLine, model(myLine), "g--")
    figure.savefig(filename)
    figure.clf()


def main() -> None:
    args: Namespace = getArgparse()

    if args.input[-5::] != ".json":
        print("Invalid input file type. Input file must be JSON")
        quit(1)

    df: DataFrame = pandas.read_json(args.input)

    plotLOC(df, filename=args.graph_loc)
    plotDeltaLOC(df, filename=args.graph_delta_loc)
    plotKLOC(df, filename=args.graph_k_loc)
    plotBestFitLOC(df, args.graph_best_fit_loc)


if __name__ == "__main__":
    main()
