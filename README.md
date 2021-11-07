# SSL Metrics `git` Commit LOC Extractor

> Using `git`, extract Lines of Code (LOC) data from a repository and graph various metrics from it

[![DOI](https://zenodo.org/badge/374020358.svg)](https://zenodo.org/badge/latestdoi/374020358) [![Release to PyPi, GitHub, and Zenodo](https://github.com/SoftwareSystemsLaboratory/ssl-metrics-git-commits-loc/actions/workflows/release.yml/badge.svg)](https://github.com/SoftwareSystemsLaboratory/ssl-metrics-git-commits-loc/actions/workflows/release.yml)

## About

This is a proof of concept demonstrating that it is possible to use `git` to extract various Lines of Code (LOC) data from a repository and graph various metrics from it.

This software extracts LOC, Delta LOC, and KLOC (LOC / 1000) for **every commit** within a *singular branch* of a local `git` repository and stores it within a `.json` file.

This file can then be piped into a bundled graphing utility to graph the following for LOC, Delta LOC, and KLOC:

* Actual data
* Trend line
* Velocity of trend line
* Acceleration of trend line

The graphs can be saved as a `.png`, `.pdf`, or any compatible format that `matplotlib` supports.

## How to Run

### Installation

#### From pip

1. Install `Python 3.9.6 +`
2. (Recommended) Create a *virtual environment* with `python3.9 -m venv env` and *activate* it
3. Run `pip install ssl-metrics-git-commits-loc`
4. Generate a JSON data set with `ssl-metrics-git-commits-loc-extract -d DIRECTORY -b BRANCH -o FILENAME.json`
5. Generate graphs with `ssl-metrics-git-commits-loc-graph -i FILENAME.json -l LOC_GRAPH_FILENAME.* -d DELTA_LOC_GRAPH_FILENAME.* -k K_LOC_GRAPH_FILENAME.* -m ESTIMATED_POLYNOMIAL_DEGREE -r REPOSITORY_NAME`

### Command Line Arguments

#### ssl-metrics-git-commits-loc-extract

- `-h`, `--help`: Shows the help menu and exits
- `-d`, `--directory`: Directory where the `.git` folder is located
- `-b`, `--branch`: Git branch to analyze
- `-o`, `--output`: Output analysis to JSON file

#### ssl-metrics-git-commits-loc-graph

- `-h`, `--help`: Shows the help menu and exits
- `-i`, `--input`: The input data file that will be read to create the graphs
- `-l`, `--graph-loc-filename`: The filename to output the LOC graph to
- `-d`, `--graph-delta-loc-filename`: The filename to output the Delta LOC graph to
- `-k`, `--graph-k-loc-filename`: The filename to output the K LOC graph to
- `-m`, `--maximum-degree-polynomial`: Estimated maximum degree of polynomial
- `-r`, `--repository-name`: Name of the repository that is being analyzed
