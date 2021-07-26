import enum
from typing import Union

@enum.unique
class ResultCode(enum.Enum):
  """Indicates whether the command was successful"""
  OK = "OK"
  ERROR = "ER"

@enum.unique
class PowerStatus(enum.Enum):
  """Indicate the current power status"""
  DISCONNECTED = "DISCONNECTED"
  ON = "ON"
  OFF = "OFF"

@enum.unique
class PlayStatus(enum.Enum):
  """Indicates the current play status"""
  OFF = "OFF"
  PLAY = "PLAY"
  PAUSE = "PAUSE"
  STOP = "STOP"
  STEP = "STEP"
  FAST_REVERSE = "FREV"
  FAST_FORWARD = "FFWD"
  SLOW_REVERSE = "SREV"
  SLOW_FORWARD = "SFWD"
  SETUP = "SETUP"
  HOME_MENU = "HOME_MENU"
  MEDIA_CENTER = "MEDIA CENTER"
  SCREEN_SAVER = "SCREEN SAVER"
  DISC_MENU = "DISC MENU"
  CLOSE = "CLOSE"
  OPEN = "OPEN"

@enum.unique
class VolumeLevel(enum.Enum):
  """Indicates the device volume level"""
  MUTE = "MUTE"
  UNMUTE = "UNMUTE"

  def __str__(self):
    return str(self.value)

VolumeLevelType = Union[VolumeLevel, int]  

@enum.unique
class TrayStatus(enum.Enum):
  """Indicates the tray status"""
  OPEN = "OPEN"
  CLOSE = "CLOSE"

@enum.unique
class HdmiMode(enum.Enum):
  """Indicates the HDMI output mode"""
  UNKNOWN = "UNKNOWN"
  AUTO = "AUTO"
  SRC = "Source Direct"
  UHD_AUTO = "UHD_AUTO"
  UHD24 = "UHD24"
  UHD50 = "UHD50"
  UHD60 = "UHD60"
  HD1080P_AUTO = "1080PAUTO"
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

@enum.unique
class ZoomMode(enum.Enum):
  """Indicate the zoom mode"""
  UNKNOWN = "UNKNOWN"
  OFF = "00"
  STRETCH = "01"
  FULL = "02"
  UNDERSCAN = "03"
  Z1D2X = "04"
  Z1D3X = "05"
  Z1D5X = "06"
  Z2X = "07"
  Z3X = "08"
  Z4X = "09"
  Z0D2X = "10"
  Z0D3X = "11"
  Z0D4X = "12"

@enum.unique
class HdrSetting(enum.Enum):
  """Indicate the HDR setting"""
  UNKNOWN = "UNKNOWN"
  AUTO = "Auto"
  ON = "On"
  OFF = "Off"
  STRIP_METADATA = "StripMetadata"

@enum.unique
class Video3dStatus(enum.Enum):
  """Indicate the 3D status for the playing video"""
  UNKNOWN = "UNKNOWN"
  V3D = "3D"
  V2D = "2D"

@enum.unique
class VideoHdrStatus(enum.Enum):
  """Indicate the HDR status for the playing video"""
  UNKNOWN = "UNKNOWN"
  HDR = "HDR"
  SDR = "SDR"
  DOV = "DOV"

@enum.unique
class InputSource(enum.Enum):
  """Indicates the input source"""
  UNKNOWN = "UNKNOWN"
  BLURAY = "0"
  HDMI_IN = "1"
  HDMI_ARC = "2"
  OPTICAL_IN = "3"
  COAX_IN = "4"
  USB_IN = "5"

@enum.unique
class DiscType(enum.Enum):
  """Indicates the type of disc"""
  UNKNOWN = "UNKNOW-DISC"
  BLURAY = "BD-MV"
  DVD_VIDEO = "DVD-VIDEO"
  DVD_AUDIO = "DVD-AUDIO"
  SACD = "SACD"
  CDDA = "CDDA"  
  UHD_BLURAY = "UHBD"
  NONE = "NO-DISC"
  DATA = "DATA"
  VCD2 = "VCD2"
  SVCD = "SVCD"

@enum.unique
class RepeatMode(enum.Enum):
  """Indicates the repeat mode"""
  OFF = "00"
  REPEAT_ONE = "01"
  REPEAT_CHAPTER = "02"
  REPEAT_ALL = "03"
  REPEAT_TITLE = "04"
  SHUFFLE = "05"
  RANDOM = "06"
  
@enum.unique
class SpeedMode(enum.Enum):
  """Indicates the speed mode for FWD/REV operations"""
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
  STEP = "STEP"

@enum.unique
class UpdatePlayStatus(enum.Enum):
  """Indicates the play status (from an update response)"""
  NO_DISC = "DISC"
  LOADING = "LOAD"
  TRAY_OPEN = "OPEN"
  TRAY_CLOSING = "CLOS"
  PLAY = "PLAY"
  PAUSED = "PAUS"
  STOPPED = "STOP"
  STP_FWD = "STPF"
  STP_REV = "STPR"
  FFWD_1 = "FFW1"
  FFWD_2 = "FFW2"
  FFWD_3 = "FFW3"
  FFWD_4 = "FFW4"
  FFWD_5 = "FFW5"
  FREV_1 = "FRV1"
  FREV_2 = "FRV2"
  FREV_3 = "FRV3"
  FREV_4 = "FRV4"
  FREV_5 = "FRV5"
  SFWD_1 = "SFW1"
  SFWD_2 = "SFW2"
  SFWD_3 = "SFW3"
  SFWD_4 = "SFW4"
  SFWD_5 = "SFW5"
  SREV_1 = "SRV1"
  SREV_2 = "SRV2"
  SREV_3 = "SRV3"
  SREV_4 = "SRV4"
  SREV_5 = "SRV5"
  HOME = "HOME"
  MEDIA_CENTER = "MCTR"
  SCREEN_SAVER = "SCVR"
  DISC_MENU = "MENU"

@enum.unique
class UpdateDiscType(enum.Enum):
  """Indicates the disc type (from an update response)"""
  UNKNOWN = "UNKW"
  BLURAY = "BDMV"
  DVD_VIDEO = "DVDV"
  DVD_AUDIO = "DVDA"
  SACD = "SACD"
  CDDA = "CDDA"  
  UHD_BLURAY = "UHBD"
  DATA = "DATA"
  VCD2 = "VCD2"
  SVCD = "SVCD"