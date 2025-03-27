import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))


import time
from mlog import Log


log = Log()

i_max = 5
j_max = 1000

log.create_bar('i')
log.create_bar('j')
for i in range(i_max):
    log.update_bar('i', i / (i_max - 1))
    log.log(f"update i => {i}")
    log.log("this message prints before progress bars!")
        
    for j in range(j_max):
        log.update_bar('j', j / (j_max - 1))
        time.sleep(0.0001)
        
log.log("don't forget to close the progress bars after")
log.close_bar('i')
log.close_bar('j')

log.log("this log is after closing the progress bars!")