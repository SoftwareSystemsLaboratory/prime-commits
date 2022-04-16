import json
import os
from argparse import Namespace
from datetime import datetime
from os.path import exists, join

import pandas
from dateutil.parser import parse as dateParse
from pandas import DataFrame
from progress.bar import Bar

from ssl_metrics_git_commits_loc.args import mainArgs


def repoExists(directory: str = ".") -> bool:
    return exists(join(directory, ".git"))


def gitCommits() -> list:
    with os.popen(r'git log --reverse --pretty=format:"%H"') as commits:
        return [commit.strip() for commit in commits]


def commitMetadata(commit: str) -> list:
    info: os._wrap_close
    with os.popen(
        rf'git log {commit} -1 --pretty=format:"%H;%an;%ae;%as;%at;%cn;%ce;%cs;%ct"'
    ) as info:
        return info.read().split(";")


def commitLOC(commit: str, options: str = "", processes: int = 0) -> list:
    if options == "":
        command: str = rf"cloc --git {commit} --use-sloccount --processes {processes} --json 2>/dev/null | jq .SUM 2>/dev/null"
    else:
        command: str = rf"cloc --git {commit} --use-sloccount --config {options} --processes {processes} --json 2>/dev/null | jq .SUM 2>/dev/null"

    info: os._wrap_close
    with os.popen(command) as info:
        data: dict = json.load(info)
        return data.values()

def commitsDiff(commit1: str, commit2: str, str = "", processes: int = 0)  ->  list:
    data: list = []
    command: str = rf"cloc --git --diff {commit1} {commit2} --processes {processes} --json 2>/dev/null | jq .SUM 2>/dev/null"

    info: os._wrap_close
    with os.popen(command) as info:
        try:
            output: dict = json.load(info)
            keys: list = output.keys()

            key: str
            for key in keys:
                data.extend(output[key].values())
        except json.JSONDecodeError as e:
            data: list = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        return data


def commitsDelta(newLOC: list, oldLOC: list) -> list:
    return [a - b for a, b in zip(newLOC, oldLOC)]


def main() -> bool:
    pwd = os.getcwd()
    args: Namespace = mainArgs()

    if repoExists(directory=args.directory) is False:
        print(f"Invalid Git repository directory: {args.directory}")
        return False

    os.chdir(args.directory)
    os.system(f"git checkout {args.branch} --quiet")

    df: DataFrame = DataFrame(
        columns=[
            "commit_hash",
            "author_name",
            "author_email",
            "author_date",
            "author_date_unix",
            "committer_name",
            "committer_email",
            "committer_date",
            "committer_date_unix",
            "lines_of_blanks",
            "lines_of_comments",
            "lines_of_code",
            "number_of_files",
            "added_lines_of_code",
            "added_number_of_files",
            "added_lines_of_blanks",
            "added_lines_of_comments",
            "same_lines_of_code",
            "same_number_of_files",
            "same_lines_of_blanks",
            "same_lines_of_comments",
            "modified_lines_of_code",
            "modified_number_of_files",
            "modified_lines_of_blanks",
            "modified_lines_of_comments",
            "removed_lines_of_code",
            "removed_number_of_files",
            "removed_lines_of_blanks",
            "removed_lines_of_comments",
            "delta_lines_of_blanks",
            "delta_lines_of_comments",
            "delta_lines_of_code",
            "delta_number_of_files",
            "author_days_since_0",
            "committer_days_since_0",
        ]
    )

    commits: list = gitCommits()

    with Bar("Getting data from commits...", max=len(commits)) as bar:
        previousLOC: list = []
        c: int
        for c in range(len(commits)):
            data: list = commitMetadata(commit=commits[c])
            loc: list = commitLOC(commits[c], options=args.cloc, processes=args.processes)

            if c == 0:
                authorDay0: datetime = dateParse(data[3]).replace(tzinfo=None)
                committerDay0: datetime = dateParse(data[7]).replace(tzinfo=None)

                diff: list = []
                diff.extend(loc)
                diff.extend([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0])

                delta: list = loc
            else:
                diff: list = commitsDiff(commit1=commits[c], commit2=commits[c-1])
                delta = commitsDelta(loc, previousLOC)

            data.extend(loc)
            data.extend(diff)
            data.extend(delta)

            authorDateDifference: int = (
                dateParse(data[3]).replace(tzinfo=None) - authorDay0
            ).days
            committerDateDifference: int = (
                dateParse(data[7]).replace(tzinfo=None) - committerDay0
            ).days

            data.append(authorDateDifference)
            data.append(committerDateDifference)

            df.loc[len(df.index)] = data

            previousLOC = loc

            bar.next()

    df.T.to_json(join(pwd, args.output))
    return True


if __name__ == "__main__":
    main()
