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
        prog="ssl-metrics-git-commits-loc Graph Generator",
        usage="This is a proof of concept demonstrating that it is possible to use Git commits to compute metrics.",
        description="The default action is to graph all figures of LOC on a single chart. If multiple data and/or graphing options are choosen the output filename and the title of the figure/chartwill reflect the combination that is being graphed."
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
        required=False,
    )
    parser.add_argument(
        "-r",
        "--repository-name",
        help="Name of the repository that is being analyzed. Will be used in the graph title",
        type=str,
        required=True,
    )
    parser.add_argument(
        "--loc",
        help="Utilize LOC data",
        required=False,
        action="store_true"
        )
    parser.add_argument(
        "--dloc",
        help="Utilize Delta LOC data",
        required=False,
        action="store_true"
    )
    parser.add_argument(
        "--kloc",
        help="Utilize KLOC data",
        required=False,
        action="store_true"
        )
    parser.add_argument(
        "--graph-data",
        help="Graph the raw data. Discrete graph of the data",
        required=False,
        action="store_true"
        )
    parser.add_argument(
        "--graph-best-fit",
        help="Graph the best fit polynomial of the data. Continous graph of the data. Polynomial degrees can be configured with `-m`",
        required=False,
        action="store_true"
        )
    parser.add_argument(
        "--graph-velocity",
        help="Graph the velocity of the data. Computes the best fit polynomial and takes the first derivitve. Polynomial degrees can be configured with `-m`",
        required=False,
        action="store_true"
        )
    parser.add_argument(
        "--graph-acceleration",
        help="Graph the acceleration of the data. Computes the best fit polynomial and takes the second derivitve. Polynomial degrees can be configured with `-m`",
        required=False,
        action="store_true"
        )
    parser.add_argument(
        "--graph-all",
        help="Graphs all possible figures of the data onto one chart. Computes the best fit polynomial and takes the first and second derivitve. Polynomial degrees can be configured with `-m`",
        required=False,
        action="store_true"
        )
    parser.add_argument(
        "--x-min",
        help="The smallest x value that will be plotted",
        type=int,
        required=False,
        default=0,
    )
    parser.add_argument(
        "--x-max",
        help="The largest x value that will be plotted",
        type=int,
        required=False,
        default=-1,
    )
    parser.add_argument(
        "-m",
        "--maximum-degree-polynomial",
        help="Estimated maximum degree of the best fit polynomial ",
        type=int,
        required=False,
        default=15,
    )
    return parser.parse_args()


def __findBestFitLine(x: list, y: list, maximumDegree: int) -> tuple:
    # https://www.w3schools.com/Python/python_ml_polynomial_regression.asp
    data: list = []

    degree: int
    for degree in range(maximumDegree):
        model: np.poly1d = np.poly1d(np.polyfit(x, y, degree))
        r2Score: np.float64 = r2_score(y, model(x))
        temp: tuple = (r2Score, model)
        data.append(temp)

    return max(data, key=itemgetter(0))


def _graphFigure(
    repositoryName: str,
    xLabel: str,
    yLabel: str,
    title: str,
    x: list,
    y: list,
    maximumDegree: int,
    filename: str,
) -> None:
    figure: Figure = plt.figure()
    plt.suptitle(repositoryName)

    # Actual Data
    plt.subplot(2, 2, 1)
    plt.xlabel(xlabel=xLabel)
    plt.ylabel(ylabel=yLabel)
    plt.title(title)
    plt.plot(x, y)
    plt.tight_layout()

    # Best Fit
    plt.subplot(2, 2, 2)
    data: tuple = __findBestFitLine(x=x, y=y, maximumDegree=maximumDegree)
    bfModel: np.poly1d = data[1]
    line: np.ndarray = np.linspace(0, max(x), 100)
    plt.ylabel(ylabel=yLabel)
    plt.xlabel(xlabel=xLabel)
    plt.title("Best Fit Line")
    plt.plot(line, bfModel(line))
    plt.tight_layout()

    # Velocity of Best Fit
    plt.subplot(2, 2, 3)
    velocityModel = np.polyder(p=bfModel, m=1)
    line: np.ndarray = np.linspace(0, max(x), 100)
    plt.ylabel(ylabel="Velocity Unit")
    plt.xlabel(xlabel=xLabel)
    plt.title("Velocity")
    plt.plot(line, velocityModel(line))
    plt.tight_layout()

    # Acceleration of Best Fit
    plt.subplot(2, 2, 4)
    accelerationModel = np.polyder(p=bfModel, m=2)
    line: np.ndarray = np.linspace(0, max(x), 100)
    plt.ylabel(ylabel="Acceleration Unit")
    plt.xlabel(xlabel=xLabel)
    plt.title("Acceleration")
    plt.plot(line, accelerationModel(line))
    plt.tight_layout()

    figure.savefig(filename)
    figure.clf()


def plot(
    x: list,
    y: list,
    xLabel: str,
    yLabel: str,
    title: str,
    maximumDegree: int,
    repositoryName: str,
    filename: str,
) -> tuple:
    _graphFigure(
        repositoryName=repositoryName,
        xLabel=xLabel,
        yLabel=yLabel,
        title=title,
        x=x,
        y=y,
        maximumDegree=maximumDegree,
        filename=filename,
    )
    return (x, y)


def main() -> None:
    args: Namespace = getArgparse()

    if args.input[-5::] != ".json":
        print("Invalid input file type. Input file must be JSON")
        quit(1)
    if args.x_min < 0:
        print("Invalid x window min. X window min >= 0")
        quit(2)
    if args.maximum_degree_polynomial < 1:
        print("The maximum degree polynomial is too small. Maximum degree polynomial >= 1")
        quit(3)
    if (args.loc and args.dloc and args.kloc) is False:
        print("No data source choosen. Defaulting to LOC")
        args.loc = True
    if (args.graph_data and args.graph_best_fit and args.graph_velocity and args.args.graph_acceleration and args.args.graph_all) is False:
        print("No graph choosen. Defaulting to graphing all figures on a single chart")
        args.graph_all = True
    print(args)
    quit()

    locXLabel: str = "Commit"
    locYLabel: str = "LOC"
    locTitle: str = "Lines of Code (LOC) / Commits"

    dlocXLabel: str = locXLabel
    dlocYLabel: str = "ΔLOC"
    dlocTitle: str = "Change of Lines of Code (ΔLOC) / Days"

    klocXLabel: str = locXLabel
    klocYLabel: str = "KLOC"
    klocTitle: str = "Thousands of Lines of Code (KLOC) / Days"

    df: DataFrame = pandas.read_json(args.input)

    if args.x_window_max <= -1:
        x: list = [x for x in range(len(df["kloc"]))][args.x_window_min :]
        yLoc: list = df["loc_sum"].tolist()[args.x_window_min :]
        yDLoc: list = df["delta_loc"].tolist()[args.x_window_min :]
        yKLoc: list = df["kloc"].to_list()[args.x_window_min :]
    else:
        x: list = [x for x in range(len(df["kloc"]))][
            args.x_window_min : args.x_window_max + 1
        ]
        yLoc: list = df["loc_sum"].tolist()[args.x_window_min : args.x_window_max + 1]
        yDLoc: list = df["delta_loc"].tolist()[
            args.x_window_min : args.x_window_max + 1
        ]
        yKLoc: list = df["kloc"].to_list()[args.x_window_min : args.x_window_max + 1]

    if args.graph_loc_filename != None:
        # LOC
        plot(
            x=x,
            y=yLoc,
            xLabel=locXLabel,
            yLabel=locYLabel,
            title=locTitle,
            maximumDegree=args.maximum_degree_polynomial,
            repositoryName=args.repository_name,
            filename=args.graph_loc_filename,
        )

    if args.graph_delta_loc_filename != None:
        # DLOC
        plot(
            x=x,
            y=yDLoc,
            xLabel=dlocXLabel,
            yLabel=dlocYLabel,
            title=dlocTitle,
            maximumDegree=args.maximum_degree_polynomial,
            repositoryName=args.repository_name,
            filename=args.graph_delta_loc_filename,
        )

    if args.graph_k_loc_filename != None:
        # KLOC
        plot(
            x=x,
            y=yKLoc,
            xLabel=klocXLabel,
            yLabel=klocYLabel,
            title=klocTitle,
            maximumDegree=args.maximum_degree_polynomial,
            repositoryName=args.repository_name,
            filename=args.graph_k_loc_filename,
        )


if __name__ == "__main__":
    main()
