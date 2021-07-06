"""Oppo UDP SDK"""

__version__ = "0.1.4"

from .codes import OppoRemoteCode, OppoRemoteCodeType
from .const import *
from .exceptions import *
from .command import *
from .client import OppoClient
from .device import OppoDevice
