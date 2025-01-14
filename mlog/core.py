import time
from enum import Enum
import asyncio
from queue import Queue
from threading import Thread


class DefaultLogLevel(Enum):
    DBG = 0       # debug
    INF = 1       # info
    SUC = 2       # success
    WAR = 3       # warning
    ERR = 4       # error

    def __str__(self):
        return self.name

LogLevel = DefaultLogLevel

# TODO:
def extend_level(new_levels):
    """extend levels with {'new_level': new_value}"""
    pass



class Log:

    def __init__(
            self, 
            filename        = False, 
            log_lst         = True,
            allow_terminal  = True, 
            force_terminal  = False, 
            raise_access_error  = True,
            ):
        
        self.filename = filename
        self.log_lst = log_lst
        self.allow_terminal = allow_terminal
        self.force_terminal = force_terminal
        self.raise_access_error = raise_access_error

        self.file = open(self.filename, "a") if self.filename else False
    
    def __del__(self):
        self.file.flush()
        self.file.close()


    def text_formatter(self, txt:str, level:LogLevel):
        return f"[{time.asctime()}] [{str(level)}] >> {txt}"
 
    def terminal_rprint(self, txt):
        """raw print in terminal"""
        if self.allow_terminal:
            print(txt, end='')
        elif self.raise_access_error:
                raise PermissionError(f"terminal is not accessable in mlog")
    
    def file_rprint(self, txt):
        """raw print in file"""
        # if self.force_terminal:
            # self.terminal_rprint(txt)
        if self.file:
            self.file.write(txt)
            self.file.flush()
        elif self.raise_access_error:
            raise PermissionError(f"log file if not accessable in mlog")

    def ln(self, char=' ', terminal=True):
        """print a emprty line for readability"""
        if terminal or self.force_terminal:
            self.terminal_rprint(char*40)
        if self.file:
            self.file_rprint(char*40)

    def log(self, txt, level=LogLevel.INF, terminal=True):
        txt = self.text_formatter(txt + '\n', level=level)
        if terminal or self.force_terminal:
            self.terminal_rprint(txt)
        if self.file:
            self.file_rprint(txt)
    

    def debug(self, txt, terminal=True):
        self.log(txt, level=LogLevel.DBG, terminal=terminal)

    def warning(self, txt, terminal=True):
        self.log(txt, level=LogLevel.WAR, terminal=terminal)
        
    def error(self, txt, terminal=True):
        self.log(txt, level=LogLevel.ERR, terminal=terminal)
    












# class QuoteLog():
#     def __init__(
#             self,
#             filename,
#             allow_terminal=True,
#             raise_access_error=False,
#         ):
#         self.filename = filename
#         self.allow_terminal = allow_terminal
#         self.raise_access_error = raise_access_error
        
#         self.file_queue = Queue()
#         self._running = True
#         self._write_thread = Thread(target=self._file_writer, daemon=True)
#         self._write_thread.start()
        
#     def __del__(self):
#         self._running = False
#         self._write_thread.join()
#         self._flush()
        
#     def _file_writer(self):
#         with open(self.filename, "a") as file:
#             while self._running or not self.file_queue.empty():
#                 try:
#                     line = self.file_queue.get(timeout=0.1)
#                     file.write(line)
#                     file.flush()
#                 except:
#                     pass
    
#     def _flush(self):
#         with open(self.filename, "a") as file:
#             while not self.file_queue.empty():
#                 file.write(self.file_queue.get())
    
#     def text_formatter(self, txt: str, level: LogLevel):
#         return f"[{time.asctime()}] [{str(level)}] >> {txt}"
    
#     def println(self, txt, level=LogLevel.LOG, terminal=True):
#         txt = txt + "\n"
#         self.print(txt, level, terminal)
    
#     def print(self, txt, level=LogLevel.LOG, terminal=True):
#         txt = self.text_formatter(txt, level)
#         if terminal:
#             print(txt, end='')
#         self.file_queue.put(txt)


# class AsyncLog():
#     def __init__(
#             self,
#             filename,
#             allow_terminal=True,
#             force_terminal=False,
#             raise_access_error=False
#             ):
#         self.filename = filename
#         self.allow_terminal = allow_terminal
#         self.force_terminal = force_terminal
#         self.raise_access_error = raise_access_error
#         self.file = open(self.filename, "a")

#         self.log_queue = asyncio.Queue()
#         self.worker_task = asyncio.create_task(self._process_logs())

#     # this function is not supported in async
#     # async def __del__(self):
#     #     await self.shutdown()

#     async def shutdown(self):
#         await self.log_queue.put(None)
#         await self.worker_task
#         self.file.flush()
#         self.file.close()

#     def text_formatter(self, txt: str, level: LogLevel):
#         return f"[{time.asctime()}] [{str(level)} >> {txt}]"
    
#     async def __terminal__(self, txt):
#         """direct terminal print"""
#         if self.allow_terminal:
#             print(txt, end='')
#         elif self.raise_access_error:
#             raise PermissionError("Terminal access if not allowed")
    
#     async def __file__(self, txt):
#         """direct file print"""
#         if self.force_terminal:
#             await self.__terminal__(txt)
#         self.file.write(txt)
#         self.file.flush()
    

#     async def _process_logs(self):
#         """background log message processor"""
#         while True:
#             item = await self.log_queue.get()
#             if item is None:    # shutdown signal
#                 break

#             txt, terminal = item
#             if terminal:
#                 await self.__file__(txt)
#             else:
#                 await self.__terminal__(txt)
            
            
            
#     async def print(self, txt, level=LogLevel.LOG, terminal=True):
#         txt = self.text_formatter(txt, level)
#         await self.log_queue.put((txt, terminal))

#     async def println(self, txt, level=LogLevel.LOG, terminal=True):
#         txt = txt + "\n"
#         await self.print(txt, level, terminal)
