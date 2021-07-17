import json
import os

from os.path import join, exists
from functools import reduce
from argparse import ArgumentParser

from dateutil.parser import parse as dateParse


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


def repoExists(directory: str = ".") -> bool:
    if exists(join(directory, ".git")) is False:
        return False
    return True


def parseCommitLineFromLog(line: str) -> dict:
    (hash, date) = line.split(";")[:2]
    return {"hash": hash, "date": dateParse(date)}


def go() -> bool:
    # Setup variables
    pwd = os.getcwd()
    args = get_argparse().parse_args()
    repoDirectory = args.directory

    # Test if directory is a Git repo
    # If True, change directory to Git repo
    if repoExists(directory=repoDirectory) is False:
        return False
    os.chdir(repoDirectory)

    # Checkout specified branch in a subshell
    os.system(f"git checkout {args.branch}")

    # Get list of commits from starting from the first commit of the repository
    # Git log help page: https://www.git-scm.com/docs/git-log
    with os.popen(r'git log --reverse --pretty=format:"%H;%ci"') as gitLogPipe:
        commits = [parseCommitLineFromLog(line=commit) for commit in gitLogPipe]

        commit_info_iter = process_commits(commits)
        commit_info = list(commit_info_iter)
        delta_loc_iter = map(lambda info: info["delta_loc"], commit_info)
        loc_sum = reduce(lambda x, y: x + y, delta_loc_iter, 0)

    if args.save_json:
        write_json_file(args.save_json, commit_info)

    kloc_sum = loc_sum / 1000.0
    os.chdir(pwd)
    return True


def write_json_file(json_file, commit_info):
    with open(json_file, "w") as jsonf:
        json.dump(commit_info, jsonf, indent=3)


def process_commits(git_commits):
    # I know this is ugly but "root" does not have a hash and is a special case in git diff-tree
    day0 = git_commits[0]["date"]
    commits = [{"hash": "--root", "date": day0}] + git_commits
    loc_sum = 0
    for i in range(0, len(commits) - 1):
        hashX = commits[i]["hash"]
        hashY = commits[i + 1]["hash"]
        dateY = commits[i + 1]["date"]
        g = git_diff_tree(hashX, hashY)
        loc_iter = map(lambda info: info["loc"], g)
        delta_sum = reduce(lambda x, y: x + y, loc_iter, 0)
        loc_sum += delta_sum
        commit_day = (dateY - day0).days
        result = {
            "hash": hashY,
            "delta_loc": delta_sum,
            "loc_sum": loc_sum,
            "day": commit_day,
        }
        yield result


def git_diff_tree(hashX, hashY):
    command = "git diff-tree -r %(hashX)s %(hashY)s" % vars()
    delta_loc = 0
    with os.popen(command) as inf:
        for line in inf:
            info = parse_diff_tree_output(line)
            operation = info.get("operation", None)
            if operation == "A":
                process_add(info)
            elif operation == "D":
                process_delete(info)
            elif operation == "M":
                process_merge(info)
            else:
                continue
            delta_loc += info["loc"]
            yield info


def process_add(info):
    info["loc"] = wc_lines(info["h2"])


def process_delete(info):
    info["loc"] = -wc_lines(info["h1"])


def process_merge(info):
    loc_before = wc_lines(info["h1"])
    loc_after = wc_lines(info["h2"])
    info["loc"] = loc_after - loc_before


def parse_diff_tree_output(line):
    tokens = line.split()
    try:
        (dummy1, mode, h1, h2, operation, path) = tokens[:6]
        return {"mode": mode, "h1": h1, "h2": h2, "path": path, "operation": operation}
    except:
        return {}


# TODO: Could replace this with cloc; make parametric


def wc_lines(blob_hash):
    command = "git show %(blob_hash)s | wc -l" % vars()
    with os.popen(command) as inf:
        command_output = inf.read()
        return int(command_output.split()[0])
    return -1


if __name__ == "__main__":
    go()
