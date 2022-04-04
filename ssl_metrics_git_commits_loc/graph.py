from signal import pause
import matplotlib.pyplot as plt
import pandas
from pandas import DataFrame


def computeXY(
    df: DataFrame,
    yKey: str,
    xKey: str = "author_days_since_0",
    yThousandth: bool = False,
) -> tuple:
    xData: set = df[xKey].unique().tolist()
    yData: list = []
    day: int

    if yThousandth:
        for day in xData:
            yData.append(df.loc[df[xKey] == day, yKey].sum() / 1000)
    else:
        for day in xData:
            print(df.loc[df[xKey] == day, yKey])
            input()


            yData.append(df.loc[df[xKey] == day, yKey].sum())
    return (xData, yData)


def plot(
    x: list,
    y: list,
    type: str = "line",
    xLabel: str = "",
    yLabel: str = "",
    title: str = "",
    output: str = "commits_loc.pdf",
    stylesheet: str = "style.mplstyle"
) -> None:
    "param: type can only be one of the following: line, bar"

    plt.style.use(stylesheet)

    if type == "line":
        plt.plot(x, y)
    elif type == "bar":
        plt.bar(x, height=y)
    else:
        print(f"Invalid plot type: {type}")

    plt.title(title)
    plt.xlabel(xLabel)
    plt.ylabel(yLabel)

    plt.savefig(output, bbox_inches='tight', transparent="True", pad_inches=0)


def main() -> None:
    df: DataFrame = pandas.read_json("commits_loc.json")
    df = df.T
    data: tuple = computeXY(df=df, yKey="added_lines_of_code", yThousandth=False)
    plot(x=data[0], y=data[1], type="bar", title="TEST")


if __name__ == "__main__":
    main()
