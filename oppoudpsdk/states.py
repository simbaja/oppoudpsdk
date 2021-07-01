import enum

@enum.unique
class OppoClientState(enum.Enum):
    INITIALIZING = enum.auto()
    CONNECTING = enum.auto()
    CONNECTED = enum.auto()
    DROPPED = enum.auto()
    WAITING = enum.auto()
    DISCONNECTING = enum.auto()
    DISCONNECTED = enum.auto()
