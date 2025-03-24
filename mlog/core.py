import time
from enum import Enum
import asyncio
from queue import Queue
from threading import Thread
import sys
from warnings import warn


class DefaultLogLevel(Enum):
    DBG = 0       # debug
    INF = 1       # info
    SUC = 2       # success
    WAR = 3       # warning
    ERR = 4       # error

    def __str__(self):
        return self.name
    
    def __lt__(self, other):
        if isinstance(other, DefaultLogLevel):
            return self.value < other.value
        return NotImplemented
    
    def __eq__(self, other):
        if isinstance(other, DefaultLogLevel):
            return self.value == other.value
        return NotImplemented

# TODO:modifyable log level
LogLevel = DefaultLogLevel


class ProgressBar:
    def __init__(self, label, char_ln=20):
        self.label = label
        self.char_ln = char_ln
        self.value = 0
    
    def print_bar(self):
        label = self.label if self.label else "no_label"
        bar_fill = int(self.value * self.char_ln)
        bar = "█" * bar_fill + "-" * (self.char_ln-bar_fill)
        per = f"{self.value * 100 : .2f}%"
        
        print(f"{label}|{bar}|{per}")
        
    def update(self, fraction):
        if not (0 <= fraction <= 1):
            raise ValueError(f"fraction is not valid")
        self.value = fraction




class Log:

    def __init__(
            self, 
            filename        = False, 
            min_log_level   = LogLevel.DBG,
            allow_terminal  = True, 
            force_terminal  = False, 
            raise_access_error  = True,
            ):
        
        self.filename = filename
        self.min_log_level = min_log_level
        self.allow_terminal = allow_terminal
        self.force_terminal = force_terminal
        self.raise_access_error = raise_access_error
        
        self.bars = []
        self.bar_topline = 100
        
        self.file = open(self.filename, "a") if self.filename else False

        
        
    def __del__(self):
        self.file.flush()
        self.file.close()


    def text_formatter(self, txt:str, level:LogLevel):
        return f"[{time.asctime()}] [{str(level)}] >> {txt}"
 
    def terminal_rprint(self, txt):
        """raw print in terminal"""
        if self.allow_terminal:
            # overwrite progress bars, or write new text
            pos = len(self.bars) - self.bar_topline

            self.move_cursor_up(pos)
            print(txt, end='')
            self.move_cursor_down(pos)
            self.bar_topline += 1
        
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

    def __log(self, txt, level, terminal):
        if level < self.min_log_level:
            return
        
        if terminal or self.force_terminal:
            self.terminal_rprint(txt)
        if self.file:
            self.file_rprint(txt)

    def ln(self, level=LogLevel.INF, terminal=True, char=' ', line_width=40,):
        """print a emprty line for readability"""
        txt = char * line_width + '\n'
        self.__log(txt, level, terminal)

    def log(self, txt, level=LogLevel.INF, terminal=True):
        if "\n" in txt:
            warn("\\n charcter in string is not recommended, use ln() function")
        txt = self.text_formatter(txt + '\n', level=level)
        self.__log(txt, level, terminal)

    def debug(self, txt, terminal=True):
        self.log(txt, level=LogLevel.DBG, terminal=terminal)

    def warning(self, txt, terminal=True):
        self.log(txt, level=LogLevel.WAR, terminal=terminal)
        
    def error(self, txt, terminal=True):
        self.log(txt, level=LogLevel.ERR, terminal=terminal)

    
    # terminal cursor management
    @staticmethod
    def move_cursor_up(n):
        if n <= 0:
            return 0
        sys.stdout.write(f"\033[{n}F")
        sys.stdout.flush()
        return n
    
    @staticmethod
    def move_cursor_down(n):
        if n <= 0:
            return 0
        sys.stdout.write(f"\033[{n}E")
        sys.stdout.flush()
        return n
    
    # progress bar management
    def create_bar(self, label):
        self.bars.append(ProgressBar(label=label))
    
    def update_bar(self, label, frac):
        i = self.__label_to_index(label)
        self.bars[i].update(frac)
        self.__print_bars()
    
    def close_bar(self, label):
        i = self.__label_to_index(label)
        del self.bars[i]
    
    def __label_to_index(self, label):
        for i, bar in enumerate(self.bars):
            if bar.label == label:
                return i
        raise LookupError(f"{label} label not found")
    
    def __print_bars(self):
        for i, bar in enumerate(self.bars):
            """overwrite any present bars, or print new bars?"""
            # if len(self.bars) - self.bar_topline > 0:
            #     move = len(self.bars) - self.bar_topline - i
            # else:
            #     move = 0
            pos = len(self.bars) - self.bar_topline - i
            

            self.move_cursor_up(pos)
            bar.print_bar()
            self.move_cursor_down(pos)
        self.bar_topline = 0
    







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
