# mlog Readme
lightweight and flexible logging library for Python

# TODO:
- queue logging
- multi thread logging
- async logging

## install mlog
```console
pip install ./mlog
```

## basic usage
```python
from mlog import Log

log = Log(f"{__file__}.log")

log.log("this is a simple log in INFO level")
log.debug("log in debug level")
log.warning("warning log")
log.error("error level log")
```

output:
```console
[Tue Jan 14 13:48:22 2025] [INF] >> this is a simple log in INFO level
[Tue Jan 14 13:48:22 2025] [DBG] >> log in debug level
[Tue Jan 14 13:48:22 2025] [WAR] >> warning log
[Tue Jan 14 13:48:22 2025] [ERR] >> error level log
```


## changing minimum logging

in the develop process the logging can set to DEBUG as minimum level. this will change to WARNING or INFO level in the published application.

```python
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
```

output:
```console
[Tue Jan 14 13:48:22 2025] [DBG] >> debug message
[Tue Jan 14 13:48:22 2025] [INF] >> log message
[Tue Jan 14 13:48:22 2025] [WAR] >> warning message
[Tue Jan 14 13:48:22 2025] [ERR] >> error message
[Tue Jan 14 13:48:22 2025] [WAR] >> warning message
[Tue Jan 14 13:48:22 2025] [ERR] >> error message

```