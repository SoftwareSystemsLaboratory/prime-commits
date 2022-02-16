from operator import itemgetter
from pathlib import Path
from textwrap import wrap

from matplotlib.figure import Figure
import matplotlib.pyplot as plt
import numpy as np
from sklearn.metrics import r2_score

def findBestFitLine(x: list, y: list, maximumDegree: int) -> tuple:
    # https://www.w3schools.com/Python/python_ml_polynomial_regression.asp
    data: list = []

    degree: int
    for degree in range(maximumDegree):
        model: np.poly1d = np.poly1d(np.polyfit(x, y, degree))
        r2Score: np.float64 = r2_score(y, model(x))
        temp: tuple = (r2Score, model)
        data.append(temp)

    return max(data, key=itemgetter(0))


def appendID(filename: str, id: str) -> str:
    # https://stackoverflow.com/a/37487898
    p = Path(filename)
    return f"{Path.joinpath(p.parent, p.stem)}_{id}{p.suffix}"


class Graph:
    def __init__(
        self, *, job="data", x, y, title, xlabel, ylabel, maxdeg=None, filename
    ):

        self.x = x
        self.y = y
        self.maxdeg = maxdeg

        self.title = title
        self.xlabel = xlabel
        self.ylabel = ylabel
        self.filename = filename

        # for multiple graphs in future
        self.jobs = ["data", "velocity", "acceleration", "best_fit", "all"]
        self.jobs = {k: int(job in k) for k in self.jobs}
        self.job = job

    def build(self, *, save=False):
        "builds an axes"

        # https://towardsdatascience.com/clearing-the-confusion-once-and-for-all-fig-ax-plt-subplots-b122bb7783ca

        # if job == "all":
        # fig, axs = subplots(2,2)
        # axs[0].plot()
        # axs[1].plot()

        fig, ax = plt.subplots()
        ax.set(xlabel=self.xlabel, ylabel=self.ylabel, title="\n".join(wrap(self.title, width=60)))

        if type(self.maxdeg) is int:
            data: tuple = findBestFitLine(x=self.x, y=self.y, maximumDegree=self.maxdeg)
            bfModel: np.poly1d = data[1]
            line: np.ndarray = np.linspace(0, max(self.x), 100)

        if self.job == "best_fit":
            ax.plot(line, bfModel(line))

        if self.job == "velocity":
            velocityModel = np.polyder(p=bfModel, m=1)
            ax.plot(line, velocityModel(line))

        if self.job == "acceleration":
            accelerationModel = np.polyder(p=bfModel, m=2)
            ax.plot(line, accelerationModel(line))

        if self.job == "data":
            ax.plot(self.x, self.y)

        fig.tight_layout()
        if save:
            fig.savefig(self.filename)

        return fig, ax
