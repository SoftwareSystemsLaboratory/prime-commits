#!/bin/bash

rm -r dist
pip uninstall clime_commits
python -m build
pip install dist/clime_commits

echo
echo "Done building"
