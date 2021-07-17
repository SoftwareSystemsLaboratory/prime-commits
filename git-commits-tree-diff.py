import json
import os

from os.path import join, exists
from functools import reduce
from argparse import ArgumentParser

from dateutil.parser import parse as dateParse
from datetime import datetime

# Command line arguement parsing
def get_argparse() -> ArgumentParser:
    parser: ArgumentParser = ArgumentParser(
        prog="Git All Python (CLI Only)",
        usage="This program outputs the lines of code (LOC) per commit and the delta LOC of a Git repository in JSON format.",
    )
    parser.add_argument(
        "-d",
        "--directory",
        help="Directory containing repository root folder (.git)",
        default=".",
        type=str,
        required=False,
    )
    parser.add_argument(
        "-b",
        "--branch",
        help="Default branch for analysis to be ran on",
        default="main",
        type=str,
        required=False,
    )
    parser.add_argument(
        "-s",
        "--save-json",
        help="Save analysis to JSON file (EX: --save-json=output.json)",
        default=True,
        type=str,
        required=False,
    )
    return parser


# Checks if a Git repo exists at a given directory
def repoExists(directory: str = ".") -> bool:
    if exists(join(directory, ".git")) is False:
        return False
    return True


# Returns dict{str, datetime}
def parseCommitLineFromLog(line: str) -> dict:
    (hash, date) = line.split(";")[:2]
    return {"hash": hash, "date": dateParse(date)}


# Script to execute program
def go() -> bool:
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
    with os.popen(r'git log --reverse --pretty=format:"%H;%ci"') as gitLogPipe:
        commits: list = [parseCommitLineFromLog(line=commit) for commit in gitLogPipe]

        # Hack to get the first commit into the commits list
        commit0Date: datetime = commits[0]["date"]
        commits = [{"hash": "--root", "date": commit0Date}] + commits

        commit_info_iter = process_commits(commits=commits, date0=commits[0]["date"])
        commit_info = list(commit_info_iter)
        delta_loc_iter = map(lambda info: info["delta_loc"], commit_info)
        loc_sum = reduce(lambda x, y: x + y, delta_loc_iter, 0)

    if args.save_json:
        write_json_file(args.save_json, commit_info)

    kloc_sum = loc_sum / 1000.0
    os.chdir(pwd)
    return True


def process_commits(commits: list, date0: datetime):
    totalLOC: int = 0  # TODO: Rename this variable

    for index in range(len(commits) - 1):
        hashX: str = commits[index]["hash"]
        hashY: str = commits[index + 1]["hash"]
        dateY: datetime = commits[index + 1]["date"]

        g = git_diff_tree(hashX, hashY)
        loc_iter = map(lambda info: info["loc"], g)
        delta_sum = reduce(lambda x, y: x + y, loc_iter, 0)
        totalLOC += delta_sum
        commit_day = (dateY - date0).days
        result = {
            "hash": hashY,
            "delta_loc": delta_sum,
            "loc_sum": totalLOC,
            "day": commit_day,
        }
        yield result


def git_diff_tree(hashX: str, hashY: str) -> dict:
    # Git diff help page: https://www.git-scm.com/docs/git-diff
    with os.popen(f"git diff-tree -r {hashX} {hashY}") as diffTreePipe:
        for line in diffTreePipe:

            lineInfo: dict = parseDiffTreeLine(line)
            lineStatus: str = lineInfo.get("status")
            if lineStatus == "A":
                process_add(lineInfo)
            elif lineStatus == "D":
                process_delete(lineInfo)
            elif lineStatus == "M":
                process_merge(lineInfo)
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


def write_json_file(json_file, commit_info):
    with open(json_file, "w") as jsonf:
        json.dump(commit_info, jsonf, indent=3)


def process_add(info):
    info["loc"] = wc_lines(info["h2"])


def process_delete(info):
    info["loc"] = -wc_lines(info["h1"])


def process_merge(info):
    loc_before = wc_lines(info["h1"])
    loc_after = wc_lines(info["h2"])
    info["loc"] = loc_after - loc_before


# TODO: Could replace this with cloc; make parametric
def wc_lines(blob_hash):
    command = "git show %(blob_hash)s | wc -l" % vars()
    with os.popen(command) as inf:
        command_output = inf.read()
        return int(command_output.split()[0])
    return -1


if __name__ == "__main__":
    go()
