# New file to extact LOC from git commits

import os
import pandas
from pandas import DataFrame

def gitCommits()    ->  list:
    with os.popen(r'git log --reverse --pretty=format:"%H"') as commits:
        return [commit.strip() for commit in commits]

def commitMetadata(commit: str) ->  list:
    info: os._wrap_close
    with os.popen(fr'git log {commit} -1 --pretty=format:"%an;%ae;%as;%at;%cn;%ce;%cs;%ct"') as info:
        return(info.read().split(";"))

def commitLOC(commit:str)   ->  list:
    info: os._wrap_close
    with os.popen(fr'cloc {commit} --config options.txt --json | jq .SUM[]') as info:
        print(info.read())

def main()  ->  None:
    df: DataFrame = DataFrame(columns=["author_name", "author_email", "author_date", "author_date_unix", "committer_name", "committer_email", "committer_date", "committer_date_unix"])

    commits: list = gitCommits()
    commit: str
    for commit in commits:
        # df.loc[len(df.index)] = commitMetadata(commit=commit)
        commitLOC(commit)
    # print(df)


if __name__ == "__main__":
    main()
