import json
import os

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


def commitLOC(commit: str) -> list:
    info: os._wrap_close
    with os.popen(rf"cloc {commit} --config options.txt --json | jq .SUM[]") as info:
        return info.read().strip().split("\n")


def commitsDiff(commit1: str, commit2: str) -> list:
    info: os._wrap_close
    with os.popen(
        rf"cloc --diff {commit1} {commit2} --config options.txt --json | jq --raw-output .SUM"
    ) as info:
        data: dict = json.loads(info.read().strip())

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
        ]
    )

    commits: list = gitCommits()
    commitsDiff(
        "ae295b3233343dd9a8092134f8a10b9a45f09450",
        "01674b1d2b5fe527d32cb7f10c6056829369a73a",
    )

    # with Bar("Getting data from commits...", max=len(commits)) as bar:
    #     commit: str
    #     for commit in commits:
    #         metadata: list = commitMetadata(commit=commit)
    #         loc: list = commitLOC(commit)
    #         data: list = metadata + loc
    #         df.loc[len(df.index)] = data
    #         bar.next()
    # df.T.to_json("out.json")

    # print(df)


if __name__ == "__main__":
    main()
