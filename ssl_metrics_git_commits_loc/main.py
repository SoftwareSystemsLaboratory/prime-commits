import json
import os
from argparse import ArgumentParser
from datetime import datetime
from functools import reduce
from os.path import exists, join

from dateutil.parser import parse as dateParse
from progress.bar import IncrementalBar


# Command line arguement parsing
def get_argparse() -> ArgumentParser:
    parser: ArgumentParser = ArgumentParser(
        prog="ssl-metrics-git-commits-loc",
        usage="This program outputs the lines of code (LOC) per commit and the delta LOC of a Git repository in JSON format.",
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
        help="Default branch for analysis to be ran on",
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
    return parser


# Checks if a Git repo exists at a given directory
def repoExists(directory: str = ".") -> bool:
    if exists(join(directory, ".git")) is False:
        return False
    return True


# Returns dict{str, datetime}
def parseCommitLineFromLog(line: str) -> dict:
    splitLine: list = line.split(";")
    name: str = splitLine[0]
    email: str = splitLine[1]
    hash: str = splitLine[2]
    date = splitLine[-1]
    return {
        "author_name": name,
        "author_email": email,
        "hash": hash,
        "date": dateParse(date),
    }


# Conducts the LOC and delta LOC analysis of a repository branch
def analyzeCommits(commits: list, date0: datetime):
    loc_sum: int = 0  # TODO: Rename this variable
    commitCounter: int = 0
    with IncrementalBar("Processing commits... ", max=len(commits) - 1) as ib:
        for index in range(len(commits) - 1):
            authorName: str = commits[index]["author_name"]
            authorEmail: str = commits[index]["author_email"]
            hashX: str = commits[index]["hash"]
            hashY: str = commits[index + 1]["hash"]
            commitDate: str = commits[index]["date"].strftime("%m/%d/%Y")
            dateY: datetime = commits[index + 1]["date"]

            gdf: dict = gitDiffTree(hashX, hashY)

            # Get the LOC from Git diff tree line
            loc = map(lambda info: info["loc"], gdf)

            delta_sum = reduce(lambda x, y: x + y, loc, 0)

            loc_sum += delta_sum
            commit_day = (dateY - date0).days
            result = {
                "commit_number": commitCounter,
                "author_name": authorName,
                "author_email": authorEmail,
                "hash": hashY,
                "delta_loc": delta_sum,
                "loc_sum": loc_sum,
                "kloc": float(loc_sum / 1000),
                "commit_date": commitDate,
                "day_since_0": commit_day,
            }

            commitCounter += 1
            ib.next()
            yield result


# Generate individual lines of a Git diff tree between two commits
def gitDiffTree(hashX: str, hashY: str) -> dict:
    # Git diff help page: https://www.git-scm.com/docs/git-diff
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
                continue  # Does not yield lineInfo
            yield lineInfo


# Parse pipe line into a dictionary of values
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


# Used for add status
def addLines(line: dict) -> None:
    line["loc"] = countFileLines(line["sha1Dst"])


# Used for delete status
def deleteLines(line: dict) -> None:
    line["loc"] = -countFileLines(line["sha1Src"])


# Used for modification status
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


# Script to execute program
def main() -> bool:
    # Setup variables
    pwd = os.getcwd()
    args = get_argparse().parse_args()

    # Test if directory is a Git repo
    # If True, change directory to Git repo and checkout specified branch
    if repoExists(directory=args.directory) is False:
        return False
    os.chdir(args.directory)
    os.system(f"git checkout {args.branch}")

    # Get list of commits from starting from the first commit of the repository
    # Git log help page: https://www.git-scm.com/docs/git-log
    with os.popen(r'git log --reverse --pretty=format:"%an;%ae;%H;%ci"') as gitLogPipe:
        commits: list = [parseCommitLineFromLog(line=commit) for commit in gitLogPipe]

        # Hack to get the first commit into the commits list
        commit0AuthorName: str = commits[0]["author_name"]
        commit0AuthorEmail: str = commits[0]["author_email"]
        commit0Date: datetime = commits[0]["date"]
        commits = [
            {
                "author_name": commit0AuthorName,
                "author_email": commit0AuthorEmail,
                "hash": "--root",
                "date": commit0Date,
            }
        ] + commits

        commit_info_iter = analyzeCommits(commits=commits, date0=commits[0]["date"])
        commit_info = list(commit_info_iter)
        delta_loc_iter = map(lambda info: info["delta_loc"], commit_info)
        loc_sum = reduce(lambda x, y: x + y, delta_loc_iter, 0)

    if args.output:
        exportJSON(join(pwd, args.output), commit_info)

    os.chdir(pwd)
    return True


if __name__ == "__main__":
    main()
