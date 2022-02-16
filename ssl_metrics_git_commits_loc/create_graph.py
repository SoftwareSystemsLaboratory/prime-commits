from argparse import ArgumentParser, Namespace

import pandas
from matplotlib.figure import Figure
from pandas import DataFrame

from args import get_graph_args, check_args
from graph_util import Graph, appendID


def main() -> None:

    # get args, check, proceed
    args: Namespace = get_graph_args()
    check_args(args)

    # labels
    xlabel = f"Every {args.stepper} Commits"
    ylabels = ["", "", "d/dx", "d^2/dx^2"]

    # read input
    df: DataFrame = pandas.read_json(args.input)

    ## windows
    xwindow = lambda maximum: [i for i in range(len(df["loc_sum"]))][
        args.x_min : maximum : args.stepper
    ]
    ywindow = lambda column, maximum: df[column].tolist()[
        args.x_min : maximum : args.stepper
    ]

    y_vars = ["LOC", "KLOC", "DLOC"]
    columns = ["loc_sum", "kloc", "delta_loc"]

    if args.x_max <= -1:
        x: list = xwindow(-1)
        dataset = {k: ywindow(v, -1) for k, v in zip(y_vars, columns)}
    else:
        x: list = xwindow(args.x_max + 1)
        dataset = {k: ywindow(v, args.x_max + 1) for k, v in zip(y_vars, columns)}

    # create graphs

    for arg, name in zip([args.loc, args.kloc, args.dloc], ["LOC", "KLOC", "DLOC"]):
        if arg:

            jobs = ["data", "best_fit", "velocity", "acceleration"]
            graph_types = [args.data, args.best_fit, args.velocity, args.acceleration]

            for arg2, job, i in zip(graph_types, jobs, [0, 1, 2, 3]):

                if arg2:

                    subtitles = [job.replace("_", " ").capitalize() for job in jobs]
                    prefix = f"""{job.replace("_"," ").capitalize()+" of " if job not in ["data", "all"] else ""}"""
                    title = f"{prefix}{args.repository_name} {name} / {xlabel}"
                    filename = appendID(
                        filename=args.output, id=f"{name.lower()}_{job}"
                    )

                    ylabel = f"{ylabels[i]} {name}"  # i should never be 4
                    g = Graph(
                        job=job,
                        x=x,
                        y=dataset[name],
                        title=title,
                        xlabel=xlabel,
                        ylabel=ylabel,
                        maxdeg=args.maximum_polynomial_degree,
                        filename=filename,
                    )
                    g.build(save=True)


if __name__ == "__main__":
    main()
