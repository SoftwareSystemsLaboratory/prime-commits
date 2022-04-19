from argparse import ArgumentParser, Namespace

name: str = "CLIME"
authors: list = ["Nicholas M. Synovic", "Matthew Hyatt", "George K. Thiruvathukal"]


def mainArgs() -> Namespace:
    parser: ArgumentParser = ArgumentParser(
        prog=f"{name} Git Commit LOC Exploder",
        description="A tool to extract all LOC information from a single branch of a Git repository on a per commit basis",
        epilog=f"Author(s): {', '.join(authors)}",
    )

    parser.add_argument(
        "-d",
        "--directory",
        help="Directory containg the .git folder of the repository to analyze",
        type=str,
        required=False,
        default=".",
    )
    parser.add_argument(
        "-b",
        "--branch",
        help="Branch of the Git repository to analyze. DEFAULT: HEAD",
        type=str,
        required=False,
        default="HEAD",
    )
    parser.add_argument(
        "-o",
        "--output",
        help="JSON file to store the data. DEFAULT: ./commits_loc.json",
        type=str,
        required=False,
        default="commits_loc.json",
    )
    parser.add_argument(
        "--cloc",
        help='TXT file containing cloc options. DEFAULT: ""',
        type=str,
        required=False,
        default="",
    )
    parser.add_argument(
        "--processes",
        help="Number of processes cloc should use. DEFAULT: 0",
        type=int,
        required=False,
        default=0,
    )
    parser.add_argument(
        "--log",
        help="Log file to store logging information to. DEFAULT: log.txt",
        type=str,
        required=False,
        default="log.log",
    )

    return parser.parse_args()


def graphArgs() -> Namespace:
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
        help='Filepath of matplotlib stylesheet to use. DEFAULT: ""',
        type=str,
        required=False,
        default="",
    )

    return parser.parse_args()
