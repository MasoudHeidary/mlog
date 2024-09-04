import time

class mlog:

    def __init__(self, name=f"log-{time.asctime()}.txt", allow_terminal=True, force_terminal=False, raise_access_error=False) -> None:
        self.name = name
        self.allow_terminal = allow_terminal
        self.force_terminal = force_terminal
        self.raise_access_error = raise_access_error

        self.file = open(self.name, "a")
    
    def __del__(self):
        self.file.flush()
        self.file.close()



    def _txt_pre_process(self, txt):
        _txt = f"[{time.asctime()}] >> {txt}"
        return _txt



    def terminal(self, txt="."):
        if not self.allow_terminal:
            if self.raise_access_error:
                raise PermissionError("terminal output is not allowed")
        _txt = self._txt_pre_process(txt)
        print(_txt)


    def __lshift__(self, txt):
        _txt = self._txt_pre_process(txt)        
        self.file.write(_txt)
        self.file.flush()


    def print(self, txt=".", terminal=True):
        if terminal
        self << txt
    

    def println(self, txt=".", terminal=True):
        self << f"{txt}\n"

