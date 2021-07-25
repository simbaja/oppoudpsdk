from typing import List, Optional
from datetime import datetime, timedelta
from ..codes import OppoSetCode, OppoSetCodeType, OppoCode, OppoCodeType
from ..helpers import *
from .enums import *
from .command import OppoCommand

class OppoSetCommand(OppoCommand):
  def __init__(self, code: OppoSetCodeType, parameters: List[str] = None):      
    super().__init__(code, parameters)

  def _translate(self, code: OppoSetCodeType):
    if isinstance(code, str):
      return OppoCode(OppoSetCode(code).value)
    return OppoCode(code.value)

class OppoSetVerboseModeCommand(OppoSetCommand):
  def __init__(self, mode: SetVerboseMode):
    super().__init__(OppoSetCode.SVM)
    self._parameters.append(mode)

class OppoSetHdmiModeCommand(OppoSetCommand):
  def __init__(self, mode: SetHdmiMode):
    super().__init__(OppoSetCode.SHD)
    self._parameters.append(mode)

class OppoSetZoomModeCommand(OppoSetCommand):
  def __init__(self, mode: SetZoomMode):
    super().__init__(OppoSetCode.SZM)
    self._parameters.append(mode)

class OppoSetVolumeLevelCommand(OppoSetCommand):
  def __init__(self, level: VolumeLevelType):
    super().__init__(OppoSetCode.SVL)
    
    if isinstance(level, int):
      self._parameters.append(str(clamp(level,0,100)))
    else:
      self._parameters.append(level)

class OppoSetRepeatModeCommand(OppoSetCommand):
  def __init__(self, mode: SetRepeatMode):
    super().__init__(OppoSetCode.SRP)
    self._parameters.append(mode)

class OppoSetSubtitleShiftCommand(OppoSetCommand):
  def __init__(self, shift: int):
    super().__init__(OppoSetCode.SSH)
    self._parameters.append(str(clamp(shift,-10,10)))

class OppoSetOsdPositionCommand(OppoSetCommand):
  def __init__(self, shift: int):
    super().__init__(OppoSetCode.SOP)
    self._parameters.append(str(clamp(shift,0,5)))

class OppoSetTimeCodeModeCommand(OppoSetCommand):
  def __init__(self, mode: SetTimeCodeMode):
    super().__init__(OppoSetCode.STC)
    self._parameters.append(mode)

class OppoSetHdrModeCommand(OppoSetCommand):
  def __init__(self, mode: SetHdrMode):
    super().__init__(OppoSetCode.SHR)
    self._parameters.append(mode)

class OppoSetInputSourceCommand(OppoSetCommand):
  def __init__(self, source: SetInputSource):
    super().__init__(OppoSetCode.SIS)
    self._parameters.append(source)

class OppoSetScreensaverCommand(OppoSetCommand):
  def __init__(self, mode: SetScreenSaverMode):
    super().__init__(OppoSetCode.SSA)
    self._parameters.append(mode)

class OppoSetAppModeCommand(OppoSetCommand):
  def __init__(self, mode: SetAppMode):
    super().__init__(OppoSetCode.APP)
    self._parameters.append(mode)

class OppoSetSacdPriorityCommand(OppoSetCommand):
  def __init__(self, mode: SetSacdPriority):
    super().__init__(OppoSetCode.SSD)
    self._parameters.append(mode)

class OppoSetSacdOutputModeCommand(OppoSetCommand):
  def __init__(self, mode: SetSacdOutputMode):
    super().__init__(OppoSetCode.SDP)
    self._parameters.append(mode)

class OppoSetFwdModeCommand(OppoSetCommand):
  def __init__(self, mode: Optional[SetSpeedMode]):
    super().__init__(OppoSetCode.FWD)
    if mode is not None:
      self._parameters.append(mode)

class OppoSetRevModeCommand(OppoSetCommand):
  def __init__(self, mode: Optional[SetSpeedMode]):
    super().__init__(OppoSetCode.REV)
    if mode is not None:
      self._parameters.append(mode)

class OppoSetTitleCommand(OppoSetCommand):
  def __init__(self, title_number: int):
    super().__init__(OppoSetCode.SRH)
    self._parameters.append("T"+str(title_number))  

class OppoSetChapterCommand(OppoSetCommand):
  def __init__(self, chapter_number: int):
    super().__init__(OppoSetCode.SRH)
    self._parameters.append("C"+str(chapter_number))  

class OppoSetChapterPositionCommand(OppoSetCommand):
  def __init__(self, position: timedelta):
    super().__init__(OppoSetCode.SRH)
    self._parameters.append("C " + strfdelta(position,"{H:02}:{M:02}:{S:02}"))

class OppoSetTitlePositionCommand(OppoSetCommand):
  def __init__(self, position: timedelta):
    super().__init__(OppoSetCode.SRH)
    self._parameters.append("T " + strfdelta(position,"{H:02}:{M:02}:{S:02}"))
