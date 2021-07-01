import logging
from datetime import datetime, timedelta
from dataclasses import dataclass
from typing import List, NamedTuple, Optional, TYPE_CHECKING

from ..codes import *
from .enums import *
from .mutator import OppoNopMutator, OppoStateMutator
from .mapping import (
  _UPDATE_PLAY_STATUS_TO_PLAY_STATUS, 
  _UPDATE_PLAY_STATUS_TO_SPEED_MODE, 
  _UPDATE_PLAY_STATUS_TO_TRAY_STATUS,
  _UPDATE_DISC_TYPE_TO_DISC_TYPE
)

if TYPE_CHECKING:
    from ..device import OppoDevice

_LOGGER = logging.getLogger(__name__)    

class OppoParsedResponse(NamedTuple):
  code: str
  result: str
  parameters: List[str] = None

@dataclass(repr=True, eq=True)
class OppoResponse:
  code: OppoCodeType
  result: ResultCode
  _parameters: List[str]
  _raw_value: Optional[str]
  
  def __init__(self, parsed: OppoParsedResponse, mutator: OppoStateMutator = OppoNopMutator(), raw_value: Optional[str] = None, single_parameter: bool = True):
    self.code = self._translate(parsed.code)
    self.result = ResultCode(parsed.result)
    
    #note: many responses can have spaces, so by default
    #we'll just rejoin all the rest of the parameters
    #if we need to split again later, we can do that in a subclass
    if single_parameter:
      self._parameters = [" ".join(parsed.parameters)]
    else:
      self._parameters = parsed.parameters
    self._raw_value = raw_value
    self._mutator = mutator

  def _translate(self, code: OppoCodeType):
    try:
      if isinstance(code, str):
        return OppoCode(code)    
    except:
      _LOGGER.info(f'Unexpected code received: {code}')
      pass
    return code

  async def mutate_state(self, device: 'OppoDevice'):
    await self._mutator.mutate_state(device, self)

class OppoStringResponse(OppoResponse):
  @property
  def value(self) -> str:
    return self._parameters[0]

class OppoIntResponse(OppoResponse):
  @property
  def value(self) -> str:
    return int(self._parameters[0])

class OppoTimeResponse(OppoResponse):
  @property
  def value(self) -> timedelta:
    t = datetime.strptime(self._parameters[0],"%H:%M:%S")
    return timedelta(hours=t.hour,minutes=t.minute,seconds=t.second)

class OppoPowerResponse(OppoResponse):
  @property
  def status(self) -> PowerStatus:
    return PowerStatus(self._parameters[0])

class OppoPlayResponse(OppoResponse):
  @property
  def status(self) -> PlayStatus:
    return PlayStatus(self._parameters[0])

class OppoHdmiModeResponse(OppoResponse):
  @property
  def mode(self) -> PlayStatus:
    return HdmiMode(self._parameters[0])

class OppoVolumeLevelResponse(OppoResponse):
  @property
  def level(self) -> VolumeLevelType:
    try:
      return int(self._parameters[0])
    except:
      return VolumeLevel(self._parameters[0])

class OppoZoomModeResponse(OppoResponse):
  def __init__(self, parsed: OppoParsedResponse, mutator: OppoStateMutator, raw_value: Optional[str] = None):
      super().__init__(parsed, mutator, raw_value, False)
  @property
  def mode(self) -> ZoomMode:
    return ZoomMode(self._parameters[0])

class OppoInputSourceResponse(OppoResponse):
  def __init__(self, parsed: OppoParsedResponse, mutator: OppoStateMutator, raw_value: Optional[str] = None):
      super().__init__(parsed, mutator, raw_value, False)
  @property
  def source(self) -> InputSource:
    return InputSource(self._parameters[0])

class OppoDiscTypeResponse(OppoResponse):
  @property
  def disc_type(self) -> DiscType:
    return DiscType(self._parameters[0])

class OppoHdrSettingResponse(OppoResponse):
  @property
  def setting(self) -> HdrSetting:
    return HdrSetting(self._parameters[0])

class OppoRepeatModeResponse(OppoResponse):
  def __init__(self, parsed: OppoParsedResponse, mutator: OppoStateMutator, raw_value: Optional[str] = None):
      super().__init__(parsed, mutator, raw_value, False)
  @property
  def mode(self) -> RepeatMode:
    return RepeatMode(self._parameters[0])

class OppoVideo3dStatusResponse(OppoResponse):
  @property
  def status(self) -> Video3dStatus:
    return Video3dStatus(self._parameters[0])

class OppoVideoHdrStatusResponse(OppoResponse):
  @property
  def status(self) -> VideoHdrStatus:
    return VideoHdrStatus(self._parameters[0])

class OppoSpeedModeResponse(OppoResponse):
  @property
  def mode(self) -> SpeedMode:
    return SpeedMode(self._parameters[0])

class OppoTrayStatusResponse(OppoResponse):
  @property
  def status(self) -> TrayStatus:
    return TrayStatus(self._parameters[0])    

class OppoCurrentTotalResponse(OppoResponse):
  @property
  def current(self) -> int:
    return int(self._parameters[0].split('/')[0])  
  @property
  def total(self) -> int:
    return int(self._parameters[0].split('/')[1])

class OppoUpdatePowerStatusResponse(OppoResponse):
  @property
  def status(self) -> PowerStatus:
    return PowerStatus.ON if int(self._parameters[0]) == 1 else PowerStatus.OFF

class OppoUpdatePlayStatusResponse(OppoResponse):
  @property
  def update_status(self) -> UpdatePlayStatus:
    return UpdatePlayStatus(self._parameters[0])
  @property
  def play_status(self) -> Optional[PlayStatus]:
    try:
      return _UPDATE_PLAY_STATUS_TO_PLAY_STATUS[self.update_status]
    except:
      return None
  @property
  def tray_status(self) -> Optional[TrayStatus]:
    try:
      return _UPDATE_PLAY_STATUS_TO_TRAY_STATUS[self.update_status]
    except:
      return None
  @property
  def fwd_speed_mode(self) -> Optional[SpeedMode]:
    try:
      if 'FW' in self.update_status.value:
        return _UPDATE_PLAY_STATUS_TO_SPEED_MODE[self.update_status]
    except:
      pass
    return None
  @property
  def rev_speed_mode(self) -> Optional[SpeedMode]:
    try:
      if 'RV' in self.update_status.value:
        return _UPDATE_PLAY_STATUS_TO_SPEED_MODE[self.update_status]
    except:
      pass
    return None 

class OppoUpdateDiscTypeResponse(OppoResponse):
  @property
  def disc_type(self) -> DiscType:
    return _UPDATE_DISC_TYPE_TO_DISC_TYPE[UpdateDiscType(self._parameters[0])]

class OppoUpdateTimeResponse(OppoResponse):
  def __init__(self, parsed: OppoParsedResponse, mutator: OppoStateMutator, raw_value: Optional[str] = None):
      super().__init__(parsed, mutator, raw_value, False)  
  @property
  def title_number(self):
    return int(self._parameters[0])
  @property
  def chapter_number(self):
    return int(self._parameters[1])
  @property
  def time_type(self):
    return self._parameters[2]
  @property
  def time_value(self) -> timedelta:
    t = datetime.strptime(self._parameters[3],"%H:%M:%S")
    return timedelta(hours=t.hour,minutes=t.minute,seconds=t.second)  