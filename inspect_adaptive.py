"""
Run this file with different python versions
- python3.13 inspect_adaptive.py
- python3.10 inspect_adaptive.py
"""

import dis
import platform
import sys


def fac_rec(n: int) -> int:
    return 1 if n < 2 else n * fac_rec(n - 1)


# warm up rec function
for _ in range(20):
    fac_rec(20)

code = fac_rec.__code__

print("Python version info:")
print(platform.python_implementation(), sys.version)

print("\nOriginal bytecode from dis.dis():")
dis.dis(fac_rec)

print("\nChecking _co_code_adaptive (Python 3.13 only):")

if hasattr(code, "_co_code_adaptive"):
    bytecode = list(code._co_code_adaptive)
    print("Quickened bytecode:", bytecode)

    print("\nDecoded opcodes:")
    for i, op in enumerate(bytecode):
        if op < len(dis.opname):
            name = dis.opname[op]
            if name.startswith("<") or name in ("CACHE", "EXTENDED_ARG"):
                status = "(internal or support)"
            else:
                status = ""
        else:
            name = f"<UNKNOWN:{op}>"
            status = "(specialised or fused opcode)"
        print(f"{i:2}: {name:25} {status}")
else:
    print("This version of Python does not expose _co_code_adaptive.")
