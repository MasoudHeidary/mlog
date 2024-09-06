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



    # print in terminal
    def __rshift__(self, txt):
        if not self.allow_terminal:
            if self.raise_access_error:
                raise PermissionError(f"terminal is not accessable in mlog")

        _txt = self._txt_pre_process(txt)
        print(txt)

    # print in file
    def __lshift__(self, txt):
        if self.force_terminal:
            self >> txt
        _txt = self._txt_pre_process(txt)
        self.file.write(_txt)
        self.file.flush()



    def terminal(self, txt="."):
        self >> txt

    def print(self, txt=".", terminal=True):
        if terminal:
            self >> txt
        self << txt
    
    def println(self, txt=".", terminal=True):
        _txt = txt + "\n"
        self.print(_txt, terminal)

