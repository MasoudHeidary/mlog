import time
from enum import Enum

class mLogLevel(Enum):
    LOG = 0
    WARNING = 1
    SUCCESS = 2
    ERROR = 3
    
    # more detailed logging [optional]
    INFO = 100
    DEBUG = 101
    TRACE = 102
    CRITICAL = 103
    FATAL =104

    def __str__(self):
        return self.name



class mLog:

    def __init__(
            self, 
            name, 
            allow_terminal=True, 
            force_terminal=False, 
            raise_access_error=False,
            ):
        
        self.name = name
        self.allow_terminal = allow_terminal
        self.force_terminal = force_terminal
        self.raise_access_error = raise_access_error

        self.file = open(self.name, "a")
    
    def __del__(self):
        self.file.flush()
        self.file.close()

    
    def text_formatter(self, txt:str, level:mLogLevel):
        return f"[{time.asctime()}] [{str(level)}] >> {txt}"
 

    # print in terminal
    def __rshift__(self, txt):
        if self.allow_terminal:
            print(txt, end='')
        else:
            if self.raise_access_error:
                raise PermissionError(f"terminal is not accessable in mlog")

    # print in file
    def __lshift__(self, txt):
        if self.force_terminal:
            self >> txt
        # _txt = self._txt_pre_process(txt)
        self.file.write(txt)
        self.file.flush()


    # direct print in terminal
    def terminal(self, txt):
        self >> txt

    # direct print in file
    def print(self, txt=".", level=mLogLevel.LOG, terminal=True):
        txt = self.text_formatter(txt, level=level)
        if terminal:
            self >> txt
        self << txt
    
    # direct print in file + new line
    def println(self, txt=".", level=mLogLevel.LOG, terminal=True):
        _txt = txt + "\n"
        self.print(_txt, level=level, terminal=terminal)


    def log(self, txt, terminal=False):
        self.println(txt=txt, level=mLogLevel.LOG, terminal=terminal)
    
    def warning(self, txt, terminal=True):
        self.println(txt=txt, level=mLogLevel.WARNING, terminal=terminal)
        
    def error(self, txt, terminal=True):
        self.println(txt=txt, level=mLogLevel.ERROR, terminal=terminal)
    

