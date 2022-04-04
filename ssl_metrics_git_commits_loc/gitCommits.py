import json
import os
from datetime import datetime
from typing import Iterable

from dateutil.parser import parse as dateParse
from pandas import DataFrame
from progress.bar import Bar


def gitCommits() -> list:
    with os.popen(r'git log --reverse --pretty=format:"%H"') as commits:
        return [commit.strip() for commit in commits]


def commitMetadata(commit: str) -> list:
    info: os._wrap_close
    with os.popen(
        rf'git log {commit} -1 --pretty=format:"%an;%ae;%as;%at;%cn;%ce;%cs;%ct"'
    ) as info:
        return info.read().split(";")


def commitLOC(commit: str) -> Iterable:
    info: os._wrap_close
    with os.popen(rf"cloc {commit} --config options.txt --json | jq .SUM") as info:
        return json.loads(info.read().strip()).values()


def commitsDiff(newCommit: str, oldCommit: str) -> list:
    info: os._wrap_close
    with os.popen(
        rf"cloc --diff {newCommit} {oldCommit} --config options.txt --json | jq --raw-output .SUM"
    ) as info:
        try:
            data: dict = json.loads(info.read().strip())
        except json.decoder.JSONDecodeError as e:
            return [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

        jsonAdded: dict = data["added"]
        jsonModified: dict = data["modified"]
        jsonRemoved: dict = data["removed"]

        addedLinesOfBlanks: int = jsonAdded["blank"]
        addedLinesOfComments: int = jsonAdded["comment"]
        addedLinesOfCode: int = jsonAdded["code"]
        addedNumberOfFiles: int = jsonAdded["nFiles"]

        modifiedLinesOfBlanks: int = jsonModified["blank"]
        modifiedLinesOfComments: int = jsonModified["comment"]
        modifiedLinesOfCode: int = jsonModified["code"]
        modifiedNumberOfFiles: int = jsonModified["nFiles"]

        removedLinesOfBlanks: int = jsonRemoved["blank"]
        removedLinesOfComments: int = jsonRemoved["comment"]
        removedLinesOfCode: int = jsonRemoved["code"]
        removedNumberOfFiles: int = jsonRemoved["nFiles"]

        return [
            addedLinesOfBlanks,
            addedLinesOfComments,
            addedLinesOfCode,
            addedNumberOfFiles,
            modifiedLinesOfBlanks,
            modifiedLinesOfComments,
            modifiedLinesOfCode,
            modifiedNumberOfFiles,
            removedLinesOfBlanks,
            removedLinesOfComments,
            removedLinesOfCode,
            removedNumberOfFiles,
        ]


def main() -> None:
    df: DataFrame = DataFrame(
        columns=[
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
            "author_day_since_0",
        ]
    )

    commits: list = gitCommits()

    with Bar("Getting data from commits...", max=len(commits)) as bar:
        c: int
        for c in range(len(commits)):
            data: list = commitMetadata(commit=commits[c])
            loc: list = commitLOC(commits[c])

            data.extend(loc)

            if c == 0:
                day0: datetime = dateParse(data[2])
                diff: list = commitsDiff(newCommit=commits[c], oldCommit=commits[c])
                diff[0] = list(loc)[0]
                diff[1] = list(loc)[1]
                diff[2] = list(loc)[2]
                diff[3] = list(loc)[3]
            else:
                try:
                    diff: list = commitsDiff(
                        newCommit=commits[c], oldCommit=commits[c - 1]
                    )
                except IndexError:
                    diff: list = commitsDiff(newCommit=commits[c], oldCommit=commits[c])

            data.extend(diff)

            dateDifference: int = dateParse(data[2]).day - day0.day

            data.append(dateDifference)
            df.loc[len(df.index)] = data
            bar.next()
    df.T.to_json("out.json")

    # print(df)


if __name__ == "__main__":
    main()