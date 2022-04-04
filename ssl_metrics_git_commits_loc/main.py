import json
import os
from argparse import Namespace
from datetime import datetime
from os.path import exists, join
from typing import Any

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


def commitLOC(commit: str, options: str) -> Any:
    info: os._wrap_close
    with os.popen(
        rf"cloc {commit} --config {options} --json 2>/dev/null | jq .SUM"
    ) as info:
        return json.loads(info.read().strip()).values()


def commitsDiff(newCommit: str, oldCommit: str, options: str) -> list:
    info: os._wrap_close
    with os.popen(
        rf"cloc --quiet --diff {newCommit} {oldCommit} --config {options} --json 2>/dev/null | jq --raw-output .SUM"
    ) as info:
        try:
            data: dict = json.loads(info.read().strip())
        except json.decoder.JSONDecodeError as e:
            return [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

        jsonAdded: dict = data["added"]
        jsonModified: dict = data["modified"]
        jsonRemoved: dict = data["removed"]

        data: list = list(jsonAdded.values())
        data.extend(jsonModified.values())
        data.extend(jsonRemoved.values())

        return data


def commitsDelta(newLOC: Any, oldLOC: Any) -> list:
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
            "added_lines_of_blanks",
            "added_lines_of_comments",
            "added_lines_of_code",
            "added_number_of_files",
            "modified_lines_of_blanks",
            "modified_lines_of_comments",
            "modified_lines_of_code",
            "modified_number_of_files",
            "removed_lines_of_blanks",
            "removed_lines_of_comments",
            "removed_lines_of_code",
            "removed_number_of_files",
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
            loc: list = commitLOC(commits[c], options=args.cloc)

            if c == 0:
                authorDay0: datetime = dateParse(data[3]).replace(tzinfo=None)
                committerDay0: datetime = dateParse(data[7]).replace(tzinfo=None)
                diff: list = commitsDiff(
                    newCommit=commits[c],
                    oldCommit=commits[c],
                    options=args.cloc,
                )
                diff[0] = list(loc)[0]
                diff[1] = list(loc)[1]
                diff[2] = list(loc)[2]
                diff[3] = list(loc)[3]

                delta: list = loc
            else:
                try:
                    diff: list = commitsDiff(
                        newCommit=commits[c],
                        oldCommit=commits[c - 1],
                        options=args.cloc,
                    )
                except IndexError:
                    diff: list = commitsDiff(
                        newCommit=commits[c],
                        oldCommit=commits[c],
                        options=args.cloc,
                    )
                delta = commitsDelta(loc, previousLOC)

            data.extend(loc)
            data.extend(diff)
            data.extend(delta)

            authorDateDifference: int = (dateParse(data[3]).replace(tzinfo=None) - authorDay0).days
            committerDateDifference: int = (dateParse(data[7]).replace(tzinfo=None) - committerDay0).days

            data.append(authorDateDifference)
            data.append(committerDateDifference)

            df.loc[len(df.index)] = data

            previousLOC = loc

            bar.next()

    df.T.to_json(join(pwd, args.output))
    return True


if __name__ == "__main__":
    main()
