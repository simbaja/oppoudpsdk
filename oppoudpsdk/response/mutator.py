import abc
from datetime import timedelta
from typing import TYPE_CHECKING
import magicattr

from .enums import VolumeLevel

if TYPE_CHECKING:
  from ..device import OppoDevice
  from .response import (
    OppoResponse, 
    OppoVolumeLevelResponse, 
    OppoUpdatePlayStatusResponse,
    OppoUpdateTimeResponse,
    OppoCurrentTotalResponse
  )

class OppoStateMutator(metaclass=abc.ABCMeta):
  """Represents a mutator that can act on an OppoDevice to change its state"""
  def __init__(self) -> None:
    pass

  @abc.abstractmethod
  async def mutate_state(self, device: 'OppoDevice', response: 'OppoResponse') -> None:
    """ Mutates the state of the device based on the response """
    pass

class OppoNopMutator(OppoStateMutator):
  async def mutate_state(self, device: 'OppoDevice', response: 'OppoResponse') -> None:
    pass

class OppoSimpleDeviceMutator(OppoStateMutator):
  def __init__(self, response_attr: str, device_attr: str) -> None:
    self.response_attr = response_attr
    self.device_attr = device_attr

  async def mutate_state(self, device: 'OppoDevice', response: 'OppoResponse') -> None:
    magicattr.set(device, self.device_attr, magicattr.get(response, self.response_attr))

class OppoSimplePlaybackMutator(OppoStateMutator):
  def __init__(self, response_attr: str, playback_attr: str) -> None:
    self.response_attr = response_attr
    self.playback_attr = playback_attr

  async def mutate_state(self, device: 'OppoDevice', response: 'OppoResponse') -> None:
    magicattr.set(device, f'playback_attributes.{self.playback_attr}', magicattr.get(response, self.response_attr))

class OppoVolumeLevelMutator(OppoStateMutator):
  async def mutate_state(self, device: 'OppoDevice', response: 'OppoVolumeLevelResponse') -> None:
    if isinstance(response.level, int):
      device.volume = response.level
      if response.level > 0:
        device.is_muted = False
    else:
      device.is_muted = response.level == VolumeLevel.MUTE 

class OppoUpdatePlayStatusMutator(OppoStateMutator):
  async def mutate_state(self, device: 'OppoDevice', response: 'OppoUpdatePlayStatusResponse') -> None:
    from ..device import OppoPlaybackStatus
    if response.tray_status:
      if device.tray_status != response.tray_status:
        device.tray_status = response.tray_status
        device.playback_attributes = OppoPlaybackStatus()
    if response.fwd_speed_mode:
      device.playback_attributes.fwd_speed = response.fwd_speed_mode
    if response.rev_speed_mode:
      device.playback_attributes.fwd_speed = response.rev_speed_mode

class OppoUpdateTimeMutator(OppoStateMutator):
  async def mutate_state(self, device: 'OppoDevice', response: 'OppoUpdateTimeResponse') -> None:
    needs_position_refresh = True if (
      device.playback_attributes.chapter != response.chapter_number or 
      device.playback_attributes.track != response.title_number
    ) else False

    if needs_position_refresh:
      if not device.is_updating:
        await device.async_request_position_update()
    else: 
      device.playback_attributes.chapter = response.chapter_number
      device.playback_attributes.track = response.title_number
      
      #figure out the deltas
      diff = timedelta(0)
      if response.time_type == "E":
        diff = response.time_value - device.playback_attributes.total_elapsed_time
      elif response.time_type == "T":
        diff = response.time_value - device.playback_attributes.track_elapsed_time
      elif response.time_type == "C":
        diff = response.time_value - device.playback_attributes.chapter_elapsed_time
      elif response.time_type == "R":
        diff = response.time_value - device.playback_attributes.total_remaining_time
      elif response.time_type == "X":
        diff = response.time_value - device.playback_attributes.track_remaining_time
      elif response.time_type == "K":
        diff = response.time_value - device.playback_attributes.chapter_remaining_time
      
      #apply the deltas  
      device.playback_attributes.total_elapsed_time += diff
      device.playback_attributes.track_elapsed_time += diff
      device.playback_attributes.chapter_elapsed_time += diff
      device.playback_attributes.total_remaining_time -= diff
      device.playback_attributes.track_remaining_time -= diff
      device.playback_attributes.chapter_remaining_time -= diff

      #if our remaining times go negative, reset them and request an
      #update to hopefully fix them up...
      if (
        device.playback_attributes.total_remaining_time <= timedelta(0) or
        device.playback_attributes.track_remaining_time <= timedelta(0) or
        device.playback_attributes.chapter_remaining_time <= timedelta(0)
      ):
        device.playback_attributes.total_remaining_time = timedelta(0)
        device.playback_attributes.track_remaining_time = timedelta(0)
        device.playback_attributes.chapter_remaining_time = timedelta(0)
        await device.async_request_position_update()

class OppoChapterTotalMutator(OppoStateMutator):
  async def mutate_state(self, device: 'OppoDevice', response: 'OppoCurrentTotalResponse') -> None:
    device.playback_attributes.chapter = response.current
    device.playback_attributes.chapter_total = response.total

class OppoTrackTotalMutator(OppoStateMutator):
  async def mutate_state(self, device: 'OppoDevice', response: 'OppoCurrentTotalResponse') -> None:
    device.playback_attributes.track = response.current
    device.playback_attributes.track_total = response.total

class OppoTrayStatusMutator(OppoStateMutator):
  async def mutate_state(self, device: 'OppoDevice', response: 'OppoResponse') -> None:
    from ..device import OppoPlaybackStatus
    if device.tray_status != response.status:
      device.tray_status = response.status
      device.playback_attributes = OppoPlaybackStatus()
