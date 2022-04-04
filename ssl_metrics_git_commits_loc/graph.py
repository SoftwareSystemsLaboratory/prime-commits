import pandas
from pandas import DataFrame
import matplotlib.pyplot as plt

def computeXY(df: DataFrame, yKey:str, xKey: str = "author_days_since_0", xStepper: int = 1)   ->  tuple:
    xData: set = df[xKey].unique().tolist()
    yData: list = []
    day: int
    for day in xData:
        yData.append(df.loc[df[xKey] == day, yKey].sum())
    return((xData, yData))

def plot(x: list, y: list, xAxis: str = "", yAxis: str = "", title: str = "", output: str = "commits_loc.pdf") ->  None:
    plt.plot(x, y)
    plt.savefig(output)

def main()  ->  None:
    df: DataFrame = pandas.read_json('commit_loc.json')
    df = df.T
    data: tuple = computeXY(df=df, yKey="added_lines_of_code")
    plot(x=data[0], y=data[1])

if __name__ == "__main__":
    main()
