"""
Run this script with different Python versions
- python3.13 benchmark_versions.py
- python3.10 benchmark_versions.py
"""

import time
import platform
import sys
import statistics


def fac_rec(n: int) -> int:
    return 1 if n < 2 else n * fac_rec(n - 1)


def benchmark(repeats=100000, rounds=10):
    results = []
    for _ in range(rounds):
        t0 = time.perf_counter()
        for _ in range(repeats):
            fac_rec(100)
        t1 = time.perf_counter()
        duration = (t1 - t0) * 1_000_000 / repeats
        results.append(duration)
    return results


if __name__ == "__main__":
    print("Python:", platform.python_implementation(), sys.version)
    repeats = 30000
    rounds = 10
    results = benchmark(repeats=repeats, rounds=rounds)
    mean = statistics.mean(results)
    stdev = statistics.stdev(results)
    print(
        f"Ran fac_rec(100) {repeats} times × {rounds} rounds = {repeats * rounds:,} calls"
    )
    print(f"Mean:  {mean:.2f} µs per fac_rec(100)")
    print(f"Stdev: {stdev:.2f} µs")
