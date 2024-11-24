
from mlog.mlog import mlog


log_file_name = "log.txt"
log_obj = mlog(log_file_name)

log_obj.log("log text")             # no print in terminal
log_obj.warning("warning text")
log_obj.error("error text")


del log_obj

# forcing terminal print
log_obj = mlog(log_file_name, force_terminal=True)
log_obj.log("log with forced terminal")
del log_obj

# blocking terminal print
log_obj = mlog(log_file_name, allow_terminal=False)
log_obj.error("error text without terminal print")
