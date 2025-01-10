
from mlog.core import Log


log_file_name = "log.txt"
log_obj = Log(log_file_name)

log_obj.log("log text")             # no print in terminal
log_obj.warning("warning text")
log_obj.error("error text")


del log_obj

# forcing terminal print
log_obj = Log(log_file_name, force_terminal=True)
log_obj.log("log with forced terminal")
del log_obj

# blocking terminal print
log_obj = Log(log_file_name, allow_terminal=False)
log_obj.error("error text without terminal print")





import asyncio

async def async_log_time():
    log = AsyncLog(f"{__file__}.async.log", force_terminal=True)

    st = time()
    for i in range(1_000_000):
        await log.println(f"log {i}")
    et = time()

    print(f"time: \t{et-st}s \tDONE")

asyncio.run(async_log_time())