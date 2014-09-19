#! /usr/bin/env python
# -*- coding: utf-8 -*-
import sys, os, re
import argparse
from os.path import dirname, realpath

#================================ head end ====================================

def main(file_path, tokenN):
    file_in  = open(file_path, 'r')
    prefix = r".*?query\[(.*?)\]"
    pattern = ""
    for x in xrange(0,tokenN):
        pattern += r".*?\[(.*?)\]"
    pattern = prefix + pattern
    log_re = re.compile(pattern)

    tokenN +=  1

    for line in file_in :
        line = line.strip()
        match = log_re.match(line)
        info = ""
        if match:
            groups = match.groups()
            for x in xrange(0,tokenN):
                info += groups[x] + "\t"
            print info
    file_in.close()

def opt_parse():
    parser = argparse.ArgumentParser(description='this is a spider')
    parser.add_argument('file',
                        help='query list file path')
    parser.add_argument('-t', action='store', dest='token', type=int, 
                        help='token number')
    args = parser.parse_args()
    return args

if __name__ == "__main__" :
    args = opt_parse()
    # print args

    main(args.file, args.token)


