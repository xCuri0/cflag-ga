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
import math
import random
import argparse
from importlib.machinery import SourceFileLoader

MUTP = 5 # Mutation probability
POP = 20 # Population per generation
MAXGEN = 10 # Maximum generation

flags = ['', '-faggressive-loop-optimizations', '-fauto-inc-dec', '-fbranch-probabilities', '-fbranch-target-load-optimize', '-fbranch-target-load-optimize2', '-fbtr-bb-exclusive', '-fcaller-saves', '-fcombine-stack-adjustments', '-fconserve-stack', '-fcompare-elim', '-fcprop-registers', '-fcrossjumping', '-fcse-follow-jumps', '-fcse-skip-blocks', '-fcx-fortran-rules', '-fcx-limited-range', '-fdata-sections', '-fdce', '-fdelayed-branch', '-fdelete-null-pointer-checks', '-fdevirtualize', '-fdevirtualize-speculatively', '-fdevirtualize-at-ltrans', '-fdse', '-fearly-inlining', '-fipa-sra', '-fexpensive-optimizations', '-ffat-lto-objects', '-ffloat-store', '-fforward-propagate', '-ffp-contract=off', '-ffp-contract=on', '-ffunction-sections', '-fgcse', '-fgcse-after-reload', '-fgcse-las', '-fgcse-lm', '-fgraphite-identity', '-fgcse-sm', '-fhoist-adjacent-loads', '-fif-conversion', '-fif-conversion2', '-findirect-inlining', '-finline-functions', '-finline-functions-called-once', '-finline-small-functions', '-fipa-cp', '-fipa-cp-clone', '-fipa-bit-cp', '-fipa-vrp', '-fipa-pta', '-fipa-profile', '-fipa-pure-const', '-fipa-reference', '-fipa-icf', '-fira-region=all', '-fira-region=mixed', '-fira-region=one', '-fira-hoist-pressure', '-fira-loop-pressure', '-fno-ira-share-save-slots', '-fno-ira-share-spill-slots', '-fisolate-erroneous-paths-dereference', '-fisolate-erroneous-paths-attribute', '-fivopts', '-fkeep-inline-functions', '-fkeep-static-functions', '-fkeep-static-consts', '-flimit-function-alignment', '-flive-range-shrinkage', '-floop-block', '-floop-interchange', '-floop-strip-mine', '-floop-unroll-and-jam', '-floop-nest-optimize', '-floop-parallelize-all', '-flra-remat', '-fmerge-constants', '-fmodulo-sched', '-fmodulo-sched-allow-regmoves', '-fmove-loop-invariants', '-fno-branch-count-reg', '-fno-defer-pop', '-fno-fp-int-builtin-inexact', '-fno-function-cse', '-fno-guess-branch-probability', '-fno-inline', '-fno-peephole', '-fno-peephole2', '-fno-printf-return-value', '-fno-sched-interblock', '-fno-sched-spec', '-fno-signed-zeros', '-fno-toplevel-reorder', '-fno-zero-initialized-in-bss', '-fomit-frame-pointer', '-foptimize-sibling-calls', '-fpartial-inlining', '-fpeel-loops', '-fpredictive-commoning', '-fprefetch-loop-arrays', '-fprofile-correction', '-fprofile-values', '-fprofile-reorder-functions', '-freciprocal-math', '-free', '-frename-registers', '-freorder-blocks', '-freorder-blocks-algorithm=simple', '-freorder-blocks-algorithm=stc', '-freorder-blocks-and-partition', '-freorder-functions', '-frerun-cse-after-loop', '-freschedule-modulo-scheduled-loops', '-frounding-math', '-fsched2-use-superblocks', '-fsched-pressure', '-fsched-spec-load', '-fsched-spec-load-dangerous', '-fsched-group-heuristic', '-fsched-critical-path-heuristic', '-fsched-spec-insn-heuristic', '-fsched-rank-heuristic', '-fsched-last-insn-heuristic', '-fsched-dep-count-heuristic', '-fschedule-fusion', '-fschedule-insns', '-fschedule-insns2', '-fselective-scheduling', '-fselective-scheduling2', '-fsel-sched-pipelining', '-fsel-sched-pipelining-outer-loops', '-fsemantic-interposition', '-fshrink-wrap', '-fshrink-wrap-separate', '-fsignaling-nans', '-fsingle-precision-constant', '-fsplit-ivs-in-unroller', '-fsplit-loops', '-fsplit-paths', '-fsplit-wide-types', '-fssa-backprop', '-fssa-phiopt', '-fstdarg-opt', '-fstore-merging', '-fstrict-aliasing', '-fthread-jumps', '-ftracer', '-ftree-bit-ccp', '-ftree-builtin-call-dce', '-ftree-ccp', '-ftree-ch', '-ftree-coalesce-vars', '-ftree-copy-prop', '-ftree-dce', '-ftree-dominator-opts', '-ftree-dse', '-ftree-forwprop', '-ftree-fre', '-fcode-hoisting', '-ftree-loop-if-convert', '-ftree-loop-im', '-ftree-phiprop', '-ftree-loop-distribution', '-ftree-loop-distribute-patterns', '-ftree-loop-ivcanon', '-ftree-loop-linear', '-ftree-loop-optimize', '-ftree-loop-vectorize', '-ftree-pre', '-ftree-partial-pre', '-ftree-pta', '-ftree-reassoc', '-ftree-sink', '-ftree-slsr', '-ftree-sra', '-ftree-switch-conversion', '-ftree-tail-merge', '-ftree-ter', '-ftree-vectorize', '-ftree-vrp', '-funconstrained-commons', '-funit-at-a-time', '-funroll-all-loops', '-funroll-loops', '-funswitch-loops', '-fipa-ra', '-fvariable-expansion-in-unroller', '-fvect-cost-model', '-fvpt', '-fweb', '-fwhole-program', '-fuse-linker-plugin']
lto = ['-flto', '-flto-partition=1to1', '-flto-partition=none', '-flto-partition=max']
unsafe = ['-fassociative-math', '-ffast-math', '-fmerge-all-constants', '-fstack-arrays', 'fno-protect-parens', '-fno-math-errno', '-funsafe-math-optimizations', '-ffinite-math-only', '-fno-trapping-math']

def mate(parents):
    new = []
    for idx in range(len(parents[1])):
        if random.uniform(0, 100) < MUTP:
            new.append(random.choice(flags))
        else:
            new.append(parents[random.randint(0, 1)][idx])
    return new

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

args = parser.parse_args()
config = SourceFileLoader("config", args.config).load_module()

if args.unsafe:
    flags.extend(unsafe)
if not args.nolto:
    flags.extend(lto)

sqrt = int(math.sqrt(len(flags)))
fbest = []

for file in config.files:
    parent = []
    best = []

    baseline = config.benchmark([], file)
    print(f"Baseline for {file} is {baseline} seconds")
    # Start evolution
    for gen in range(1, MAXGEN): # 100 maximum generations
        res = []

        if not parent:
            pop = [mate([random.sample(flags, sqrt), random.sample(flags, sqrt)]) for i in range(POP)]
        else:
            pop = [mate([parent, random.sample(flags, sqrt)]) for i in range(POP)]

        for p in pop:
            try:
                res.append([baseline - config.benchmark(p, file), p])
            except AssertionError:
                continue

        res.sort(key=lambda x: x[0], reverse=True)
        if res[0][0] > 0:
            parent = res[0][1]
            best.append(res[0])

        print(f'Generation {gen} {res[0][0]} {" ".join(str(x) for x in res[0][1])}')

    best.sort(key=lambda x: x[0], reverse=True)
    print(f'Best for {file} is {best[0][0]} {" ".join(str(x) for x in best[0][1])}')

    fbest.append([file, best[0][1]])

if args.output:
    with open(args.output, 'w') as out:
        for r in fbest:
            print(str(r[0]) + ":" + " ".join(str(x) for x in r[1]), file=out)
