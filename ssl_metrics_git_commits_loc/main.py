from argparse import ArgumentParser
from concurrent.futures import ProcessPoolExecutor
from datetime import datetime
from functools import reduce
import itertools
from itertools import repeat
import json
import os
from os.path import exists, join
import time
from tqdm import tqdm

from dateutil.parser import parse as dateParse


def get_argparse() -> ArgumentParser:
    parser: ArgumentParser = ArgumentParser(
        prog="SSL Metrics Git Commits LOC Extraction Utility",
        usage="Extraction utility to extract statistics from git commits",
        description="This prgram takes in a git repository and generates a JSON file of statistics derived from git commits",
        epilog="This utility was developed by Nicholas M. Synovic and George K. Thiruvathukal",
    )
    parser.add_argument(
        "-d",
        "--directory",
        help="Directory containing repository root folder (.git)",
        default=".",
        type=str,
        required=True,
    )
    parser.add_argument(
        "-b",
        "--branch",
        help="Git branch for analysis to be ran on",
        default="main",
        type=str,
        required=True,
    )
    parser.add_argument(
        "-o",
        "--output",
        help="Output analysis to a JSON file",
        type=str,
        required=True,
    )
    # parser.add_argument(
    #     "-c",
    #     "--cores",
    #     help="Number of cores to use for analysis",
    #     type=int,
    #     required=False,
    #     default=1,
    # )
    return parser


def repoExists(directory: str = ".") -> bool:
    return exists(join(directory, ".git"))


def parseCommitLineFromLog(line: str) -> dict:

    name, email, hash, *_, date = line.split(";")

    return {
        "author_name": name,
        "author_email": email,
        "hash": hash,
        "date": dateParse(date),
    }


def analyze_commit(commits, i, date0):
    '''return a dict of commit info in parallel'''

    hashX: str = commits[i]["hash"]
    hashY: str = commits[i + 1]["hash"]

    dateY: datetime = commits[i + 1]["date"]
    commit_day = (dateY - date0).days

    gdf: dict = gitDiffTree(hashX, hashY)
    loc = map(lambda info: info["loc"], gdf)
    delta_sum = reduce(lambda x, y: x + y, loc, 0)

    result = {
        "commit_number": i,
        "author_name": commits[i]["author_name"],
        "author_email": commits[i]["author_email"],
        "hash": hashY,
        "delta_loc": delta_sum,
        # "kloc": float(loc_sum / 1000),
        "commit_date": commits[i]["date"].strftime("%m/%d/%Y"),
        "days_since_0": commit_day,
    }

    return result


def gitDiffTree(hashX: str, hashY: str) -> dict:
    # git diff help page: https://www.git-scm.com/docs/git-diff
    with os.popen(f"git diff-tree -r {hashX} {hashY}") as diffTreePipe:
        for line in diffTreePipe:

            lineInfo: dict = parseDiffTreeLine(line)
            lineStatus: str = lineInfo.get("status")

            if lineStatus == "A":
                addLines(lineInfo)
            elif lineStatus == "D":
                deleteLines(lineInfo)
            elif lineStatus == "M":
                deltaLines(lineInfo)
            else:
                continue
            yield lineInfo


def parseDiffTreeLine(line: str) -> dict:

    tokens: list = line.split()
    try:
        (dstMode, sha1Src, sha1Dst, status, srcPath) = tokens[1:6]
    except ValueError:
        return {}
    return {
        "dstMode": dstMode,
        "sha1Src": sha1Src,
        "sha1Dst": sha1Dst,
        "status": status,
        "srcPath": srcPath,
    }


def addLines(line: dict) -> None:
    line["loc"] = countFileLines(line["sha1Dst"])


def deleteLines(line: dict) -> None:
    line["loc"] = -countFileLines(line["sha1Src"])


def deltaLines(line: dict) -> None:
    loc_before = countFileLines(line["sha1Src"])
    loc_after = countFileLines(line["sha1Dst"])
    line["loc"] = loc_after - loc_before


# TODO: Could replace this with cloc; make parametric
def countFileLines(blobHash: str):
    # Git show help page: https://www.git-scm.com/docs/git-show
    # wc help page: https://linux.die.net/man/1/wc
    with os.popen(f"git show {blobHash} | wc -l") as data:
        return int(data.read().split()[0])
    return -1


def exportJSON(filename, commitInfo):

    with open(filename, "w") as jsonf:
        json.dump(commitInfo, jsonf, indent=4)


'''TODO: remove ... if not used'''
# def pairwise(iterable, coreCount: int, maxValue: int) -> list:
#
#     data: list = []
#     a, b = itertools.tee(iterable)
#     next(b, None)
#
#     data = [[x+1 if x else x, y] for x, y in zip(a, b)]
#
#     if len(data) < coreCount:
#         data.append([data[-1][1] + 1, maxValue])
#
#     if data[-1][1] != maxValue:
#         data[-1][1] = maxValue
#
#     return data


def generate_loc_sum(commit, loc_sum):
    '''generate loc_sum from list in parallel'''

    commit['loc_sum'] = loc_sum
    commit['kloc'] = loc_sum / 1000

    return commit


def main() -> bool:

    pwd = os.getcwd()
    args = get_argparse().parse_args()

    if not repoExists(directory=args.directory):
        return False

    os.chdir(args.directory)

    start = time.perf_counter()

    # Git log help page: https://www.git-scm.com/docs/git-log
    with os.popen(r'git log --reverse --pretty=format:"%an;%ae;%H;%ci"') as gitLogPipe:

        commits = [commit for commit in gitLogPipe]

        with ProcessPoolExecutor() as executor:

            commits = list(executor.map(parseCommitLineFromLog, commits))
            root = [
                {
                    "author_name": commits[0]["author_name"],
                    "author_email": commits[0]["author_email"],
                    "hash": "--root",
                    "date": commits[0]["date"],
                }
            ]

            commits = root + commits

            date0 = commits[0]["date"]

            commits = list(tqdm(executor.map(analyze_commit, repeat(commits), [
                i for i in range(len(commits)-1)], repeat(date0)), total=len(commits)-1))

            loc_sums = [0]
            for commit in commits:
                loc_sums.append(commit['delta_loc'] + loc_sums[-1])
            loc_sums = loc_sums[1:]

            commits = list(executor.map(generate_loc_sum, commits, loc_sums))

    os.chdir(pwd)
    exportJSON(args.output, commits)

    stop = time.perf_counter()
    print(f'Finished in: {round(stop-start, 2)} sec(s)')

    return True


if __name__ == "__main__":
    main()
