"handles arguments recieved by create_graph.py"

from argparse import ArgumentParser, Namespace


def get_graph_args() -> Namespace:
    """
    returns arguments for create_graph.py
    """
    
    authors = ["Nicholas M. Synovic", "Matthew Hyatt"]
    parser: ArgumentParser = ArgumentParser(
        prog="SSL Metrics Git Commits LOC Graphing Utility",
        usage="Graphing utility to visualize statistics from the SSL Metrics Git Commits LOC Extraction Utility",
        description="This prgram takes in a JSON file of values extracted from a git repository with ssl-metrics-git-commits-loc and generates graph based off of that information",
        epilog=f"This utility was developed by {', '.join(authors)}",
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
        "--data",
        help="Graph the raw data. Discrete graph of the data",
        required=False,
        action="store_true",
    )
    parser.add_argument(
        "--best-fit",
        help="Graph the best fit polynomial of the data. Continous graph of the data. Polynomial degrees can be configured with `-m`",
        required=False,
        action="store_true",
    )
    parser.add_argument(
        "--velocity",
        help="Graph the velocity of the data. Computes the best fit polynomial and takes the first derivitve. Polynomial degrees can be configured with `-m`",
        required=False,
        action="store_true",
    )
    parser.add_argument(
        "--acceleration",
        help="Graph the acceleration of the data. Computes the best fit polynomial and takes the second derivitve. Polynomial degrees can be configured with `-m`",
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


def check_args(args):
    """
    ensures that arguments are formatted properly
    else quit
    """

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

    if not any([args.loc, args.dloc, args.kloc]):
        print("No data option choosen. Defaulting to --loc")
        args.loc = True

    if not any([args.data, args.best_fit, args.velocity, args.acceleration]):
        print("No graph option choosen. Defaulting to --data")
        args.data = True
