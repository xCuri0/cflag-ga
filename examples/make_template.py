import time
import subprocess
import os
import sys
import glob
import pathlib

files = ['foo/*.c', 'bar/*.c'] # Group the files into sections you want to optimize here

def benchmark(cflags, file):
    cdir = os.path.dirname(os.path.realpath(__file__))
    cf_env = os.environ.copy()
    cf_env['CC'] = os.path.dirname(os.path.realpath(sys.argv[0])) + "/cflag-override.py" + " gcc"
    cf_env['CFFILE'] = file + ":" + " ".join(str(x) for x in cflags)

    # Touch the files which the CFlags are changed so that the compiler recompiles them
    for f in glob.glob(file):
        pathlib.Path(f).touch()

    # Delete main binary(s) before building
    try:
        os.remove(cdir + './program')
    except FileNotFoundError:
        pass

    # Build the program. Modify this if your program has additionial build stages. It must be aware of the "CC" variable
    if subprocess.call(['make'], stderr=subprocess.DEVNULL, stdout=subprocess.DEVNULL, env=cf_env, cwd=cdir):
        raise AssertionError

    # Add your benchmark code for each section here
    if file == 'foo/*.c':
        start = time.perf_counter()
        subprocess.check_output([cdir + "program", "--foo"], cwd=cdir)
        return time.perf_counter() - start, cflags
    elif file == 'bar/*.c':
        start = time.perf_counter()
        subprocess.check_output([cdir + "program", "--bar"], cwd=cdir)
        return time.perf_counter() - start
