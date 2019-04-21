import time
import subprocess
import os
import random
import string
import sys
import glob
import pathlib

files = ['./foo/*.c', './bar/*.c'] # Group the files into sections you want to optimize here

def benchmark(cflags, baseline, file):
        name = './' + ''.join(random.choices(string.ascii_uppercase, k=8))
        with open(name + ".cfg", 'w') as f:
                f.write(file + ":" + " ".join(str(x) for x in cflags))

        cf_env = os.environ.copy()
        cf_env['CC'] = os.path.dirname(os.path.realpath(sys.argv[0])) + "/cflag-override.py" + " gcc"
        cf_env['CFOVERRIDE'] = name + ".cfg"

        # Touch the files which the CFlags are changed so that the compiler recompiles them
        for f in glob.glob(file):
                pathlib.Path(f).touch()

        # Build the program. Modify this if your program has additionial buils stages. It must be aware of the "CC" variable
        if subprocess.call(['make'], stderr=subprocess.DEVNULL, stdout=subprocess.DEVNULL, env=cf_env):
                return 0

        os.remove(name + ".cfg")

        # Add your benchmark code for each section here
        if file == './foo/*.c':
                start = time.perf_counter()
                subprocess.check_output(["/program", "--foo"])
                return baseline - (time.perf_counter() - start)
        elif file == './bar/*.c':
                start = time.perf_counter()
                subprocess.check_output(["/program", "--bar"])
                return baseline - (time.perf_counter() - start)