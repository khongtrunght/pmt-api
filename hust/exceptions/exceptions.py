class InvalidTokenException(Exception):
    def __init__(self, text, rsp):
        super().__init__(text)
        self._rsp = rsp

    def get_rsp(self):
        return self._rsp


class HetHanDrlException(Exception):
    pass