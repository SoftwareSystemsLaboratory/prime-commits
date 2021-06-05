import os
import os.path
import sys
import logging

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
    logger = logging.getLogger(__name__) 

    repo_dir = args.dir
    git_dir = os.path.join(repo_dir, ".git")
    if not os.path.exists(git_dir):
        logging.error("Cannot find %s" % git_dir)
        return
    
    pwd = os.getcwd()
    os.chdir(repo_dir)
    set_branch = 'git checkout %s' % args.branch
    os.system(set_branch)
    command = 'git log --reverse --pretty=format:"%H"'
    total_loc = 0
    with os.popen(command) as git_log_pipe:
        commits = git_log_pipe.read().split()
        for i in range(0, len(commits)-1):
            logging.info(commits[i] + ":")
            total_loc += git_diff_tree(commits[i], commits[i+1])
    os.chdir(pwd)
    logger.info("Total LOC = %d", total_loc)


# TODO: May no longer need this.
def git_checkout(hash):
  checkout = 'git checkout %(hash)s' % vars()
  os.system(checkout)

# TODO: Make this into a generator
def git_diff_tree(hashX, hashY):
  logger = logging.getLogger(__name__) 
  command = 'git diff-tree -r %(hashX)s %(hashY)s' % vars()
  logging.debug("Running: " + command)
  cumulative_loc = 0
  with os.popen(command) as inf:
      for line in inf:
          info = parse_diff_tree_output(line)
          logging.info("dictionary of info %s" % info)
          if info['operation'] == 'A':
              process_add(info)
          elif info['operation'] == 'D':
              process_delete(info)
          elif info['operation'] == 'M':
              process_merge(info)
          else:
              logger.error("Unknown operation '%(operation)s'" % info)
              continue
          cumulative_loc += info['loc']
  logging.info('> Delta KLOC = diff(%(hashX)s,%(hashY)s) = %(cumulative_loc)s' % vars())
  return cumulative_loc


def process_add(info):
    #git_checkout(info['h2'])
    info['loc'] = wc_lines(info['h2'])
    logging.info("%(path)s delta LOC = %(loc)s" % info)

def process_delete(info):
    #git_checkout(info['h1'])
    info['loc'] = -wc_lines(info['h1'])
    logging.info("%(path)s delta LOC = %(loc)s" % info)

def process_merge(info):
    #git_checkout(info['h1'])
    loc_before = wc_lines(info['h1'])
    #git_checkout(info['h2'])
    loc_after = wc_lines(info['h2'])
    info['loc'] = loc_after - loc_before
    logging.info("%(path)s delta LOC = %(loc)s" % info)

def parse_diff_tree_output(line):
    tokens = line.split()
    (dummy1, mode, h1, h2, operation, path) = tokens[:6]

    return { 'mode' : mode, 'h1' : h1, 'h2' : h2, 'path' : path, 'operation' : operation }

# Fake LOC for now...

def wc_lines(blob_hash):
    command = 'git show %(blob_hash)s | wc -l' % vars()
    with os.popen(command) as inf:
        command_output = inf.read()
        return int(command_output.split()[0])
    return -1

if __name__ == '__main__':
    go()

