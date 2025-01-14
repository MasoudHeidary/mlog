import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))



## simple interaction
from mlog import Log

log = Log(f"{__file__}.log")

log.log("this is a simple log in INFO level")
log.debug("log in debug level")
log.warning("warning log")
log.error("error level log")


## manual log setting
from mlog import LogLevel

log.ln()
log.log("manual debug level log", level=LogLevel.DBG)


## changing logging level with one variable
min_log_level = LogLevel.DBG
log = Log(f"{__file__}.log", min_log_level=min_log_level)

# all of these messages will be printed
log.ln()
log.debug("debug message")
log.log("log message")
log.warning("warning message")
log.error("error message")


min_log_level = LogLevel.WAR
log = Log(f"{__file__}.log", min_log_level=min_log_level)

# just warning and error messages will be printed
log.ln()    # won't work because it is in INFO level log
log.debug("debug message")
log.log("log message")
log.warning("warning message")
log.error("error message")