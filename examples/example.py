import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from mlog import Log

log = Log(f"{__file__}.log")

log.log("this is a simple log in INFO level")
log.debug("log in debug level")
log.warning("warning log")
log.error("error level log")



from mlog import LogLevel

log.log("manual debug level log", level=LogLevel.DBG)

del log