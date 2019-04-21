#!/usr/bin/python3
""" This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <https://www.gnu.org/licenses/>.
"""
#!/usr/bin/python3
import random
import argparse
import subprocess
import psutil
import io
import sys
from multiprocessing import Pool
from importlib.machinery import SourceFileLoader

flags = ['-faggressive-loop-optimizations', '-fauto-inc-dec', '-fbranch-probabilities', '-fbranch-target-load-optimize', '-fbranch-target-load-optimize2', '-fbtr-bb-exclusive', '-fcaller-saves', '-fcombine-stack-adjustments', '-fconserve-stack', '-fcompare-elim', '-fcprop-registers', '-fcrossjumping', '-fcse-follow-jumps', '-fcse-skip-blocks', '-fcx-fortran-rules', '-fcx-limited-range', '-fdata-sections', '-fdce', '-fdelayed-branch', '-fdelete-null-pointer-checks', '-fdevirtualize', '-fdevirtualize-speculatively', '-fdevirtualize-at-ltrans', '-fdse', '-fearly-inlining', '-fipa-sra', '-fexpensive-optimizations', '-ffat-lto-objects', '-ffloat-store', '-fforward-propagate', '-ffp-contract=off', '-ffp-contract=on', '-ffunction-sections', '-fgcse', '-fgcse-after-reload', '-fgcse-las', '-fgcse-lm', '-fgraphite-identity', '-fgcse-sm', '-fhoist-adjacent-loads', '-fif-conversion', '-fif-conversion2', '-findirect-inlining', '-finline-functions', '-finline-functions-called-once', '-finline-small-functions', '-fipa-cp', '-fipa-cp-clone', '-fipa-bit-cp', '-fipa-vrp', '-fipa-pta', '-fipa-profile', '-fipa-pure-const', '-fipa-reference', '-fipa-icf', '-fira-region=all', '-fira-region=mixed', '-fira-region=one', '-fira-hoist-pressure', '-fira-loop-pressure', '-fno-ira-share-save-slots', '-fno-ira-share-spill-slots', '-fisolate-erroneous-paths-dereference', '-fisolate-erroneous-paths-attribute', '-fivopts', '-fkeep-inline-functions', '-fkeep-static-functions', '-fkeep-static-consts', '-flimit-function-alignment', '-flive-range-shrinkage', '-floop-block', '-floop-interchange', '-floop-strip-mine', '-floop-unroll-and-jam', '-floop-nest-optimize', '-floop-parallelize-all', '-flra-remat', '-fmerge-constants', '-fmodulo-sched', '-fmodulo-sched-allow-regmoves', '-fmove-loop-invariants', '-fno-branch-count-reg', '-fno-defer-pop', '-fno-fp-int-builtin-inexact', '-fno-function-cse', '-fno-guess-branch-probability', '-fno-inline', '-fno-peephole', '-fno-peephole2', '-fno-printf-return-value', '-fno-sched-interblock', '-fno-sched-spec', '-fno-signed-zeros', '-fno-toplevel-reorder', '-fno-zero-initialized-in-bss', '-fomit-frame-pointer', '-foptimize-sibling-calls', '-fpartial-inlining', '-fpeel-loops', '-fpredictive-commoning', '-fprefetch-loop-arrays', '-fprofile-correction', '-fprofile-values', '-fprofile-reorder-functions', '-freciprocal-math', '-free', '-frename-registers', '-freorder-blocks', '-freorder-blocks-algorithm=simple', '-freorder-blocks-algorithm=stc', '-freorder-blocks-and-partition', '-freorder-functions', '-frerun-cse-after-loop', '-freschedule-modulo-scheduled-loops', '-frounding-math', '-fsched2-use-superblocks', '-fsched-pressure', '-fsched-spec-load', '-fsched-spec-load-dangerous', '-fsched-group-heuristic', '-fsched-critical-path-heuristic', '-fsched-spec-insn-heuristic', '-fsched-rank-heuristic', '-fsched-last-insn-heuristic', '-fsched-dep-count-heuristic', '-fschedule-fusion', '-fschedule-insns', '-fschedule-insns2', '-fselective-scheduling', '-fselective-scheduling2', '-fsel-sched-pipelining', '-fsel-sched-pipelining-outer-loops', '-fsemantic-interposition', '-fshrink-wrap', '-fshrink-wrap-separate', '-fsignaling-nans', '-fsingle-precision-constant', '-fsplit-ivs-in-unroller', '-fsplit-loops', '-fsplit-paths', '-fsplit-wide-types', '-fssa-backprop', '-fssa-phiopt', '-fstdarg-opt', '-fstore-merging', '-fstrict-aliasing', '-fthread-jumps', '-ftracer', '-ftree-bit-ccp', '-ftree-builtin-call-dce', '-ftree-ccp', '-ftree-ch', '-ftree-coalesce-vars', '-ftree-copy-prop', '-ftree-dce', '-ftree-dominator-opts', '-ftree-dse', '-ftree-forwprop', '-ftree-fre', '-fcode-hoisting', '-ftree-loop-if-convert', '-ftree-loop-im', '-ftree-phiprop', '-ftree-loop-distribution', '-ftree-loop-distribute-patterns', '-ftree-loop-ivcanon', '-ftree-loop-linear', '-ftree-loop-optimize', '-ftree-loop-vectorize', '-ftree-pre', '-ftree-partial-pre', '-ftree-pta', '-ftree-reassoc', '-ftree-sink', '-ftree-slsr', '-ftree-sra', '-ftree-switch-conversion', '-ftree-tail-merge', '-ftree-ter', '-ftree-vectorize', '-ftree-vrp', '-funconstrained-commons', '-funit-at-a-time', '-funroll-all-loops', '-funroll-loops', '-funswitch-loops', '-fipa-ra', '-fvariable-expansion-in-unroller', '-fvect-cost-model', '-fvpt', '-fweb', '-fwhole-program', '-fuse-linker-plugin']
lto = ['-flto', '-flto-partition=1to1', '-flto-partition=none', '-flto-partition=max']
unsafe = ['-fassociative-math', '-ffast-math', '-fmerge-all-constants', '-fstack-arrays', 'fno-protect-parens', '-fno-math-errno', '-funsafe-math-optimizations',  '-ffinite-math-only', '-fno-trapping-math']

def getoptflags(lvl):
    proc = subprocess.Popen(['gcc', '-Q' , lvl, '--help=optimizers'], stdout=subprocess.PIPE)
    for l in io.TextIOWrapper(proc.stdout, encoding="utf-8"):
        line = l.split()
        try:
            if len(line) == 1 and '-f' in line[0]:
                yield line[0].split('=')[0].rstrip()
            elif line[-1] == '[enabled]':
                yield line[-2].rstrip()
            elif line[-1] == '[disabled]':
                pass
            elif line[-1] == '[default]':
                pass
            elif '-f' in line[-2]:
                yield line[-2].split('=')[0] + "=" + line[-1].rstrip()
        except IndexError:
            continue

def dobenchmark(arg):
    flag = arg[0]
    file = arg[1]

    if args.cflags:
        cflags = args.cflags.split()
    else:
        cflags = []
    if best:
        cflags = best[0].copy()

    # Mutation
    if cflags and random.randint(1,100) == 1:
        cflags[random.randint(0,len(cflags) - 1)] = flags[random.randint(0,len(flags) - 1)]

    cflags.append(flag)

    try:
        res = config.benchmark(cflags, baseline, file)
    except Exception:
        return [[], -1]

    return [cflags, res]

# Setup command line arguments
parser = argparse.ArgumentParser(
    description='Find optimal CFLAGS using a genetic algorithm')
parser.add_argument('config', metavar='config', type=str,
                    help='Config file to use')
parser.add_argument('--unsafe', dest='unsafe', action='store_const',
                    const=True, default=False,
                    help='Allow use of unsafe CFLAGS')
parser.add_argument('--nolto', dest='nolto', action='store_const',
                    const=True, default=False,
                    help='Disable use of LTO')
parser.add_argument('--cflags', metavar='cflags', type=str,
                    help='CFLAGS to start with')
parser.add_argument('--blacklist', metavar='blacklist', type=str,
                    help='CFLAGS to be blacklisted')
parser.add_argument('--output', metavar='output', type=str,
                    help='File to output CFLAGS to. If not specified they will be only be printed')

opt = parser.add_mutually_exclusive_group()
opt.add_argument('-Os', action='store_const',
                    const=True,
                    help="Use -Os as base")
opt.add_argument('-O0', action='store_const',
                    const=True,
                    help="Use -O0 as base")
opt.add_argument('-O1', action='store_const',
                    const=True,
                    help="Use -O1 as base")
opt.add_argument('-O2', action='store_const',
                    const=True,
                    help="Use -O2 as base (default, recommended)")
opt.add_argument('-O3', action='store_const',
                    const=True,
                    help="Use -O3 as base")
opt.add_argument('-Ofast', action='store_const',
                    const=True,
                    help="Use -Ofast as base")

args = parser.parse_args()

config = SourceFileLoader("config", args.config).load_module()
optflags = []

if args.unsafe:
    flags.extend(unsafe)
if not args.nolto:
    flags.extend(lto)

if args.Os:
    optflags = getoptflags('-Os')
elif args.O0:
    optflags = getoptflags('-O0')
elif args.O1:
    optflags = getoptflags('-O1')
elif args.O2:
    optflags = getoptflags('-O2')
elif args.O3:
    optflags = getoptflags('-O3')
elif args.Ofast:
    optflags = getoptflags('-Ofast')
else:
    optflags = getoptflags('-O2')

# Remove flags already in optimization level to avoid duplicates
for f in optflags:
    for f2 in flags:
        if f == f2:
            flags.remove(f)
if args.blacklist:
    for f in args.blacklist.split():
        for f2 in flags:
            if f == f2:
                flags.remove(f)

threads = 1 # Todo add multithread support

res = []
for file in config.files:
    best = []
    bad = []
    fail = 0

    print("Evolving " + file)

    baseline = abs(config.benchmark([], 0, file))
    print("Baseline is " + str(baseline) + " seconds")
    # Start evolution
    for gen in range(len(flags)):
        pool = Pool(processes=threads)
    
        if best:
            flagsl = list(set(flags) - set(bad) - set(best[0]))
        else:
            flagsl = flags

        flagsl_len = 20
        if len(flagsl) < 20:
            flagsl_len = len(flagsl)
            if flagsl_len == 0:
                flagsl_len = -1
        try:
            results = pool.map(dobenchmark, zip(random.sample(flagsl, flagsl_len), [file] * flagsl_len))
        except ValueError:
            break

        results.sort(key=lambda x: x[1], reverse=True)

        if best:
            for i, f in enumerate(results):
                if f[1] < best[1]:
                    bad.append(f[0][-1])
                    if i == 0:
                        fail += 1
                else:
                    best = f
                    bad = []
                    fail = 0
                    break
        elif results:
            best = results[0]
        else:
            print("Bruh moment")
            continue

        print("Best of generation " + str(gen + 1) +
            " are: " + " ".join(str(x) for x in results[0][0]) + " " + str(results[0][1] * -1))

        if fail > 5:
            break
    print("Best CFLAGS for " + file + " are: " + " ".join(str(x) for x in best[0]) + " " + str(best[1] * -1))
    res.append([file, best[0]])

if args.output:
    with open(args.output, 'w') as out:
        for r in res:
            print(str(r[0]) + ":" + " ".join(str(x) for x in r[1]), file=out)