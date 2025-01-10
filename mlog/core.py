import time
from enum import Enum
import asyncio

class LogLevel(Enum):
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



class Log:

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

    
    def text_formatter(self, txt:str, level:LogLevel):
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
    def print(self, txt=".", level=LogLevel.LOG, terminal=True):
        txt = self.text_formatter(txt, level=level)
        if terminal:
            self >> txt
        self << txt
    
    # direct print in file + new line
    def println(self, txt=".", level=LogLevel.LOG, terminal=True):
        _txt = txt + "\n"
        self.print(_txt, level=level, terminal=terminal)


    def log(self, txt, terminal=False):
        self.println(txt=txt, level=LogLevel.LOG, terminal=terminal)
    
    def warning(self, txt, terminal=True):
        self.println(txt=txt, level=LogLevel.WARNING, terminal=terminal)
        
    def error(self, txt, terminal=True):
        self.println(txt=txt, level=LogLevel.ERROR, terminal=terminal)
    



class AsyncLog():
    def __init__(
            self,
            filename,
            allow_terminal=True,
            force_terminal=False,
            raise_access_error=False
            ):
        self.filename = filename
        self.allow_terminal = allow_terminal
        self.force_terminal = force_terminal
        self.raise_access_error = raise_access_error
        self.file = open(self.filename, "a")

        self.log_queue = asyncio.Queue()
        self.worker_task = asyncio.create_task(self._process_logs())

    # this function is not supported in async
    # async def __del__(self):
    #     await self.shutdown()

    async def shutdown(self):
        await self.log_queue.put(None)
        await self.worker_task
        self.file.flush()
        self.file.close()

    def text_formatter(self, txt: str, level: LogLevel):
        return f"[{time.asctime()}] [{str(level)} >> {txt}]"
    
    async def __terminal__(self, txt):
        """direct terminal print"""
        if self.allow_terminal:
            print(txt, end='')
        elif self.raise_access_error:
            raise PermissionError("Terminal access if not allowed")
    
    async def __file__(self, txt):
        """direct file print"""
        if self.force_terminal:
            await self.__terminal__(txt)
        self.file.write(txt)
        self.file.flush()
    

    async def _process_logs(self):
        """background log message processor"""
        while True:
            item = await self.log_queue.get()
            if item is None:    # shutdown signal
                break

            txt, terminal = item
            if terminal:
                await self.__file__(txt)
            else:
                await self.__terminal__(txt)
            
            
            
    async def print(self, txt, level=LogLevel.LOG, terminal=True):
        txt = self.text_formatter(txt, level)
        await self.log_queue.put((txt, terminal))

    async def println(self, txt, level=LogLevel.LOG, terminal=True):
        txt = txt + "\n"
        await self.print(txt, level, terminal)