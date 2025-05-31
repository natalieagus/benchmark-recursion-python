#!/usr/bin/env python3
"""
Compare iterative vs naive recursive factorial on stock CPython
"""

import dis
import sys
import timeit
import cProfile
from functools import partial

print(f"Python: {sys.implementation.name} {sys.version.split()[0]}")


# naive implementations
def fac_iter(n: int) -> int:
    res = 1
    for i in range(2, n + 1):
        res *= i
    return res


def fac_rec(n: int) -> int:
    return 1 if n < 2 else n * fac_rec(n - 1)


# benchmark
def bench(n: int, reps: int = 10) -> None:
    sys.setrecursionlimit(n + 50)
    t_iter = timeit.timeit(partial(fac_iter, n), number=reps)
    t_rec = timeit.timeit(partial(fac_rec, n), number=reps)
    print(f"n={n:<6}  reps={reps:<4}  iter: {t_iter:.6f}s   rec: {t_rec:.6f}s")


print("== Recursive factorial bytecode ==")
dis.dis(fac_rec)

print("\n== Iterative factorial bytecode ==")
dis.dis(fac_iter)
for n in (10, 100, 500, 1000, 2000, 10000, 20000, 30000, 50000):
    bench(n, reps=10)


# detailed profiling info so we can see the call overhead
N_PROFILE = 50000  # pick a size that finishes quickly but shows a gap
sys.setrecursionlimit(N_PROFILE + 50)

print("\n--- cProfile on iterative version ---")
cProfile.run("fac_iter(N_PROFILE)", sort="tottime")

print("\n--- cProfile on recursive version ---")
cProfile.run("fac_rec(N_PROFILE)", sort="tottime")
