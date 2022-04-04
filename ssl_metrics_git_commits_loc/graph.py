from argparse import ArgumentParser, Namespace
import matplotlib.pyplot as plt
import pandas
from pandas import DataFrame

def getArgs()   ->  Namespace:
    name: str = "CLIME"
    authors: list = ["Nicholas M. Synovic"]
    parser: ArgumentParser = ArgumentParser(
        prog=f"{name} Git Commit LOC Exploder Grapher",
        description=f"A tool for graphing LOC information from the output of the {name} Commit LOC Exploder",
        epilog=f"Author(s): {', '.join(authors)}",
    )

    parser.add_argument(
        "-i",
        "--input",
        help=f"JSON export from {name} Git Commit Exploder. DEFAULT: ./commits_loc.json",
        type=str,
        required=False,
        default="commits_loc.json",
    )
    parser.add_argument(
        "-o",
        "--output",
        help="Filename of the graph. DEFAULT: ./commits_loc.pdf",
        type=str,
        required=False,
        default="commits_loc.pdf",
    )
    parser.add_argument(
        "-x",
        help="Key of the x values to use for graphing. DEFAULT: author_days_since_0",
        type=str,
        required=False,
        default="author_days_since_0",
    )
    parser.add_argument(
        "-y",
        help="Key of the y values to use for graphing. DEFAULT: lines_of_code",
        type=str,
        required=False,
        default="lines_of_code",
    )
    parser.add_argument(
        "--y-thousandths",
        help="Flag to divide the y values by 1000",
        action="store_true",
        required=False,
        default=False,
    )
    parser.add_argument(
        "--type",
        help="Type of figure to plot. DEFAULT: line",
        type=str,
        required=False,
        default="line",
    )
    parser.add_argument(
        "--title",
        help='Title of the figure. DEFAULT: ""',
        type=str,
        required=False,
        default="",
    )
    parser.add_argument(
        "--x-label",
        help='X axis label of the figure. DEFAULT: ""',
        type=str,
        required=False,
        default="",
    )
    parser.add_argument(
        "--y-label",
        help='Y axis label of the figure. DEFAULT: ""',
        type=str,
        required=False,
        default="",
    )
    parser.add_argument(
        "--stylesheet",
        help="Filepath of matplotlib stylesheet to use. DEFAULT: style.mplstyle. NOTE: This is an internal stylesheet used by the program and doesn't need to be specified/ created by you the user (you)",
        type=str,
        required=False,
        default="style.mplstyle",
    )

    return parser.parse_args()

def computeXY(
    df: DataFrame,
    yKey: str,
    xKey: str,
    yThousandth: bool,
) -> tuple:
    xData: set = df[xKey].unique().tolist()
    yData: list = []
    day: int

    if yThousandth:
        for day in xData:
            yData.append(df.loc[df[xKey] == day, yKey].sum() / 1000)
    else:
        for day in xData:
            yData.append(df.loc[df[xKey] == day, yKey].sum())
    return (xData, yData)


def plot(
    x: list,
    y: list,
    type: str,
    title: str,
    xLabel: str,
    yLabel: str,
    output: str,
    stylesheet: str,
) -> None:
    "param: type can only be one of the following: line, bar"

    plt.style.use(stylesheet)

    if type == "line":
        plt.plot(x, y)
    elif type == "bar":
        plt.bar(x, height=y)
    else:
        print(f"Invalid plot type: {type}. Can only be one of the following: line, bar")

    plt.title(title)
    plt.xlabel(xLabel)
    plt.ylabel(yLabel)

    plt.savefig(output)


def main() -> None:
    args: Namespace = getArgs()

    df: DataFrame = pandas.read_json(args.input)
    df = df.T
    data: tuple = computeXY(df=df, yKey="added_lines_of_code", yThousandth=True)
    plot(x=data[0], y=data[1], type="bar", title="TEST")


if __name__ == "__main__":
    main()
