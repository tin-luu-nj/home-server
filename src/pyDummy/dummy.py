class clsDummy(object):
    def __init__(self) -> None:
        self.param: int = 0

    def foo(self, arg: bool) -> bool:
        if arg:
            return True
        return False

    def baz(self):
        self.param = 1
