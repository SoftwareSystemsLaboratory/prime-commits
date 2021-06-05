import os
import os.path
import sys

import argparse


def get_argparse():
    parser = argparse.ArgumentParser()

    parser.add_argument('--dir', help="dir containing repo", default=".")
    return parser

def go():
    parser = get_argparse()
    args = parser.parse_args()
    
    repo_dir = args.dir
    git_dir = os.path.join(repo_dir, ".git")
    if not os.path.exists(git_dir):
        print("Cannot find %s" % git_dir) # todo: Log
        return
    
    pwd = os.getcwd()
    os.chdir(repo_dir)
    command = 'git log --reverse --pretty=format:"%H"'
    with os.popen(command) as git_log_pipe:
        commits = git_log_pipe.read().split()
        for i in range(0, len(commits)-1):
            print(commits[i] + ":")
            git_diff_tree(commits[i], commits[i+1])
            print()

def git_diff_tree(hashX, hashY):
  checkout = 'git checkout %(hashY)s' % vars()
  print(checkout)
  os.system(checkout)
  command = 'git diff-tree -r %(hashX)s %(hashY)s' % vars()
  with os.popen(command) as inf:
      print(command + ":")
      for line in inf:
          tokens = line.split()
          mode = tokens[4]
          path = tokens[5]
          line_count = wc_lines(path)
          print(mode, path, line_count)

def wc_lines(path):
    command = 'wc -l "%s"' % path
    text = "0"
    with os.popen(command) as inf:
        text = inf.read()
    try:
       return int(text.split()[0])
    except:
       return -1

if __name__ == '__main__':
    go()

