# Overview

This is a proof-of-concept to show how to script git's CLI (command-lne interface) in Python.
We're interested in classical metrics, which often require us to look more longtudinally at project history.

In this example, we're looking at LOC (lines of code) changes between commits, starting from the "root" of the project history.

Note that this does not support arcane projects with multiple histories. Don't expect that to work reliably.

The present implementation assumes a freshly checked out Git project.
Although we have taken every step to be "read only", please make sure you are not running this on anything of importance.

The LOC calculation is done, naively, using the `wc` command. Support for running any external tool, incudng `cloc` (one of the most popular and
quite good) is coming next.


# Usage

```
$ pip install -r requirements.txt
$ python git-commits-tree-diff.py --dir=<checkout dir> --branch=main
```

You may have a different main branch, e.g. master. We use main in our projects.

# What you'll see

The output will show you a timeline:
- hash of commit
- the "day" of the commit. 0 is the first day, and all dates in the commit histroy are converted to actual days of duration
- LOC delta - change in LOC since last commit
- LOC cumulative - total lOC

# Next Steps

- Add support for matplotlib to show a simple plot
- Support some of the derived metrics from our Metrics Pipeline project at https://ssl.cs.luc.edu.
