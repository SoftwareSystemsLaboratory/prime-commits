# CLIME Commits

[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.6478197.svg)](https://doi.org/10.5281/zenodo.6478197)
[![Release Project](https://github.com/SoftwareSystemsLaboratory/clime-commits/actions/workflows/release.yml/badge.svg)](https://github.com/SoftwareSystemsLaboratory/clime-commits/actions/workflows/release.yml)

> A tool to extract and compute the lines of code (LOC), thousands of lines of code (KLOC), delta lines of code (DLOC), and delta thousands of lines of code (DKLOC) of a Git repository per commit

## Table of Contents

- [CLIME Commits](#clime-commits)
  - [Table of Contents](#table-of-contents)
  - [About](#about)
  - [Developer Tooling](#developer-tooling)
    - [Operating System](#operating-system)
    - [Python Tools](#python-tools)
    - [Shell Tools](#shell-tools)
  - [How To Use](#how-to-use)
    - [Installation](#installation)
    - [Command Line Arguements](#command-line-arguements)

## About

The Software Systems Laboratory (SSL) GitHub Issue Spoilage Project is a `python` tool to extract commit information from a `git` repository.

This project is licensed under the BSD-3-Clause. See the [LICENSE](LICENSE) for more information.

## Developer Tooling

To maximize the utility of this project and the greater SSL Metrics project, the following software packages are **required**:

### Operating System

All tools developed for the greater SSL Metrics project **must target** Mac OS and Linux. SSL Metrics software is not supported or recommended to run on Windows *but can be modified to do so at your own risk*.

It is recomendded to develop on Mac OS or Linux. However, if you are on a Windows machine, you can use WSL to develop as well.

### Python Tools

- `matplotlib`
- `numpy`
- `pandas`
- `progress`
- `python-dateutil`
- `scikit-learn`

### Shell Tools

You will need the following shell software to run this application:

- `git`
- `cloc`
- `SLOCCount` (optional)
- `jq`

## How To Use

### Installation

You can install the tool via `pip` with either of the two following one-liners:

- `pip install --upgrade pip ssl-metrics-meta`
- `pip install --upgrade pip ssl-metrics-git-commits-loc`

### Command Line Arguements

`ssl-metrics-git-commits-loc-extract -h`

```shell
options:
  -h, --help            show this help message and exit
  -d DIRECTORY, --directory DIRECTORY
                        Directory containg the .git folder of the repository
                        to analyze
  -b BRANCH, --branch BRANCH
                        Branch of the Git repository to analyze. DEFAULT: HEAD
  -o OUTPUT, --output OUTPUT
                        JSON file to store the data. DEFAULT:
                        ./commits_loc.json
  --cloc CLOC           TXT file containing cloc options. DEFAULT:
                        options.txt. NOTE: This is an internal options file
                        used by the program and doesn't need to be specified/
                        created by you the user (you)
```

`ssl-metrics-git-commits-loc-graph -h`

```shell
options:
  -h, --help            show this help message and exit
  -i INPUT, --input INPUT
                        JSON export from CLIME Git Commit Exploder. DEFAULT:
                        ./commits_loc.json
  -o OUTPUT, --output OUTPUT
                        Filename of the graph. DEFAULT: ./commits_loc.pdf
  -x X                  Key of the x values to use for graphing. DEFAULT:
                        author_days_since_0
  -y Y                  Key of the y values to use for graphing. DEFAULT:
                        lines_of_code
  --type TYPE           Type of figure to plot. DEFAULT: line
  --title TITLE         Title of the figure. DEFAULT: ""
  --x-label X_LABEL     X axis label of the figure. DEFAULT: ""
  --y-label Y_LABEL     Y axis label of the figure. DEFAULT: ""
  --stylesheet STYLESHEET
                        Filepath of matplotlib stylesheet to use. DEFAULT:
                        style.mplstyle. NOTE: This is an internal stylesheet
                        used by the program and doesn't need to be specified/
                        created by you the user (you)
```
