from argparse import ArgumentParser, Namespace

import pandas
from matplotlib.figure import Figure
from pandas import DataFrame

from args import get_graph_args, check_args
from graph_util import Graph, graph_all, appendID


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

    xwindow = lambda maximum: [i for i in range(len(df["loc_sum"]))] [args.x_min : maximum : args.stepper]
    ywindow = lambda column, maximum: df[column].tolist()[args.x_min : maximum : args.stepper]

    # if the max window is less than 1, set it to -1 for all data
    y_vars = ["LOC", "KLOC", "DLOC"]
    columns = ["loc_sum", "kloc", "delta_loc"]
    # dataset = {k: v for k, v in zip(y_vars, [yLOC, yKLOC, yDLOC])}

    if args.x_max <= -1:
        xData: list = xwindow(-1)
        dataset = {k: ywindow(v, -1) for k, v in zip(y_vars, columns)}
    else:
        xData: list = xwindow(args.x_max + 1)
        dataset = {k: ywindow(v, args.x_max + 1) for k, v in zip(y_vars, columns)}

    # create graphs

    for arg, name in zip([args.loc, args.dloc, args.kloc], ["LOC", "KLOC", "DLOC"]):
        if arg:

            print(arg, name)
            jobs = ["data", "best_fit", "velocity", "acceleration", "all"]
            graph_type_args = [
                args.graph_data,
                args.graph_best_fit,
                args.graph_velocity,
                args.graph_acceleration,
                args.graph_all,
            ]

            print((graph_type_args,jobs))
            for arg2, job, i in zip(graph_type_args, jobs, [0, 1, 2, 3, 4]):

                print(arg2,job)
                if arg2:
                    print(arg2)

                    subtitles = [job.replace("_"," ").capitalize() for job in jobs[:-1]]
                    prefix = f"""{job.replace("_"," ").capitalize()+" of " if job not in ["data", "all"] else ""}"""
                    title = f"{prefix}{args.repository_name} {name} / {xlabel}"
                    filename = appendID(filename=args.output, id=f"{name.lower()}_{job}")

                    if job == "all":
                        named_ylabels = [f"{ylabels[j]} {name}" for j in [0, 1, 2, 3]]
                        graph_all(
                            title=title,
                            subtitles=subtitles,
                            xlabel=xlabel,
                            ylabels=named_ylabels,
                            x = xData,
                            y = dataset[name],
                            maxdeg = args.maximum_polynomial_degree,
                            filename=filename,

                        )
                        continue

                    # arg != all

                    ylabel = f"{ylabels[i]} {name}" # i should never be 4
                    g = Graph(
                        job=job,
                        x=xData,
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
