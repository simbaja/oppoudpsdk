class OppoException(Exception):
    """ Base class for all other custom exceptions """
    pass

class OppoCommandError(OppoException):
    """ Exception raised when there is an error processing a command """
    def __init__(self, message: str, code, reason, *args: object) -> None:
        super().__init__(*args)
        self.code = code
        self.reason = reason
        self.message = message
    
    def __str__(self) -> str:
        return f"There was an error while processing a command: Code={self.code}, Reason={self.reason}, Message={self.message}"

class OppoInvalidStateError(OppoException):
    """ Exception raised when an invalid operation is attempted """
    def __init__(self, message: str, *args: object) -> None:
        super().__init__(*args)
        self.message = message
    
    def __str__(self) -> str:
        return f"Invalid operation: {self.message}"

