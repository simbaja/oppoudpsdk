"""Oppo UDP SDK"""

__version__ = "0.1.2"

from .codes import OppoRemoteCode, OppoRemoteCodeType
from .const import *
from .exceptions import *
from .client import OppoClient
from .device import OppoDevice
