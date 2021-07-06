import enum
from typing import Union

@enum.unique
class SetVerboseMode(enum.Enum):
  OFF = "0"
  INFO = "2"
  VERBOSE = "3"

  def __str__(self):
    return str(self.value)

@enum.unique
class SetHdmiMode(enum.Enum):
  AUTO = "AUTO"
  SRC = "SRC"
  UHD_AUTO = "UHD_AUTO"
  UHD24 = "UHD24"
  UHD50 = "UHD50"
  UHD60 = "UHD60"
  HD1080P_AUTO = "1080P_AUTO"
  HD1080P24 = "1080P24"
  HD1080P50 = "1080P50"
  HD1080P60 = "1080P60"
  HD1080I50 = "1080I50"
  HD1080I60 = "1080I60"
  HD720P50 = "720P50"
  HD720P60 = "720P60"
  SD576P = "576P"
  SD576I = "576I"
  SD480P = "480P"
  SD480I = "480I"

  def __str__(self):
    return str(self.value)

@enum.unique
class SetZoomMode(enum.Enum):
  Z1 = "1"
  AR = "AR"
  FS = "FS"
  US = "US"
  Z1P2 = "1.2"
  Z1P3 = "1.3"
  Z1P5 = "1.5"
  Z2 = "2"
  Z0P2 = "1/2"
  Z3 = "3"
  Z4 = "4"
  Z0P3 = "1/3"
  Z0P4 = "1/4"

  def __str__(self):
    return str(self.value)

@enum.unique
class SetVolumeLevel(enum.Enum):
  MUTE = "MUTE"

  def __str__(self):
    return str(self.value)

VolumeLevelType = Union[SetVolumeLevel, int]

@enum.unique
class SetRepeatMode(enum.Enum):
  CHAPTER = "CH"
  TRACK = "TT"
  ALL = "ALL"
  OFF = "OFF"
  SHUFFLE = "SHF"
  RANDOM = "RND"

  def __str__(self):
    return str(self.value)

@enum.unique
class SetSearchMode(enum.Enum):
  CHAPTER = "C"
  TITLE = "T"

  def __str__(self):
    return str(self.value)

@enum.unique
class SetTimeCodeMode(enum.Enum):
  TOTAL_ELAPSED = "E"
  TOTAL_REMAINING = "R"
  TITLE_ELAPSED = "T"
  TITLE_REMAINING = "X"
  CHAPTER_ELAPSED = "C"
  CHAPTER_REMAINING = "K"

  def __str__(self):
    return str(self.value)

@enum.unique
class SetHdrMode(enum.Enum):
  AUTO = "Auto"
  ON = "On"
  OFF = "Off"

  def __str__(self):
    return str(self.value)

@enum.unique
class SetInputSource(enum.Enum):
  BLURAY = "0"
  HDMI_IN = "1"
  HDMI_ARC = "2"
  OPTICAL_IN = "3"
  COAX_IN = "4"
  USB_IN = "5"

  def __str__(self):
    return str(self.value)

@enum.unique
class SetScreenSaverMode(enum.Enum):
  ON = "ON"
  OFF = "OFF"
  SAVE = "SAVE"

  def __str__(self):
    return str(self.value)

@enum.unique
class SetAppMode(enum.Enum):
  DISC = "DIS"
  MUSIC = "MUS"
  PHOTO = "PHO"
  MOVIE = "MOV"
  NETWORK = "NET"
  SETUP = "SET"

  def __str__(self):
    return str(self.value)

@enum.unique
class SetSacdPriority(enum.Enum):
  MULTI_CHANNEL = "M"
  STEREO = "S"
  CD = "C"

  def __str__(self):
    return str(self.value)

@enum.unique
class SetSacdOutputMode(enum.Enum):
  DSD = "D"
  PCM = "P"
  AUTO = "A"

  def __str__(self):
    return str(self.value)

@enum.unique
class SetSpeedMode(enum.Enum):
  SLOW_1_32 = "1/32"
  SLOW_1_16 = "1/16"
  SLOW_1_8 = "1/8"
  SLOW_1_4 = "1/4"
  SLOW_1_2 = "1/2"
  NORMAL = "1"
  FAST_2 = "2"
  FAST_3 = "3"
  FAST_4 = "4"
  FAST_5 = "5"

  def __str__(self):
    return str(self.value)

  