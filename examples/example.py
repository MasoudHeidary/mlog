import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))



# ## simple interaction
# from mlog import Log

# log = Log(f"{__file__}.log")

# log.log("this is a simple log in INFO level")
# log.debug("log in debug level")
# log.warning("warning log")
# log.error("error level log")


# ## manual log setting
# from mlog import LogLevel

# log.ln()
# log.log("manual debug level log", level=LogLevel.DBG)


# ## changing logging level with one variable
# min_log_level = LogLevel.DBG
# log = Log(f"{__file__}.log", min_log_level=min_log_level)

# # all of these messages will be printed
# log.ln()
# log.debug("debug message")
# log.log("log message")
# log.warning("warning message")
# log.error("error message")


# min_log_level = LogLevel.WAR
# log = Log(f"{__file__}.log", min_log_level=min_log_level)

# # just warning and error messages will be printed
# log.ln()    # won't work because it is in INFO level log
# log.debug("debug message")
# log.log("log message")
# log.warning("warning message")
# log.error("error message")


from mlog import Log
from time import sleep
log = Log(f"rm.log")

log.log("creating bars")
log.log("creating bars")
log.log("creating bars")

i_max = 3
j_max = 100

log.create_bar("i")
log.create_bar("j")
for i in range(i_max):
    log.update_bar('i', i/(i_max-1))
    log.log(f"print log at the same time while interacting with bars, like: new i >>> {i}")
    for j in range(j_max):
        log.update_bar('j', j/(j_max-1))
        sleep(0.03)