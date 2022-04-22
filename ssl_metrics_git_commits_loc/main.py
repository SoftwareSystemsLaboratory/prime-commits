import json
import logging
import os
from argparse import Namespace
from datetime import datetime
from os.path import exists, join

from dateutil.parser import parse as dateParse
from pandas import DataFrame, Series
from progress.bar import Bar

from ssl_metrics_git_commits_loc.args import mainArgs

def repoExists(directory: str = ".") -> bool:
    isGitRepository: bool = exists(join(directory, ".git"))
    if isGitRepository:
        logging.debug(f"{directory} has a .git folder")
    else:
        logging.debug(f"{directory} doesn't have a .git folder")
    return isGitRepository


def gitCommits() -> list:
    with os.popen(r'git log --reverse --pretty=format:"%H"') as commits:
        commitList: list = [commit.strip() for commit in commits]
        logging.debug(f"List of commits from Git repository: {commitList}")
        return commitList


def commitMetadata(commit: str) -> list:
    info: os._wrap_close
    with os.popen(
        rf'git log {commit} -1 --pretty=format:"%H;%an;%ae;%as;%at;%cn;%ce;%cs;%ct"'
    ) as info:
        data: str = info.read()
        logging.info(f"{commit} information:\n{data}")
        return data.split(";")


def commitLOC(commit: str, options: str = "", processes: int = 0) -> list:
    if options == "":
        command: str = rf"cloc --git {commit} --use-sloccount --processes {processes} --json 2>/dev/null"
    else:
        command: str = rf"cloc --git {commit} --use-sloccount --config {options} --processes {processes} --json 2>/dev/null"

    info: os._wrap_close
    with os.popen(command) as info:
        try:
            data: dict = json.load(info)
        except json.JSONDecodeError:
            logging.debug([0, 0, 0, 0])
            logging.info("Output should be in order: [blanks, code, comments, nfiles]")
            return [0, 0, 0, 0]
        df: DataFrame = DataFrame(data)
        output: Series = df["SUM"].dropna().sort_index()
        logging.info(f"Commit {commit} cloc information:\n{output}")
        logging.debug(f"Series to list conversion for commit {commit}: {output.to_list()}")
        logging.info("Output should be in order: [blanks, code, comments, nfiles]")
        return output.to_list()


def commitsDiff(commit1: str, commit2: str, str="", processes: int = 0) -> list:
    output: list = []
    command: str = rf"cloc --git --diff {commit1} {commit2} --processes {processes} --json 2>/dev/null"

    info: os._wrap_close
    with os.popen(command) as info:
        try:
            data: dict = json.load(info)
        except json.JSONDecodeError as e:
            logging.warning(
                f"\nERROR: Couldn't convert to JSON between commits {commit1} and {commit2}"
            )
            return [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        df: DataFrame = DataFrame(data["SUM"])

        added: Series = df["added"].dropna().sort_index()
        same: Series = df["same"].dropna().sort_index()
        modified: Series = df["modified"].dropna().sort_index()
        removed: Series = df["removed"].dropna().sort_index()

        logging.debug(f"Added diff between commits {commit1} and {commit2}:\n{added}")
        logging.debug(f"Same diff between commits {commit1} and {commit2}:\n{same}")
        logging.debug(f"Modified diff between commits {commit1} and {commit2}:\n{modified}")
        logging.debug(f"Removed diff between commits {commit1} and {commit2}:\n{removed}")

        output.extend(added.to_list())
        output.extend(same.to_list())
        output.extend(modified.to_list())
        output.extend(removed.to_list())

        logging.debug(f"Series to list conversion for the diff of commits {commit1} and {commit2}: {output}")
        logging.info("Output should be in order: [blanks, code, comments, nfiles] in key order: [added, same, modified, removed]")
        return output

def commitsDelta(newLOC: list, oldLOC: list) -> list:
    return [a - b for a, b in zip(newLOC, oldLOC)]


def main() -> bool:
    pwd = os.getcwd()
    args: Namespace = mainArgs()

    logging.basicConfig(level=logging.DEBUG, filename=args.log, filemode="a", format='%(process)d-%(asctime)s-%(levelname)s: %(message)s')
    logging.info("Started logging...")

    if repoExists(directory=args.directory) is False:
        print(f"Invalid Git repository directory: {args.directory}")
        return False

    os.chdir(args.directory)
    os.system(f"git checkout {args.branch} --quiet")
    logging.info(f"Checked out Git branch {args.branch}")

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
            "lines_of_code",
            "lines_of_comments",
            "number_of_files",
            "added_lines_of_blanks",
            "added_lines_of_code",
            "added_lines_of_comments",
            "added_number_of_files",
            "same_lines_of_blanks",
            "same_lines_of_code",
            "same_lines_of_comments",
            "same_number_of_files",
            "modified_lines_of_blanks",
            "modified_lines_of_code",
            "modified_lines_of_comments",
            "modified_number_of_files",
            "removed_lines_of_blanks",
            "removed_lines_of_code",
            "removed_lines_of_comments",
            "removed_number_of_files",
            "delta_lines_of_blanks",
            "delta_lines_of_code",
            "delta_lines_of_comments",
            "delta_number_of_files",
            "author_days_since_0",
            "committer_days_since_0",
        ]
    )

    commits: list = gitCommits()
    logging.info("Started iterating through commits\n")
    with Bar("Getting data from commits...", max=len(commits)) as bar:
        previousLOC: list = []
        c: int
        for c in range(len(commits)):
            logging.info(f"On commit {c}: ({commits[c]})")
            data: list = commitMetadata(commit=commits[c])
            loc: list = commitLOC(
                commits[c], options=args.cloc, processes=args.processes
            )

            if c == 0:
                authorDay0: datetime = dateParse(data[3]).replace(tzinfo=None)
                committerDay0: datetime = dateParse(data[7]).replace(tzinfo=None)

                diff: list = []
                diff.extend(loc)
                diff.extend([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0])

                delta: list = loc
                logging.info("Diff isn't calculated because there was no previous commit")
            else:
                diff: list = commitsDiff(commit1=commits[c], commit2=commits[c - 1])
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
            logging.info(f"End of commit {c}: {commits[c]}\n")

            bar.next()

    df.T.to_json(join(pwd, args.output))
    return True


if __name__ == "__main__":
    main()
