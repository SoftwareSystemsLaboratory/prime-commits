#!/bin/bash

pip uninstall ssl-metrics-git-commits-loc -y
rm -r dist
python -m build
pip install dist/ssl_*
ssl-metrics-git-commits-loc-extract -d .
