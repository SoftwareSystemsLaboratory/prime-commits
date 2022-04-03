# Software Systems Laboratory Metrics Git Commits Extractor

> A `python` tool to extract commit information from a `git` repository

![[https://img.shields.io/badge/python-3.9.6%20%7C%203.10-blue](https://img.shields.io/badge/python-3.9.6%20%7C%203.10-blue)](https://img.shields.io/badge/python-3.9.6%20%7C%203.10-blue)
[![DOI](https://zenodo.org/badge/374020358.svg)](https://zenodo.org/badge/latestdoi/374020358)
[![Release Project](https://github.com/SoftwareSystemsLaboratory/ssl-metrics-git-commits-loc/actions/workflows/release.yml/badge.svg?branch=main)](https://github.com/SoftwareSystemsLaboratory/ssl-metrics-git-commits-loc/actions/workflows/release.yml)
[![https://img.shields.io/badge/license-BSD--3-yellow](https://img.shields.io/badge/license-BSD--3-yellow)](LICENSE)

## Table of Contents

- [Software Systems Laboratory Metrics Git Commits Extractor](#software-systems-laboratory-metrics-git-commits-extractor)
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
- `wc`

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
                        Directory containing repository root folder (.git)
  -b BRANCH, --branch BRANCH
                        Git branch for analysis to be ran on
  -o OUTPUT, --output OUTPUT
                        Output analysis to a JSON file
  -c CORES, --cores CORES
                        Number of cores to use for analysis
```

`ssl-metrics-git-commits-loc-graph -h`

```shell
options:
  -h, --help            show this help message and exit
  -i INPUT, --input INPUT
                        The input data file that will be read to create the graphs
  -o OUTPUT, --output OUTPUT
                        The filename to output the graph to
  -r REPOSITORY_NAME, --repository-name REPOSITORY_NAME
                        Name of the repository that is being analyzed. Will be used in the graph title
  --loc                 Utilize LOC data
  --dloc                Utilize Delta LOC data
  --kloc                Utilize KLOC data
  --graph-data          Graph the raw data. Discrete graph of the data
  --graph-best-fit      Graph the best fit polynomial of the data. Continous graph of the data. Polynomial degrees can be configured with
                        `-m`
  --graph-velocity      Graph the velocity of the data. Computes the best fit polynomial and takes the first derivitve. Polynomial degrees
                        can be configured with `-m`
  --graph-acceleration  Graph the acceleration of the data. Computes the best fit polynomial and takes the second derivitve. Polynomial
                        degrees can be configured with `-m`
  --graph-all           Graphs all possible figures of the data onto one chart. Computes the best fit polynomial and takes the first and
                        second derivitve. Polynomial degrees can be configured with `-m`
  --x-min X_MIN         The smallest x value that will be plotted
  --x-max X_MAX         The largest x value that will be plotted
  -m MAXIMUM_POLYNOMIAL_DEGREE, --maximum-polynomial-degree MAXIMUM_POLYNOMIAL_DEGREE
                        Estimated maximum degree of the best fit polynomial
  -s STEPPER, --stepper STEPPER
                        Step through every nth data point
```
