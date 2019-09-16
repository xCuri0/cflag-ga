#!/usr/bin/python3
import subprocess
import sys
import os
import glob

CC = sys.argv[2]
args = sys.argv[3:]
lines = []

try:
    if 'CFFILE' in os.environ:
        lines = os.environ['CFFILE'].splitlines()
    else:
        lines = open(sys.argv[1]).readlines()
    for l in lines:
        for a in args:
            if os.path.abspath(a) in [os.path.abspath(x) for x in glob.glob(l.split(':')[0])]:
                args.extend(l.split(":")[1].split())
except (IOError, IndexError):
    print("Couldn't read CFLAG override file")

sys.exit(subprocess.call([CC] + args))
