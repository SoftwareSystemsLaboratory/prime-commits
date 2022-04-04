import matplotlib.pyplot as plt
import pandas
from pandas import DataFrame


def computeXY(
    df: DataFrame, yKey: str, xKey: str = "author_days_since_0", xStepper: int = 1
) -> tuple:
    xData: set = df[xKey].unique().tolist()
    yData: list = []
    day: int
    for day in xData:
        yData.append(df.loc[df[xKey] == day, yKey].sum())
    return (xData, yData)


def plot(
    x: list,
    y: list,
    type: str = "line",
    xAxis: str = "",
    yAxis: str = "",
    title: str = "",
    output: str = "commits_loc.pdf",
) -> None:
    "type can only be one of the following: line, bar"

    if type == "line":
        plt.plot(x, y)
    elif type == "bar":
        plt.bar(x, height=y)
    else:
        print(f"Invalid plot type: {type}")
    plt.savefig(output)


def main() -> None:
    df: DataFrame = pandas.read_json("commit_loc.json")
    df = df.T
    data: tuple = computeXY(df=df, yKey="added_lines_of_code")
    plot(x=data[0], y=data[1], type="bar")


if __name__ == "__main__":
    main()
