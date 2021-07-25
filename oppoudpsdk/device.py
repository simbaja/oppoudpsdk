import logging
import asyncio
from typing import Optional, TYPE_CHECKING
from dataclasses import dataclass
from datetime import datetime, timedelta
from .const import *
from .command import *
from .response import *
from .codes import *
from .helpers import clamp

if TYPE_CHECKING:
    from .client import OppoClient

_LOGGER = logging.getLogger(__name__)

@dataclass(repr=True, eq=True)
class OppoPlaybackStatus:
  """Playback attributes for the Oppo device"""
  track: int = 0
  track_total: int = 0
  chapter: int = 0
  chapter_total: int = 0
  track_elapsed_time: timedelta = timedelta(seconds=0)
  track_remaining_time: timedelta = timedelta(seconds=0)
  track_duration: timedelta = timedelta(seconds=0)
  chapter_elapsed_time: timedelta = timedelta(seconds=0)
  chapter_remaining_time: timedelta = timedelta(seconds=0)
  chapter_duration: timedelta = timedelta(seconds=0)
  total_elapsed_time: timedelta = timedelta(seconds=0)
  total_remaining_time: timedelta = timedelta(seconds=0)
  total_duration: timedelta = timedelta(seconds=0)
  audio_type: str = ""
  subtitle_type: str = ""
  repeat_mode: RepeatMode = RepeatMode.OFF
  video_3d_status: Video3dStatus = Video3dStatus.UNKNOWN
  video_hdr_status: VideoHdrStatus = VideoHdrStatus.UNKNOWN
  aspect_ratio: str = ""
  media_file_format: str = ""
  media_file_name: str = ""
  track_name: str = ""
  track_album: str = ""
  track_performer: str = "" 
  rev_speed: SpeedMode = SpeedMode.NORMAL
  fwd_speed: SpeedMode = SpeedMode.NORMAL

class OppoDevice:
  """Represents a low-level Oppo device"""
  def __init__(self, client: 'OppoClient', mac_address: Optional[str] = None):
    self._client = client
    self._mac_address = mac_address
    self._client.add_event_handler(EVENT_MESSAGE_RECEIVED, self._on_message_received)
    self._client.add_event_handler(EVENT_DISCONNECTED, self._on_client_disconnected)

    self.power_status = PowerStatus.DISCONNECTED
    self.playback_status = PlayStatus.OFF
    self.firmware_version = ""
    self._reset_attributes() 
    self._state_events_enabled = True
    self._update_lock = asyncio.Lock()

  @property
  def mac_address(self) -> str:
    """The oppo device's MAC address"""
    return self._mac_address.upper()

  @property
  def is_playing(self) -> bool:
    """Indicates whether the device is playing"""
    return self.playback_status not in [
      PlayStatus.OFF, 
      PlayStatus.HOME_MENU, 
      PlayStatus.MEDIA_CENTER, 
      PlayStatus.SCREEN_SAVER, 
      PlayStatus.SETUP
    ]  

  @property
  def cddb_id(self) -> str:
    """The disc id for the currently loaded disc"""
    return self.cddb_id_1 + self.cddb_id_2

  @property
  def is_updating(self) -> bool:
    """Indicates whether we are currently updating the state"""
    return not self._state_events_enabled

  async def async_request_update(self):
    """Request the device to send a full state update"""
    try:
      #async with self._update_lock:
        #disable individual state events since we're doing a bunch at once
      self._state_events_enabled = False
      await self._client.async_event(EVENT_DEVICE_STATE_UPDATING, self)
      #await self._client.async_send_command(OppoSetVerboseModeCommand(SetVerboseMode.OFF))
      await self._client.async_send_command(OppoQueryCommand(OppoQueryCode.QVM))
      await self._client.async_send_command(OppoQueryCommand(OppoQueryCode.QPW))
      await self._client.async_send_command(OppoQueryCommand(OppoQueryCode.QVR))
      await self._client.async_send_command(OppoQueryCommand(OppoQueryCode.QVL))
      await self._client.async_send_command(OppoQueryCommand(OppoQueryCode.QHD))
      await self._client.async_send_command(OppoQueryCommand(OppoQueryCode.QPL))
      await self._client.async_send_command(OppoQueryCommand(OppoQueryCode.QDT))
      await self._client.async_send_command(OppoQueryCommand(OppoQueryCode.QSH))
      await self._client.async_send_command(OppoQueryCommand(OppoQueryCode.QOP))
      await self._client.async_send_command(OppoQueryCommand(OppoQueryCode.QZM))
      await self._client.async_send_command(OppoQueryCommand(OppoQueryCode.QHR))
      await self._client.async_send_command(OppoQueryCommand(OppoQueryCode.QIS))
      await self._client.async_send_command(OppoQueryCommand(OppoQueryCode.QAR))
      await self._client.async_send_command(OppoQueryCdCommand())

      #request media-related updates
      await self.async_request_media_update(False)
    finally:
      #re-enable state events and send the updated event
      #await self._client.async_send_command(OppoSetVerboseModeCommand(SetVerboseMode.VERBOSE))
      self._state_events_enabled = True
      await self._client.async_event(EVENT_DEVICE_STATE_UPDATED, self)

  async def async_request_media_update(self, suspend_events: bool = True):
    try:
      if self.is_playing:
        if suspend_events:
          self._state_events_enabled = False
          await self._client.async_event(EVENT_DEVICE_STATE_UPDATING, self)

        await self._client.async_send_command(OppoQueryCommand(OppoQueryCode.QTK))
        await self._client.async_send_command(OppoQueryCommand(OppoQueryCode.QCH))
        await self._client.async_send_command(OppoQueryCommand(OppoQueryCode.QTE))
        await self._client.async_send_command(OppoQueryCommand(OppoQueryCode.QTR))
        await self._client.async_send_command(OppoQueryCommand(OppoQueryCode.QCE))
        await self._client.async_send_command(OppoQueryCommand(OppoQueryCode.QCR))
        await self._client.async_send_command(OppoQueryCommand(OppoQueryCode.QEL))
        await self._client.async_send_command(OppoQueryCommand(OppoQueryCode.QRE))
        await self._client.async_send_command(OppoQueryCommand(OppoQueryCode.QAT))
        await self._client.async_send_command(OppoQueryCommand(OppoQueryCode.QST))
        await self._client.async_send_command(OppoQueryCommand(OppoQueryCode.QRP))   
        await self._client.async_send_command(OppoQueryCommand(OppoQueryCode.Q3D))
        await self._client.async_send_command(OppoQueryCommand(OppoQueryCode.QHS))   
        await self._client.async_send_command(OppoQueryCommand(OppoQueryCode.QFT))
        await self._client.async_send_command(OppoQueryCommand(OppoQueryCode.QFN))
        await self._client.async_send_command(OppoQueryCommand(OppoQueryCode.QTN))
        await self._client.async_send_command(OppoQueryCommand(OppoQueryCode.QTA))
        await self._client.async_send_command(OppoQueryCommand(OppoQueryCode.QTP))
        await self._client.async_send_command(OppoQueryCommand(OppoQueryCode.QDS))
        self._calculate_duration()
    finally:
      if suspend_events:
        self._state_events_enabled = True
        await self._client.async_event(EVENT_DEVICE_STATE_UPDATED, self)        

  async def async_request_position_update(self):
    """Requests a playback position update"""
    try:
      #async with self._update_lock:      
      self._state_events_enabled = False
      await self._client.async_event(EVENT_DEVICE_STATE_UPDATING, self)
      #await self._client.async_send_command(OppoSetVerboseModeCommand(SetVerboseMode.OFF))
      await self._client.async_send_command(OppoQueryCommand(OppoQueryCode.QTK))
      await self._client.async_send_command(OppoQueryCommand(OppoQueryCode.QCH))
      await self._client.async_send_command(OppoQueryCommand(OppoQueryCode.QTE))
      await self._client.async_send_command(OppoQueryCommand(OppoQueryCode.QTR))
      await self._client.async_send_command(OppoQueryCommand(OppoQueryCode.QCE))
      await self._client.async_send_command(OppoQueryCommand(OppoQueryCode.QCR))
      await self._client.async_send_command(OppoQueryCommand(OppoQueryCode.QEL))
      await self._client.async_send_command(OppoQueryCommand(OppoQueryCode.QRE))
      self._calculate_duration()
      
    finally:
      #await self._client.async_send_command(OppoSetVerboseModeCommand(SetVerboseMode.VERBOSE))
      self._state_events_enabled = True
      await self._client.async_event(EVENT_DEVICE_STATE_UPDATED, self)

  async def async_send_command(self, code: OppoRemoteCodeType):
    """Sends a remote command to the device"""
    await self._client.async_send_command(OppoRemoteCommand(code))

  async def async_set_input_source(self, source: SetInputSource):
    """Sets the input source"""
    await self._client.async_send_command(OppoSetInputSourceCommand(source))

  async def async_set_volume(self, level: int):
    """Sets the volume, accepts a level between 0 and 100"""
    await self._client.async_send_command(OppoSetVolumeLevelCommand(clamp(level, 0, 100)))

  async def async_seek_position(self, position_type: SetSearchMode, position: timedelta):
    """Seeks to a given position within either the chapter or title."""
    if position_type == SetSearchMode.CHAPTER:
      await self._client.async_send_command(OppoSetChapterPositionCommand(position))
    else:
      await self._client.async_send_command(OppoSetTitlePositionCommand(position))  

  async def async_repeat_mode(self, mode: SetRepeatMode):
    """Sets the volume, accepts a level between 0 and 100"""
    await self._client.async_send_command(OppoSetRepeatModeCommand(mode))

  def _reset_attributes(self):
    """Initializes/resets device attributes"""
    self.is_muted = False
    self.tray_status = TrayStatus.CLOSE
    self.volume = 0
    self.hdmi_mode = HdmiMode.UNKNOWN
    self.subtitle_shift = 0
    self.osd_position = 0
    self.input_source = InputSource.UNKNOWN
    self.zoom_mode = ZoomMode.UNKNOWN
    self.hdr_setting = HdrSetting.UNKNOWN
    self.disc_type = DiscType.UNKNOWN
    self.playback_status = PlayStatus.OFF
    self.cddb_id_1 = ""
    self.cddb_id_2 = ""
    self.last_update_at = datetime.utcnow()

    self.playback_attributes = OppoPlaybackStatus()

  def _calculate_duration(self):
    """Calculates the track/chapter/total duration (these are not provided by the device directly)"""
    pa = self.playback_attributes
    pa.track_duration = pa.track_elapsed_time + pa.track_remaining_time
    pa.chapter_duration = pa.chapter_elapsed_time + pa.chapter_remaining_time
    pa.total_duration = pa.total_elapsed_time + pa.total_remaining_time

  async def _on_client_disconnected(self):
    """Handles the client disconnected event"""
    self.power_status = PowerStatus.DISCONNECTED
    self._reset_attributes()

  async def _on_message_received(self, response: OppoResponse):
    """Handles message received events, updating state as needed"""
    if response.result == ResultCode.ERROR:
      _LOGGER.info(f"Invalid response {response}, ignoring")
      return

    if self._state_events_enabled:
      await self._client.async_event(EVENT_DEVICE_STATE_UPDATING, self)

    try:
      #handle various special messages first (affecting play status/power)
      if isinstance(response, OppoPowerResponse):
        await self._handle_power_response(response.status)
      elif isinstance(response, OppoUpdatePowerStatusResponse):
        await self._handle_power_response(response.status)
      elif isinstance(response, OppoPlayResponse):
        await self._handle_play_response(response.status)
      elif isinstance(response, OppoUpdatePlayStatusResponse):
        if response.play_status:
          await self._handle_play_response(response.play_status)
        await response.mutate_state(self)
      else:
        #otherwise, modify the state based on the response
        await response.mutate_state(self)

      #indicate when we last updated
      self.last_update_at = datetime.utcnow()

      if self._state_events_enabled:
        await self._client.async_event(EVENT_DEVICE_STATE_UPDATED, self)
    except:
      _LOGGER.warning("Error updating state.", exc_info=True)

  async def _handle_power_response(self, new_status: PowerStatus):
    """Handles power change events"""
    if self.power_status != new_status:
      self.power_status = new_status
      if self.power_status == PowerStatus.ON:
        #make sure that verbose mode is enabled
        await self._client.async_send_command(OppoSetVerboseModeCommand(SetVerboseMode.VERBOSE))
        #request an update of the state since it was OFF/DISCONNECTED
        await self.async_request_update()

  async def _handle_play_response(self, new_status: PlayStatus):
    """Handles play status change events"""
    if self.playback_status != new_status:
      self.playback_status = new_status
      if self.is_playing and self._state_events_enabled:
        await self.async_request_update()
