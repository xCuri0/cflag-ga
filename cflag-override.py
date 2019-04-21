#!/usr/bin/python3
import subprocess
import sys
import os
import glob

CC = sys.argv[1]
args = sys.argv[2:]

try:
    with open(os.environ['CFOVERRIDE']) as f:
        for l in f.readlines():
            for a in args:
                if os.path.abspath(a) in [os.path.abspath(x) for x in glob.glob(l.split(':')[0])]:
                    args.extend(l.split(":")[1].split())
except (IOError, IndexError):
    print("Couldn't read CFOVERRIDE file")

sys.exit(subprocess.call([CC] + args))