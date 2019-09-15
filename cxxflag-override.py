#!/usr/bin/python3
import subprocess
import sys
import os
import glob

CXX = sys.argv[1]
args = sys.argv[2:]
lines = []

try:
    if 'CFFILE' in os.environ:
        lines = os.environ['CFFILE'].splitlines()
    else:
        lines = open(os.environ['CFOVERRIDE']).readlines()
    for l in lines:
        for a in args:
            if os.path.abspath(a) in [os.path.abspath(x) for x in glob.glob(l.split(':')[0])]:
                args.extend(l.split(":")[1].split())
except (IOError, IndexError):
    print("Couldn't read CFOVERRIDE file")

sys.exit(subprocess.call([CXX] + args))
