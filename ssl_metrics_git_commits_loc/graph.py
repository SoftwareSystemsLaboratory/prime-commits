import pandas
from pandas import DataFrame, Series

def computeXY(data: DataFrame, yKey:str, xKey: str = "author_days_since_0", xStepper: int = 1)   ->  tuple:
    x: set = set(data[xKey].tolist())
    print(x)

def main()  ->  None:
    df: DataFrame = pandas.read_json('commit_loc.json')
    df = df.T
    computeXY(data=df, xKey="author_day_since_0", yKey="")

if __name__ == "__main__":
    main()
