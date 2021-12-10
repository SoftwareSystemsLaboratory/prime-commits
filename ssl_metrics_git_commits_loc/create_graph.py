from argparse import ArgumentParser, Namespace
from operator import itemgetter
from os import path
from pathlib import Path

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
        description="The default action is to graph all figures of LOC on a single chart. If multiple data and/or graphing options are choosen the output filename and the title of the figure/chartwill reflect the combination that is being graphed.",
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
    parser.add_argument(
        "-r",
        "--repository-name",
        help="Name of the repository that is being analyzed. Will be used in the graph title",
        type=str,
        required=True,
    )
    parser.add_argument(
        "--loc", help="Utilize LOC data", required=False, action="store_true"
    )
    parser.add_argument(
        "--dloc", help="Utilize Delta LOC data", required=False, action="store_true"
    )
    parser.add_argument(
        "--kloc", help="Utilize KLOC data", required=False, action="store_true"
    )
    parser.add_argument(
        "--graph-data",
        help="Graph the raw data. Discrete graph of the data",
        required=False,
        action="store_true",
    )
    parser.add_argument(
        "--graph-best-fit",
        help="Graph the best fit polynomial of the data. Continous graph of the data. Polynomial degrees can be configured with `-m`",
        required=False,
        action="store_true",
    )
    parser.add_argument(
        "--graph-velocity",
        help="Graph the velocity of the data. Computes the best fit polynomial and takes the first derivitve. Polynomial degrees can be configured with `-m`",
        required=False,
        action="store_true",
    )
    parser.add_argument(
        "--graph-acceleration",
        help="Graph the acceleration of the data. Computes the best fit polynomial and takes the second derivitve. Polynomial degrees can be configured with `-m`",
        required=False,
        action="store_true",
    )
    parser.add_argument(
        "--graph-all",
        help="Graphs all possible figures of the data onto one chart. Computes the best fit polynomial and takes the first and second derivitve. Polynomial degrees can be configured with `-m`",
        required=False,
        action="store_true",
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
        "--maximum-polynomial-degree",
        help="Estimated maximum degree of the best fit polynomial",
        type=int,
        required=False,
        default=15,
    )
    parser.add_argument(
        "-s",
        "--stepper",
        help="Step through every nth data point",
        type=int,
        required=False,
        default=1,
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


def _appendID(filename: str, id: str) -> str:
    p = Path(filename)
    return "{0}_{2}{1}".format(Path.joinpath(p.parent, p.stem), p.suffix, id)


def _graphData(
    title: str,
    xLabel: str,
    yLabel: str,
    xData: list,
    yData: list,
) -> Figure:
    figure: Figure = plt.figure()
    plt.title(title)
    plt.xlabel(xlabel=xLabel)
    plt.ylabel(ylabel=yLabel)
    plt.plot(xData, yData)
    plt.tight_layout()
    return figure


def _graphBestFit(
    title: str,
    xLabel: str,
    yLabel: str,
    xData: list,
    yData: list,
    maximumDegree: int,
) -> Figure:
    figure: Figure = plt.figure()
    data: tuple = __findBestFitLine(
        x=xData,
        y=yData,
        maximumDegree=maximumDegree,
    )
    bfModel: np.poly1d = data[1]
    line: np.ndarray = np.linspace(0, max(xData), 100)
    plt.ylabel(ylabel=yLabel)
    plt.xlabel(xlabel=xLabel)
    plt.title(title)
    plt.plot(line, bfModel(line))
    plt.tight_layout()
    return figure


def _graphVelocity(
    title: str,
    xLabel: str,
    yLabel: str,
    xData: list,
    yData: list,
    maximumDegree: int,
) -> Figure:
    figure: Figure = plt.figure()
    data: tuple = __findBestFitLine(
        x=xData,
        y=yData,
        maximumDegree=maximumDegree,
    )
    bfModel: np.poly1d = data[1]
    velocityModel = np.polyder(p=bfModel, m=1)
    line: np.ndarray = np.linspace(0, max(xData), 100)
    plt.ylabel(ylabel=yLabel)
    plt.xlabel(xlabel=xLabel)
    plt.title(title)
    plt.plot(line, velocityModel(line))
    plt.tight_layout()
    return figure


def _graphAcceleration(
    title: str,
    xLabel: str,
    yLabel: str,
    xData: list,
    yData: list,
    maximumDegree: int,
) -> Figure:
    figure: Figure = plt.figure()
    data: tuple = __findBestFitLine(
        x=xData,
        y=yData,
        maximumDegree=maximumDegree,
    )
    bfModel: np.poly1d = data[1]
    accelerationModel = np.polyder(p=bfModel, m=2)
    line: np.ndarray = np.linspace(0, max(xData), 100)
    plt.ylabel(ylabel=yLabel)
    plt.xlabel(xlabel=xLabel)
    plt.title(title)
    plt.plot(line, accelerationModel(line))
    plt.tight_layout()
    return figure


def _graphAll(
    title: str,
    xLabel: str,
    yLabelList: list,
    xData: list,
    yData: list,
    maximumDegree: int,
    subplotTitles: list,
) -> Figure:
    figure: Figure = plt.figure()
    plt.suptitle(title)

    # Data
    plt.subplot(2, 2, 1)
    plt.xlabel(xlabel=xLabel)
    plt.ylabel(ylabel=yLabelList[0])
    plt.title(subplotTitles[0])
    plt.plot(xData, yData)
    plt.tight_layout()

    # Best Fit
    plt.subplot(2, 2, 2)
    data: tuple = __findBestFitLine(x=xData, y=yData, maximumDegree=maximumDegree)
    bfModel: np.poly1d = data[1]
    line: np.ndarray = np.linspace(0, max(xData), 100)
    plt.ylabel(ylabel=yLabelList[1])
    plt.xlabel(xlabel=xLabel)
    plt.title(subplotTitles[1])
    plt.plot(line, bfModel(line))
    plt.tight_layout()

    # Velocity
    plt.subplot(2, 2, 3)
    velocityModel = np.polyder(p=bfModel, m=1)
    line: np.ndarray = np.linspace(0, max(xData), 100)
    plt.ylabel(ylabel=yLabelList[2])
    plt.xlabel(xlabel=xLabel)
    plt.title(subplotTitles[2])
    plt.plot(line, velocityModel(line))
    plt.tight_layout()

    # Acceleration
    plt.subplot(2, 2, 4)
    accelerationModel = np.polyder(p=bfModel, m=2)
    line: np.ndarray = np.linspace(0, max(xData), 100)
    plt.ylabel(ylabel=yLabelList[3])
    plt.xlabel(xlabel=xLabel)
    plt.title(subplotTitles[3])
    plt.plot(line, accelerationModel(line))
    plt.tight_layout()

    return figure


def graphChart(
    figureType: str,
    title: str,
    xLabel: str,
    yLabel: str,
    xData: list,
    yData: list,
    filename: str,
    maximumDegree: int = None,
    subplotTitles: list = None,
    yLabelList: list = None,
) -> None:
    if figureType == "data":
        figure: Figure = _graphData(
            title=title,
            xLabel=xLabel,
            yLabel=yLabel,
            xData=xData,
            yData=yData,
        )
    if figureType == "best_fit":
        figure: Figure = _graphBestFit(
            title=title,
            xLabel=xLabel,
            yLabel=yLabel,
            xData=xData,
            yData=yData,
            maximumDegree=maximumDegree,
        )
    if figureType == "velocity":
        figure: Figure = _graphVelocity(
            title=title,
            xLabel=xLabel,
            yLabel=yLabel,
            xData=xData,
            yData=yData,
            maximumDegree=maximumDegree,
        )
    if figureType == "acceleration":
        figure: Figure = _graphAcceleration(
            title=title,
            xLabel=xLabel,
            yLabel=yLabel,
            xData=xData,
            yData=yData,
            maximumDegree=maximumDegree,
        )
    if figureType == "all":
        figure: Figure = _graphAll(
            title=title,
            xLabel=xLabel,
            xData=xData,
            yData=yData,
            maximumDegree=maximumDegree,
            subplotTitles=subplotTitles,
            yLabelList=yLabelList,
        )

    figure.savefig(filename)
    figure.clf()


def main() -> None:
    args: Namespace = getArgparse()

    if args.input[-5::] != ".json":
        print("Invalid input file type. Input file must be JSON")
        quit(1)
    if args.x_min < 0:
        print("Invalid x window min. X window min >= 0")
        quit(2)
    if args.maximum_polynomial_degree < 1:
        print(
            "The maximum degree polynomial is too small. Maximum degree polynomial >= 1"
        )
        quit(3)
    if args.stepper < 1:
        print("The stepper is too small. Stepper >= 1")
        quit(4)

    if (args.loc is False) and (args.dloc is False) and (args.kloc is False):
        print("No data source choosen. Defaulting to LOC")
        args.loc = True
    if (
        (args.graph_data is False)
        and (args.graph_best_fit is False)
        and (args.graph_velocity is False)
        and (args.args.graph_acceleration is False)
        and (args.args.graph_all is False)
    ):
        print("No graph choosen. Defaulting to graphing all figures on a single chart")
        args.graph_all = True

    xLabel: str = f"Every {args.stepper} Commit(s)"
    yLabel0: str = "{}"
    yLabel1: str = "d/dx {}"
    yLabel2: str = "d^2/dx^2 {}"

    df: DataFrame = pandas.read_json(args.input)

    if args.x_max <= -1:
        xData: list = [x for x in range(len(df["loc_sum"]))][
            args.x_min : -1 : args.stepper
        ]
        yLOC: list = df["loc_sum"].tolist()[args.x_min : -1 : args.stepper]
        yDLOC: list = df["delta_loc"].tolist()[args.x_min : -1 : args.stepper]
        yKLOC: list = df["kloc"].to_list()[args.x_min : -1 : args.stepper]
    else:
        xData: list = [x for x in range(len(df["loc_sum"]))][
            args.x_min : args.x_max + 1 : args.stepper
        ]
        yLOC: list = df["loc_sum"].tolist()[args.x_min : args.x_max + 1 : args.stepper]
        yDLOC: list = df["delta_loc"].tolist()[
            args.x_min : args.x_max + 1 : args.stepper
        ]
        yKLOC: list = df["kloc"].to_list()[args.x_min : args.x_max + 1 : args.stepper]

    if args.loc:
        title: str = "{}{} {} / (Every {} Commits)"
        if args.graph_data:
            filename: str = _appendID(filename=args.output, id="loc_data")
            title = title.format("", args.repository_name, "Lines of Code (LOC)", args.stepper)
            graphChart(
                figureType="data",
                title=title,
                xLabel=xLabel,
                yLabel=yLabel0.format("LOC"),
                xData=xData,
                yData=yLOC,
                filename=filename,
            )

        if args.graph_best_fit:
            filename: str = _appendID(filename=args.output, id="loc_best_fit")
            title = title.format("Best Fit of ", args.repository_name, "Lines of Code (LOC)", args.stepper)
            graphChart(
                figureType="best_fit",
                title=title,
                xLabel=xLabel,
                yLabel=yLabel0.format("LOC"),
                xData=xData,
                yData=yLOC,
                filename=filename,
                maximumDegree=args.maximum_polynomial_degree,
            )

        if args.graph_velocity:
            filename: str = _appendID(filename=args.output, id="loc_velocity")
            title = title.format("Velocity of ", args.repository_name, "Lines of Code (LOC)", args.stepper)
            graphChart(
                figureType="velocity",
                title=title,
                xLabel=xLabel,
                yLabel=yLabel1.format("LOC"),
                xData=xData,
                yData=yLOC,
                filename=filename,
                maximumDegree=args.maximum_polynomial_degree,
            )

        if args.graph_acceleration:
            filename: str = _appendID(filename=args.output, id="loc_acceleration")
            title = title.format("Acceleration of ", args.repository_name, "Lines of Code (LOC)", args.stepper)
            graphChart(
                figureType="acceleration",
                title=title,
                xLabel=xLabel,
                yLabel=yLabel2.format("LOC"),
                xData=xData,
                yData=yLOC,
                filename=filename,
                maximumDegree=args.maximum_polynomial_degree,
                subplotTitles=[],
            )

        if args.graph_all:
            filename: str = _appendID(filename=args.output, id="loc_all")
            title = title.format("", args.repository_name, "Lines of Code (LOC)", args.stepper)
            graphChart(
                figureType="all",
                title=title,
                xLabel=xLabel,
                yLabel=None,
                xData=xData,
                yData=yLOC,
                filename=filename,
                maximumDegree=args.maximum_polynomial_degree,
                subplotTitles=[
                    "Data",
                    "Best Fit",
                    "Velocity",
                    "Acceleration",
                ],
                yLabelList=[
                    yLabel0.format("LOC"),
                    yLabel0.format("LOC"),
                    yLabel1.format("LOC"),
                    yLabel2.format("LOC"),
                ],
            )

    if args.dloc:
        title: str = "{}{} {} / (Every {} Commits)"
        if args.graph_data:
            filename: str = _appendID(filename=args.output, id="dloc_data")
            title = title.format("", args.repository_name, "Delta Lines of Code (DLOC)", args.stepper)
            graphChart(
                figureType="data",
                title=title,
                xLabel=xLabel,
                yLabel=yLabel0.format("DLOC"),
                xData=xData,
                yData=yDLOC,
                filename=filename,
            )

        if args.graph_best_fit:
            filename: str = _appendID(filename=args.output, id="dloc_best_fit")
            title = title.format("Best Fit of ", args.repository_name, "Delta Lines of Code (DLOC)", args.stepper)
            graphChart(
                figureType="best_fit",
                title=title,
                xLabel=xLabel,
                yLabel=yLabel0.format("DLOC"),
                xData=xData,
                yData=yDLOC,
                filename=filename,
                maximumDegree=args.maximum_polynomial_degree,
            )

        if args.graph_velocity:
            filename: str = _appendID(filename=args.output, id="dloc_velocity")
            title = title.format("Velocity of ", args.repository_name, "Delta Lines of Code (DLOC)", args.stepper)
            graphChart(
                figureType="velocity",
                title=title,
                xLabel=xLabel,
                yLabel=yLabel1.format("DLOC"),
                xData=xData,
                yData=yDLOC,
                filename=filename,
                maximumDegree=args.maximum_polynomial_degree,
            )

        if args.graph_acceleration:
            filename: str = _appendID(filename=args.output, id="dloc_acceleration")
            title = title.format("Acceleration of ", args.repository_name, "Delta Lines of Code (DLOC)", args.stepper)
            graphChart(
                figureType="acceleration",
                title=title,
                xLabel=xLabel,
                yLabel=yLabel2.format("DLOC"),
                xData=xData,
                yData=yDLOC,
                filename=filename,
                maximumDegree=args.maximum_polynomial_degree,
                subplotTitles=[],
            )

        if args.graph_all:
            filename: str = _appendID(filename=args.output, id="dloc_all")
            title = title.format("", args.repository_name, "Delta Lines of Code (DLOC)", args.stepper)
            graphChart(
                figureType="all",
                title=title,
                xLabel=xLabel,
                yLabel=None,
                xData=xData,
                yData=yDLOC,
                filename=filename,
                maximumDegree=args.maximum_polynomial_degree,
                subplotTitles=[
                    "Data",
                    "Best Fit",
                    "Velocity",
                    "Acceleration",
                ],
                yLabelList=[
                    yLabel0.format("DLOC"),
                    yLabel0.format("DLOC"),
                    yLabel1.format("DLOC"),
                    yLabel2.format("DLOC"),
                ],
            )

    if args.kloc:
        title: str = "{}{} {} / (Every {} Commits)"
        if args.graph_data:
            filename: str = _appendID(filename=args.output, id="kloc_data")
            title = title.format("", args.repository_name, "Thousands of Lines of Code (KLOC)", args.stepper)
            graphChart(
                figureType="data",
                title=title,
                xLabel=xLabel,
                yLabel=yLabel0.format("KLOC"),
                xData=xData,
                yData=yKLOC,
                filename=filename,
            )

        if args.graph_best_fit:
            filename: str = _appendID(filename=args.output, id="kloc_best_fit")
            title = title.format("Best Fit of ", args.repository_name, "Thousands of Lines of Code (KLOC)", args.stepper)
            graphChart(
                figureType="best_fit",
                title=title,
                xLabel=xLabel,
                yLabel=yLabel0.format("KLOC"),
                xData=xData,
                yData=yKLOC,
                filename=filename,
                maximumDegree=args.maximum_polynomial_degree,
            )

        if args.graph_velocity:
            filename: str = _appendID(filename=args.output, id="kloc_velocity")
            title = title.format("Velocity of ", args.repository_name, "Thousands of Lines of Code (KLOC)", args.stepper)
            graphChart(
                figureType="velocity",
                title=title,
                xLabel=xLabel,
                yLabel=yLabel1.format("KLOC"),
                xData=xData,
                yData=yKLOC,
                filename=filename,
                maximumDegree=args.maximum_polynomial_degree,
            )

        if args.graph_acceleration:
            filename: str = _appendID(filename=args.output, id="kloc_acceleration")
            title = title.format("Acceleration of ", args.repository_name, "Thousands of Lines of Code (KLOC)", args.stepper)
            graphChart(
                figureType="acceleration",
                title=title,
                xLabel=xLabel,
                yLabel=yLabel2.format("KLOC"),
                xData=xData,
                yData=yKLOC,
                filename=filename,
                maximumDegree=args.maximum_polynomial_degree,
                subplotTitles=[],
            )

        if args.graph_all:
            filename: str = _appendID(filename=args.output, id="kloc_all")
            title = title.format("", args.repository_name, "Thousands of Lines of Code (KLOC)", args.stepper)
            graphChart(
                figureType="all",
                title=title,
                xLabel=xLabel,
                yLabel=None,
                xData=xData,
                yData=yKLOC,
                filename=filename,
                maximumDegree=args.maximum_polynomial_degree,
                subplotTitles=[
                    "Data",
                    "Best Fit",
                    "Velocity",
                    "Acceleration",
                ],
                yLabelList=[
                    yLabel0.format("KLOC"),
                    yLabel0.format("KLOC"),
                    yLabel1.format("KLOC"),
                    yLabel2.format("KLOC"),
                ],
            )

    dlocXLabel: str = 0
    dlocYLabel: str = "ΔLOC"
    dlocTitle: str = "Change of Lines of Code (ΔLOC) / Commits"

    klocXLabel: str = 0
    klocYLabel: str = "KLOC"
    klocTitle: str = "Thousands of Lines of Code (KLOC) / Commits"


if __name__ == "__main__":
    main()
