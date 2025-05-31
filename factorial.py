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


def fac_while(n: int) -> int:
    res = 1
    idx = 2
    while idx < n + 1:
        res *= idx
        idx = idx + 1
    return res


# benchmark
def bench(n: int, reps: int = 10) -> None:
    sys.setrecursionlimit(n + 50)
    t_iter = timeit.timeit(partial(fac_iter, n), number=reps)
    t_iter_while = timeit.timeit(partial(fac_while, n), number=reps)
    t_rec = timeit.timeit(partial(fac_rec, n), number=reps)
    t_fastest = min(
        ("t_iter", t_iter),
        ("t_iter_while", t_iter_while),
        ("t_rec", t_rec),
        key=lambda x: x[1],
    )

    print(
        f"n={n:<6}  reps={reps:<4}  iter: {t_iter:.6f}s iter_while: {t_iter_while:.6f}s  rec: {t_rec:.6f}s fastest: {t_fastest[0]}"
    )


print(f"Python: {sys.implementation.name} {sys.version.split()[0]}")
print("== Recursive factorial bytecode ==")
dis.dis(fac_rec)

print("\n== Iterative factorial bytecode ==")
dis.dis(fac_iter)

print("\n== Iterative (while) factorial bytecode ==")
dis.dis(fac_while)

print(f"Python: {sys.implementation.name} {sys.version.split()[0]}")
for n in (10, 100, 500, 1000, 2000, 10000, 20000, 30000, 50000):
    bench(n, reps=10)


# detailed profiling info so we can see the call overhead
N_PROFILE = 50000  # pick a size that finishes quickly but shows a gap
sys.setrecursionlimit(N_PROFILE + 50)

print(f"Python: {sys.implementation.name} {sys.version.split()[0]}")
print("\n--- cProfile on iterative version ---")
cProfile.run("fac_iter(N_PROFILE)", sort="tottime")

print("\n--- cProfile on iterative while version ---")
cProfile.run("fac_while(N_PROFILE)", sort="tottime")

print("\n--- cProfile on recursive version ---")
cProfile.run("fac_rec(N_PROFILE)", sort="tottime")
