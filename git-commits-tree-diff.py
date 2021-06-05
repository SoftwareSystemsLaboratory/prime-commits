import os
import os.path
import sys
import logging
import dateutil.parser
import datetime

from functools import reduce

import argparse


def get_argparse():
    parser = argparse.ArgumentParser()

    parser.add_argument('--dir', help="dir containing repo", default=".")
    parser.add_argument('--branch', help="default branch", default="main")
    return parser

def go():
    parser = get_argparse()
    args = parser.parse_args()
    
    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger("LOC.go()") 

    # Ensure folder has a chance to be a git repo
    repo_dir = args.dir
    git_dir = os.path.join(repo_dir, ".git")
    if not os.path.exists(git_dir):
        logger.error("Not a Git repo: %s" % git_dir)
        return
    
    # Perform analysis in-place on this folder
    pwd = os.getcwd()
    os.chdir(repo_dir)
    git_checkout(args.branch)

    # Get list of commits from "first commit"
    command = 'git log --reverse --pretty=format:"%H;%ci"'
    total_loc = 0
    with os.popen(command) as git_log_pipe:
        # --root here allows you to use this instead of has for "beginning"
        commits = [ parse_commit_line(commit) for commit in git_log_pipe ]
        #commits = git_log_pipe.read().split()
        commit_info_iter = process_commits(commits)
        delta_loc_iter = map(lambda info: info['delta_loc'], commit_info_iter)
        loc_sum = reduce(lambda x, y : x + y, delta_loc_iter, 0)

    kloc_sum = loc_sum / 1000.0
    logger.info("LOC = %d; KLOC = %.3f" % (loc_sum, kloc_sum))
    os.chdir(pwd)

def parse_commit_line(commit_line):
    (commit_hash, commit_raw_date) = commit_line.split(";")[:2]
    parsed_date = dateutil.parser.parse(commit_raw_date)
    return { 'hash' : commit_hash, 'date' : parsed_date }

def process_commits(git_commits):
    # I know this is ugly but "root" does not have a hash and is a special case in git diff-tree
    day0 = git_commits[0]['date']
    commits = [{ 'hash' : '--root', 'date' : day0 }]  + git_commits
    logger = logging.getLogger("LOC:process_commits()") 
    loc_sum = 0
    for i in range(0, len(commits)-1):
        hashX = commits[i]['hash']
        hashY = commits[i+1]['hash']
        dateY = commits[i+1]['date']
        g = git_diff_tree(hashX, hashY)
        loc_iter = map(lambda info: info['loc'], g)
        delta_sum = reduce(lambda x, y : x + y, loc_iter, 0)
        loc_sum += delta_sum
        commit_day = (dateY - day0).days
        result = { 'hash' : hashY, 'delta_loc' : delta_sum, 'loc_sum' : loc_sum, 'day' : commit_day }
        logger.info(str(result))
        yield result

def git_checkout(hash):
  checkout = 'git checkout %(hash)s' % vars()
  os.system(checkout)

# TODO: Make this into a generator
def git_diff_tree(hashX, hashY):
  logger = logging.getLogger("LOC.git_diff_tree()") 
  command = 'git diff-tree -r %(hashX)s %(hashY)s' % vars()
  delta_loc = 0
  with os.popen(command) as inf:
      for line in inf:
          info = parse_diff_tree_output(line)
          operation = info.get('operation', None)
          if operation == 'A':
              process_add(info)
          elif operation == 'D':
              process_delete(info)
          elif operation  == 'M':
              process_merge(info)
          else:
              logger.error("Unknown operation '%s'" % operation)
              continue
          delta_loc += info['loc']
          yield info


def process_add(info):
    info['loc'] = wc_lines(info['h2'])

def process_delete(info):
    info['loc'] = -wc_lines(info['h1'])

def process_merge(info):
    loc_before = wc_lines(info['h1'])
    loc_after = wc_lines(info['h2'])
    info['loc'] = loc_after - loc_before

def parse_diff_tree_output(line):
    tokens = line.split()
    try:
       (dummy1, mode, h1, h2, operation, path) = tokens[:6]
       return { 'mode' : mode, 'h1' : h1, 'h2' : h2, 'path' : path, 'operation' : operation }
    except:
       return {}

# TODO: Could replace this with cloc; make parametric
def wc_lines(blob_hash):
    command = 'git show %(blob_hash)s | wc -l' % vars()
    with os.popen(command) as inf:
        command_output = inf.read()
        return int(command_output.split()[0])
    return -1

if __name__ == '__main__':
    go()

