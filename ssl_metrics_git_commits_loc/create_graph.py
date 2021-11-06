from argparse import ArgumentParser, Namespace
from operator import itemgetter
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


def findBestFitLine(x: list, y: list, maximumDegrees: int) -> tuple:
    # https://www.w3schools.com/Python/python_ml_polynomial_regression.asp
    data: list = []

    degree: int
    for degree in range(maximumDegrees):
        model: np.poly1d = np.poly1d(np.polyfit(x, y, degree))
        r2Score: np.float64 = r2_score(y, model(x))
        temp: tuple = (r2Score, model)
        data.append(temp)

    return max(data, key=itemgetter(0))


def plotLOC(
    df: DataFrame,
    xLabel: str,
    yLabel: str,
    title: str,
    filename: str,
) -> tuple:
    x: list = [x for x in range(len(df["loc_sum"]))]
    y: list = df["loc_sum"].tolist()

    figure: Figure = plt.figure()

    plt.xlabel(xlabel=xLabel)
    plt.ylabel(ylabel=yLabel)
    plt.title(title)
    plt.plot(x, y)
    plt.tight_layout()

    figure.savefig(filename)
    figure.clf()
    return (x, y)


def plotDeltaLOC(
    df: DataFrame,
    xLabel: str,
    yLabel: str,
    title: str,
    filename: str,
) -> tuple:
    x: list = [x for x in range(len(df["delta_loc"]))]
    y: list = df["delta_loc"].tolist()

    figure: Figure = plt.figure()

    plt.xlabel(xlabel=xLabel)
    plt.ylabel(ylabel=yLabel)
    plt.title(title)
    plt.plot(x, y)
    plt.tight_layout()

    figure.savefig(filename)
    figure.clf()
    return (x, y)


def plotKLOC(
    df: DataFrame,
    xLabel: str,
    yLabel: str,
    title: str,
    filename: str,
) -> tuple:
    x: list = [x for x in range(len(df["kloc"]))]
    y: list = df["kloc"].to_list()

    figure: Figure = plt.figure()

    plt.xlabel(xlabel=xLabel)
    plt.ylabel(ylabel=yLabel)
    plt.title(title)
    plt.plot(x, y)
    plt.tight_layout()

    figure.savefig(filename)
    figure.clf()

    return (x, y)


def plotBestFitLine(
    x: list,
    y: list,
    maximumDegree: int,
    xLabel: str,
    yLabel: str,
    title: str,
    filename: str,
) -> np.poly1d:
    data: tuple = findBestFitLine(x=x, y=y, maximumDegrees=maximumDegree)

    model: np.poly1d = data[1]
    line: np.ndarray = np.linspace(0, max(x), 100)

    figure: Figure = plt.figure()

    plt.ylabel(ylabel=yLabel)
    plt.xlabel(xlabel=xLabel)
    plt.title(title)

    plt.scatter(x, y, color="black")
    plt.plot(line, model(line))
    figure.savefig(filename)
    figure.clf()

    return model

def plotDerivative (
    model: np.poly1d,
    order: int,
    maximumXValue: int,
    xLabel: str,
    yLabel: str,
    title: str,
    filename: str,
) -> np.poly1d:
    model = np.polyder(p=model, m=order)
    line: np.ndarray = np.linspace(0, maximumXValue, 100)

    figure: Figure = plt.figure()

    plt.ylabel(ylabel=yLabel)
    plt.xlabel(xlabel=xLabel)
    plt.title(title)

    plt.plot(line, model(line))
    figure.savefig(filename)
    figure.clf()

    return model

def main() -> None:
    locXLabel: str = "Commit"
    locYLabel: str = "LOC"
    locTitle: str = "Lines of Code (LOC) / Commits"

    dlocXLabel: str = locXLabel
    dlocYLabel: str = "ΔLOC"
    dlocTitle: str = "Change of Lines of Code (ΔLOC) / Days"

    klocXLabel: str = locXLabel
    klocYLabel: str = "KLOC"
    klocTitle: str = "Thousands of Lines of Code (KLOC) / Days"

    args: Namespace = getArgparse()

    if args.input[-5::] != ".json":
        print("Invalid input file type. Input file must be JSON")
        quit(1)

    df: DataFrame = pandas.read_json(args.input)

    loc: tuple = plotLOC(
        df=df,
        xLabel=locXLabel,
        yLabel=locYLabel,
        title=locTitle,
        filename=args.graph_loc,
    )
    dloc: tuple = plotDeltaLOC(
        df=df,
        xLabel=dlocXLabel,
        yLabel=dlocYLabel,
        title=dlocTitle,
        filename=args.graph_delta_loc,
    )
    kloc: tuple = plotKLOC(
        df=df,
        xLabel=klocXLabel,
        yLabel=klocYLabel,
        title=klocTitle,
        filename=args.graph_k_loc,
    )

    bfLOC: np.poly1d = plotBestFitLine(
        x=loc[0],
        y=loc[1],
        maximumDegree=15,
        xLabel=locXLabel,
        yLabel=locYLabel,
        title=locTitle,
        filename=args.graph_best_fit_loc,
    )

    vLOC: np.poly1d = plotDerivative(model=bfLOC, order=1, maximumXValue=max(loc[0]), xLabel=locXLabel, yLabel="Velocity", title="Velocity of LOC / Commits", filename="velocityLOC.png")

    aLOC: np.poly1d = plotDerivative(model=vLOC, order=1, maximumXValue=max(loc[0]), xLabel=locXLabel, yLabel="Acceleration", title="Acceleration of LOC / Commits", filename="accelerationLOC.png")

if __name__ == "__main__":
    main()
