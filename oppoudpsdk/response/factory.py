from typing import Any, Tuple, Type
from ..const import *
from .response import *
from .mutator import *

class ResponseMapping(NamedTuple):
  """Represents a combination of response and mutator which is used to handle a response"""
  response_type: Type
  mutator: OppoStateMutator

def get_response(message: bytes) -> OppoResponse:
  """Gets the response for a given message."""
  parsed = _parse_message(message)
  try:
    tcode = _translate_code(parsed.code)
    if tcode in _MAPPING:
      mapping =_MAPPING[tcode]
      return mapping.response_type(parsed, mapping.mutator, message)
  except:
    pass

  return OppoResponse(parsed, OppoNopMutator(), message) 

def _parse_message(message: bytes) -> OppoParsedResponse:
  """Parses a message received to identify the code, result, and parameters """
  decoded = message.decode()

  try:
    segments = decoded[:-1].split(" ")
    
    p_code = segments[0][1:]

    #must be wrong verbose mode, don't have the actual code
    if p_code in ["OK","ER"]:
      p_result = p_code
      p_code = ""
      p_parameters = segments[1:]
    #update codes don't have a result...
    elif p_code.startswith('U'):
      p_result = "OK"
      p_parameters = segments[1:]
    else:
      p_result = segments[1]
      p_parameters = segments[2:]
  except:
    p_code = ""
    p_result = "ER"
    p_parameters = [] 

  return OppoParsedResponse(
    code = p_code,
    result = p_result,
    parameters = p_parameters
  )

def _translate_code(code: OppoCodeType):
  try:
    if isinstance(code, str):
      return OppoCode(code)    
  except:
    _LOGGER.info(f'Unexpected code received: {code}')
    pass
  return code  

_MAPPING = {
  OppoCode.QPW: ResponseMapping(OppoPowerResponse, OppoSimpleDeviceMutator('status',ATTR_DEVICE_POWER_STATUS)),
  OppoCode.PON: ResponseMapping(OppoPowerResponse, OppoSimpleDeviceMutator('status',ATTR_DEVICE_POWER_STATUS)),
  OppoCode.POF: ResponseMapping(OppoPowerResponse, OppoSimpleDeviceMutator('status',ATTR_DEVICE_POWER_STATUS)),
  OppoCode.POW: ResponseMapping(OppoPowerResponse, OppoSimpleDeviceMutator('status',ATTR_DEVICE_POWER_STATUS)),
  OppoCode.UPW: ResponseMapping(OppoUpdatePowerStatusResponse, OppoNopMutator()),

  OppoCode.QVM: ResponseMapping(OppoIntResponse, OppoNopMutator()),
  OppoCode.SVM: ResponseMapping(OppoIntResponse, OppoNopMutator()),
  OppoCode.QVR: ResponseMapping(OppoStringResponse, OppoSimpleDeviceMutator('value', ATTR_DEVICE_FIRMWARE_VERSION)),
  OppoCode.QVL: ResponseMapping(OppoVolumeLevelResponse, OppoVolumeLevelMutator()),  
  OppoCode.SVL: ResponseMapping(OppoVolumeLevelResponse, OppoVolumeLevelMutator()),  
  #TODO: there's an undocumented UVL that needs to be mapped
  OppoCode.MUT: ResponseMapping(OppoVolumeLevelResponse, OppoVolumeLevelMutator()),    
  OppoCode.VUP: ResponseMapping(OppoVolumeLevelResponse, OppoVolumeLevelMutator()),    
  OppoCode.VDN: ResponseMapping(OppoVolumeLevelResponse, OppoVolumeLevelMutator()),    
  OppoCode.QHD: ResponseMapping(OppoHdmiModeResponse, OppoSimpleDeviceMutator('mode', ATTR_DEVICE_HDMI_MODE)),
  OppoCode.SHD: ResponseMapping(OppoHdmiModeResponse, OppoSimpleDeviceMutator('mode', ATTR_DEVICE_HDMI_MODE)),
  OppoCode.QPL: ResponseMapping(OppoPlayResponse, OppoSimpleDeviceMutator('status',ATTR_DEVICE_PLAYBACK_STATUS)),
  OppoCode.UPL: ResponseMapping(OppoUpdatePlayStatusResponse, OppoUpdatePlayStatusMutator()),
  OppoCode.QTK: ResponseMapping(OppoCurrentTotalResponse, OppoTrackTotalMutator()),
  OppoCode.QCH: ResponseMapping(OppoCurrentTotalResponse, OppoChapterTotalMutator()),
  OppoCode.QDT: ResponseMapping(OppoDiscTypeResponse, OppoSimpleDeviceMutator('disc_type', ATTR_DEVICE_DISC_TYPE)),
  OppoCode.UDT: ResponseMapping(OppoUpdateDiscTypeResponse, OppoSimpleDeviceMutator('disc_type', ATTR_DEVICE_DISC_TYPE)),
  OppoCode.QSH: ResponseMapping(OppoIntResponse, OppoSimpleDeviceMutator('value', ATTR_DEVICE_SUBTITLE_SHIFT)),
  OppoCode.SSH: ResponseMapping(OppoIntResponse, OppoSimpleDeviceMutator('value', ATTR_DEVICE_SUBTITLE_SHIFT)),
  OppoCode.QOP: ResponseMapping(OppoIntResponse, OppoSimpleDeviceMutator('value', ATTR_DEVICE_OSD_POSITION)),
  OppoCode.SOP: ResponseMapping(OppoIntResponse, OppoSimpleDeviceMutator('value', ATTR_DEVICE_OSD_POSITION)),
  OppoCode.QZM: ResponseMapping(OppoRepeatModeResponse, OppoSimpleDeviceMutator('mode', ATTR_DEVICE_ZOOM_MODE)),
  OppoCode.SZM: ResponseMapping(OppoRepeatModeResponse, OppoSimpleDeviceMutator('mode', ATTR_DEVICE_ZOOM_MODE)),
  OppoCode.QHR: ResponseMapping(OppoHdrSettingResponse, OppoSimpleDeviceMutator('setting', ATTR_DEVICE_HDR_SETTING)),
  OppoCode.SHR: ResponseMapping(OppoHdrSettingResponse, OppoSimpleDeviceMutator('setting', ATTR_DEVICE_HDR_SETTING)),
  OppoCode.QIS: ResponseMapping(OppoInputSourceResponse, OppoSimpleDeviceMutator('source', ATTR_DEVICE_INPUT_SOURCE)),
  OppoCode.SIS: ResponseMapping(OppoInputSourceResponse, OppoSimpleDeviceMutator('source', ATTR_DEVICE_INPUT_SOURCE)),
  OppoCode.UIS: ResponseMapping(OppoInputSourceResponse, OppoSimpleDeviceMutator('source', ATTR_DEVICE_INPUT_SOURCE)),
  OppoCode.QC1: ResponseMapping(OppoStringResponse, OppoSimpleDeviceMutator('value', ATTR_DEVICE_CDDB_ID_1)),
  OppoCode.QC2: ResponseMapping(OppoStringResponse, OppoSimpleDeviceMutator('value', ATTR_DEVICE_CDDB_ID_2)),
 
  OppoCode.QTE: ResponseMapping(OppoTimeResponse, OppoSimplePlaybackMutator('value', ATTR_PLAYBACK_TRACK_ELAPSED_TIME)),
  OppoCode.QTR: ResponseMapping(OppoTimeResponse, OppoSimplePlaybackMutator('value', ATTR_PLAYBACK_TRACK_REMAINING_TIME)),
  OppoCode.QCE: ResponseMapping(OppoTimeResponse, OppoSimplePlaybackMutator('value', ATTR_PLAYBACK_CHAPTER_ELAPSED_TIME)),
  OppoCode.QCR: ResponseMapping(OppoTimeResponse, OppoSimplePlaybackMutator('value', ATTR_PLAYBACK_CHAPTER_REMAINING_TIME)),
  OppoCode.QEL: ResponseMapping(OppoTimeResponse, OppoSimplePlaybackMutator('value', ATTR_PLAYBACK_TOTAL_ELAPSED_TIME)),
  OppoCode.QRE: ResponseMapping(OppoTimeResponse, OppoSimplePlaybackMutator('value', ATTR_PLAYBACK_TOTAL_REMAINING_TIME)),
  OppoCode.QAT: ResponseMapping(OppoStringResponse, OppoSimplePlaybackMutator('value', ATTR_PLAYBACK_AUDIO_TYPE)),
  OppoCode.UAT: ResponseMapping(OppoStringResponse, OppoSimplePlaybackMutator('value', ATTR_PLAYBACK_AUDIO_TYPE)),
  OppoCode.QST: ResponseMapping(OppoStringResponse, OppoSimplePlaybackMutator('value', ATTR_PLAYBACK_SUBTITLE_TYPE)),
  OppoCode.UST: ResponseMapping(OppoStringResponse, OppoSimplePlaybackMutator('value', ATTR_PLAYBACK_SUBTITLE_TYPE)),
  OppoCode.QRP: ResponseMapping(OppoRepeatModeResponse, OppoSimplePlaybackMutator('mode', ATTR_PLAYBACK_REPEAT_MODE)),
  OppoCode.SRP: ResponseMapping(OppoRepeatModeResponse, OppoSimplePlaybackMutator('mode', ATTR_PLAYBACK_REPEAT_MODE)),
  OppoCode.Q3D: ResponseMapping(OppoVideo3dStatusResponse, OppoSimplePlaybackMutator('status', ATTR_PLAYBACK_VIDEO_3D_STATUS)),
  OppoCode.U3D: ResponseMapping(OppoVideo3dStatusResponse, OppoSimplePlaybackMutator('status', ATTR_PLAYBACK_VIDEO_3D_STATUS)),
  OppoCode.QHS: ResponseMapping(OppoVideoHdrStatusResponse, OppoSimplePlaybackMutator('status', ATTR_PLAYBACK_VIDEO_HDR_STATUS)),
  OppoCode.QFT: ResponseMapping(OppoStringResponse, OppoSimplePlaybackMutator('value', ATTR_PLAYBACK_MEDIA_FILE_FORMAT)),
  OppoCode.QFN: ResponseMapping(OppoStringResponse, OppoSimplePlaybackMutator('value', ATTR_PLAYBACK_MEDIA_FILE_NAME)),
  OppoCode.QTN: ResponseMapping(OppoStringResponse, OppoSimplePlaybackMutator('value', ATTR_PLAYBACK_TRACK_NAME)),
  OppoCode.QTA: ResponseMapping(OppoStringResponse, OppoSimplePlaybackMutator('value', ATTR_PLAYBACK_TRACK_ALBUM)),
  OppoCode.QTP: ResponseMapping(OppoStringResponse, OppoSimplePlaybackMutator('value', ATTR_PLAYBACK_TRACK_PERFORMER)),
  OppoCode.QAR: ResponseMapping(OppoStringResponse, OppoSimplePlaybackMutator('value', ATTR_PLAYBACK_ASPECT_RATIO)),
  OppoCode.UAR: ResponseMapping(OppoStringResponse, OppoSimplePlaybackMutator('value', ATTR_PLAYBACK_ASPECT_RATIO)),

  OppoCode.EJT: ResponseMapping(OppoTrayStatusResponse, OppoTrayStatusMutator()),
  OppoCode.REV: ResponseMapping(OppoSpeedModeResponse, OppoSimplePlaybackMutator('mode', ATTR_PLAYBACK_REV_SPEED)),
  OppoCode.FWD: ResponseMapping(OppoSpeedModeResponse, OppoSimplePlaybackMutator('mode', ATTR_PLAYBACK_FWD_SPEED)),
  OppoCode.FWD: ResponseMapping(OppoStringResponse, OppoSimplePlaybackMutator('value', ATTR_PLAYBACK_CAMERA_ANGLE)),
  OppoCode.ATB: ResponseMapping(OppoStringResponse, OppoSimplePlaybackMutator('value', ATTR_PLAYBACK_ATB_REPLAY)),

  OppoCode.UTC: ResponseMapping(OppoUpdateTimeResponse, OppoUpdateTimeMutator()),
}
