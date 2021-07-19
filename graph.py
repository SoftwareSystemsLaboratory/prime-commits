from argparse import ArgumentParser, Namespace

import matplotlib.pyplot as plt


def get_argparse() -> ArgumentParser:
    parser: ArgumentParser = ArgumentParser(
        prog="Convert Output",
        usage="This program converts a JSON file into various different formats.",
    )
    parser.add_argument(
        "-i",
        "--input",
        help="The input data file that will be read to create the graphs",
        type=str,
        required=True,
    )
    return parser


def helloworld():
    fig = plt.figure()
    plt.plot([1, 2, 3, 4], [1, 4, 2, 3])
    fig.savefig("test.png")

if __name__ == "__main__":
    args: Namespace = get_argparse().parse_args()
