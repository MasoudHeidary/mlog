import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from mlog import Log
from mlog import QuoteLog
from time import time, sleep


def ff():
    return 2**200

st = time()
log = Log(f"{__file__}.log")
for i in range(1_000_000):
    ff()
    log.println(f"{i}XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX", terminal=False)
et = time()
print(f"Time: \t{et-st:.2f}s")


st = time()
for i in range(1_000_000):
    ff()
et = time()
print(f"Time: \t{et-st}s")


st = time()
log = QuoteLog(f"{__file__}.quote.log")
for i in range(1_000_000):
    ff()
    log.println(f"{i}XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX", terminal=False)
et = time()
print(f"Time: \t{et-st:.2f}s")


sleep(10)
print(f"DONE after delay")