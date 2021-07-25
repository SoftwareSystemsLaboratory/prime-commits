# Git All Python

> (Proof of Concept) Using git diff trees to analyze the git commit timeline

## Reasoning Behind the Project

We're interested in classical metrics, which often require us to look more longtudinally at project history.

In this example, we're looking at LOC (lines of code) changes between commits, starting from the "root" of the project history.

The present implementation assumes a freshly checked out Git project.

### Technical Note

The LOC calculation is done, naively, using the `wc` command. Support for running any external tool, incudng `cloc` (which is popular and quite good) is coming next.

### Notes

* This project does not support arcane projects with multiple histories. Don't expect that to work reliably (yet).

* Although we have taken every step to be "read only" in our git usage to analyze the commits, please make sure you are not running this on anything of importance.

## Install 

```
pip install git ssl-metrics-git-commits-loc
```

## Run

```
$ ssl-metrics-git-commits-loc --directory <checkout dir> --branch <branch to analyze> --save-json <filename.json>
```

**Availible arguments**
* `-d, --directory`: Directory where a `.git` folder is located. Default is `"."`.
* `-b, --branch`: A branch that exists within the Git repository. Default is `main`.
* `-s, --save-json`: The filename that will hold the output of the analysis.

## Convert Output (optional)

```
$ ssl-metrics-git-commits-convert --input <filename.json> --csv --tsv`
```

**Availible arguments**
* `-i, --input`: The input `json` file to be converted
* `--csv`: Flag to output a `CSV` file with the filename. EX: `filename.csv`
* * `--tsv`: Flag to output a `TSV` file with the filename. EX: `filename.tsv`

## Visualize (optional)

```
$ ssl-metrics-git-commits-graph.py --input <filename.json>
```

**Availible arguments**
* `-i, --input`: The input `json, csv, tsv` file to be graphed

## What You'll See

### Exported JSON file from `ssl-metrics-git-commits-loc`

* Hash of the commit
* `delta_loc`: Change in LOC since last commit
* `loc_sum`: The total LOC of the commit
* `day`: The "day" of the commit in reference of the timeline. 0 is the first day, and all dates in the commit histroy are converted to actual days of duration

### Explanation of chart

* A chart with a scatter plot overlayed on a line plot of the `delta_loc` on the y-axis, and the `day` on the x-axis.

## TODOs

* Support some of the derived metrics from our Metrics Pipeline project at https://ssl.cs.luc.edu.
