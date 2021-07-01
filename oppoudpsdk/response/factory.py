from typing import Any, Tuple, Type
from ..const import *
from .response import *
from .mutator import *

class ResponseMapping(NamedTuple):
  response_type: Type
  mutator: OppoStateMutator

def get_response(message: bytes) -> OppoResponse:
  parsed = _parse_message(message)
  try:
    if parsed.code in _MAPPING:
      mapping =_MAPPING[parsed.code]
      return mapping.response_type(parsed, mapping.mutator, message)
  except:
    pass

  return OppoResponse(parsed, OppoNopMutator(), message) 

def _parse_message(message: bytes) -> OppoParsedResponse:
  decoded = message.decode()

  try:
    segments = decoded[:-1].split(" ")
    
    p_code = segments[0][1:]
    #update codes don't have a result...
    if p_code.startswith('U'):
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

_MAPPING = {
  OppoCode.QPW.value: ResponseMapping(OppoPowerResponse, OppoSimpleDeviceMutator('status',ATTR_DEVICE_POWER_STATUS)),
  OppoCode.PON.value: ResponseMapping(OppoPowerResponse, OppoSimpleDeviceMutator('status',ATTR_DEVICE_POWER_STATUS)),
  OppoCode.POF.value: ResponseMapping(OppoPowerResponse, OppoSimpleDeviceMutator('status',ATTR_DEVICE_POWER_STATUS)),
  OppoCode.POW.value: ResponseMapping(OppoPowerResponse, OppoSimpleDeviceMutator('status',ATTR_DEVICE_POWER_STATUS)),
  OppoCode.UPW.value: ResponseMapping(OppoUpdatePowerStatusResponse, OppoNopMutator()),

  OppoCode.QVM.value: ResponseMapping(OppoIntResponse, OppoNopMutator()),
  OppoCode.SVM.value: ResponseMapping(OppoIntResponse, OppoNopMutator()),
  OppoCode.QVR.value: ResponseMapping(OppoStringResponse, OppoSimpleDeviceMutator('value', ATTR_DEVICE_FIRMWARE_VERSION)),
  OppoCode.QVL.value: ResponseMapping(OppoVolumeLevelResponse, OppoVolumeLevelMutator()),  
  OppoCode.SVL.value: ResponseMapping(OppoVolumeLevelResponse, OppoVolumeLevelMutator()),  
  OppoCode.MUT.value: ResponseMapping(OppoVolumeLevelResponse, OppoVolumeLevelMutator()),    
  OppoCode.VUP.value: ResponseMapping(OppoVolumeLevelResponse, OppoVolumeLevelMutator()),    
  OppoCode.VDN.value: ResponseMapping(OppoVolumeLevelResponse, OppoVolumeLevelMutator()),    
  OppoCode.QHD.value: ResponseMapping(OppoHdmiModeResponse, OppoSimpleDeviceMutator('mode', ATTR_DEVICE_HDMI_MODE)),
  OppoCode.SHD.value: ResponseMapping(OppoHdmiModeResponse, OppoSimpleDeviceMutator('mode', ATTR_DEVICE_HDMI_MODE)),
  OppoCode.QPL.value: ResponseMapping(OppoPlayResponse, OppoSimpleDeviceMutator('status',ATTR_DEVICE_PLAYBACK_STATUS)),
  OppoCode.UPL.value: ResponseMapping(OppoUpdatePlayStatusResponse, OppoUpdatePlayStatusMutator()),
  OppoCode.QTK.value: ResponseMapping(OppoCurrentTotalResponse, OppoTrackTotalMutator()),
  OppoCode.QCH.value: ResponseMapping(OppoCurrentTotalResponse, OppoChapterTotalMutator()),
  OppoCode.QDT.value: ResponseMapping(OppoDiscTypeResponse, OppoSimpleDeviceMutator('disc_type', ATTR_DEVICE_DISC_TYPE)),
  OppoCode.UDT.value: ResponseMapping(OppoUpdateDiscTypeResponse, OppoSimpleDeviceMutator('disc_type', ATTR_DEVICE_DISC_TYPE)),
  OppoCode.QSH.value: ResponseMapping(OppoIntResponse, OppoSimpleDeviceMutator('value', ATTR_DEVICE_SUBTITLE_SHIFT)),
  OppoCode.SSH.value: ResponseMapping(OppoIntResponse, OppoSimpleDeviceMutator('value', ATTR_DEVICE_SUBTITLE_SHIFT)),
  OppoCode.QOP.value: ResponseMapping(OppoIntResponse, OppoSimpleDeviceMutator('value', ATTR_DEVICE_OSD_POSITION)),
  OppoCode.SOP.value: ResponseMapping(OppoIntResponse, OppoSimpleDeviceMutator('value', ATTR_DEVICE_OSD_POSITION)),
  OppoCode.QZM.value: ResponseMapping(OppoRepeatModeResponse, OppoSimpleDeviceMutator('mode', ATTR_DEVICE_ZOOM_MODE)),
  OppoCode.SZM.value: ResponseMapping(OppoRepeatModeResponse, OppoSimpleDeviceMutator('mode', ATTR_DEVICE_ZOOM_MODE)),
  OppoCode.QHR.value: ResponseMapping(OppoHdrSettingResponse, OppoSimpleDeviceMutator('setting', ATTR_DEVICE_HDR_SETTING)),
  OppoCode.SHR.value: ResponseMapping(OppoHdrSettingResponse, OppoSimpleDeviceMutator('setting', ATTR_DEVICE_HDR_SETTING)),
  OppoCode.QIS.value: ResponseMapping(OppoInputSourceResponse, OppoSimpleDeviceMutator('source', ATTR_DEVICE_INPUT_SOURCE)),
  OppoCode.SIS.value: ResponseMapping(OppoInputSourceResponse, OppoSimpleDeviceMutator('source', ATTR_DEVICE_INPUT_SOURCE)),
  OppoCode.UIS.value: ResponseMapping(OppoInputSourceResponse, OppoSimpleDeviceMutator('source', ATTR_DEVICE_INPUT_SOURCE)),
  OppoCode.QC1.value: ResponseMapping(OppoStringResponse, OppoSimpleDeviceMutator('value', ATTR_DEVICE_CDDB_ID_1)),
  OppoCode.QC2.value: ResponseMapping(OppoStringResponse, OppoSimpleDeviceMutator('value', ATTR_DEVICE_CDDB_ID_2)),
 
  OppoCode.QTE.value: ResponseMapping(OppoTimeResponse, OppoSimplePlaybackMutator('value', ATTR_PLAYBACK_TRACK_ELAPSED_TIME)),
  OppoCode.QTR.value: ResponseMapping(OppoTimeResponse, OppoSimplePlaybackMutator('value', ATTR_PLAYBACK_TRACK_REMAINING_TIME)),
  OppoCode.QCE.value: ResponseMapping(OppoTimeResponse, OppoSimplePlaybackMutator('value', ATTR_PLAYBACK_CHAPTER_ELAPSED_TIME)),
  OppoCode.QCR.value: ResponseMapping(OppoTimeResponse, OppoSimplePlaybackMutator('value', ATTR_PLAYBACK_CHAPTER_REMAINING_TIME)),
  OppoCode.QEL.value: ResponseMapping(OppoTimeResponse, OppoSimplePlaybackMutator('value', ATTR_PLAYBACK_TOTAL_ELAPSED_TIME)),
  OppoCode.QRE.value: ResponseMapping(OppoTimeResponse, OppoSimplePlaybackMutator('value', ATTR_PLAYBACK_TOTAL_REMAINING_TIME)),
  OppoCode.QAT.value: ResponseMapping(OppoStringResponse, OppoSimplePlaybackMutator('value', ATTR_PLAYBACK_AUDIO_TYPE)),
  OppoCode.UAT.value: ResponseMapping(OppoStringResponse, OppoSimplePlaybackMutator('value', ATTR_PLAYBACK_AUDIO_TYPE)),
  OppoCode.QST.value: ResponseMapping(OppoStringResponse, OppoSimplePlaybackMutator('value', ATTR_PLAYBACK_SUBTITLE_TYPE)),
  OppoCode.UST.value: ResponseMapping(OppoStringResponse, OppoSimplePlaybackMutator('value', ATTR_PLAYBACK_SUBTITLE_TYPE)),
  OppoCode.QRP.value: ResponseMapping(OppoRepeatModeResponse, OppoSimplePlaybackMutator('mode', ATTR_PLAYBACK_REPEAT_MODE)),
  OppoCode.SRP.value: ResponseMapping(OppoRepeatModeResponse, OppoSimplePlaybackMutator('mode', ATTR_PLAYBACK_REPEAT_MODE)),
  OppoCode.Q3D.value: ResponseMapping(OppoVideo3dStatusResponse, OppoSimplePlaybackMutator('status', ATTR_PLAYBACK_VIDEO_3D_STATUS)),
  OppoCode.U3D.value: ResponseMapping(OppoVideo3dStatusResponse, OppoSimplePlaybackMutator('status', ATTR_PLAYBACK_VIDEO_3D_STATUS)),
  OppoCode.QHS.value: ResponseMapping(OppoVideoHdrStatusResponse, OppoSimplePlaybackMutator('status', ATTR_PLAYBACK_VIDEO_HDR_STATUS)),
  OppoCode.QFT.value: ResponseMapping(OppoStringResponse, OppoSimplePlaybackMutator('value', ATTR_PLAYBACK_MEDIA_FILE_FORMAT)),
  OppoCode.QFN.value: ResponseMapping(OppoStringResponse, OppoSimplePlaybackMutator('value', ATTR_PLAYBACK_MEDIA_FILE_NAME)),
  OppoCode.QTN.value: ResponseMapping(OppoStringResponse, OppoSimplePlaybackMutator('value', ATTR_PLAYBACK_TRACK_NAME)),
  OppoCode.QTA.value: ResponseMapping(OppoStringResponse, OppoSimplePlaybackMutator('value', ATTR_PLAYBACK_TRACK_ALBUM)),
  OppoCode.QTP.value: ResponseMapping(OppoStringResponse, OppoSimplePlaybackMutator('value', ATTR_PLAYBACK_TRACK_PERFORMER)),
  OppoCode.QAR.value: ResponseMapping(OppoStringResponse, OppoSimplePlaybackMutator('value', ATTR_PLAYBACK_ASPECT_RATIO)),
  OppoCode.UAR.value: ResponseMapping(OppoStringResponse, OppoSimplePlaybackMutator('value', ATTR_PLAYBACK_ASPECT_RATIO)),

  OppoCode.EJT.value: ResponseMapping(OppoTrayStatusResponse, OppoTrayStatusMutator()),
  OppoCode.REV.value: ResponseMapping(OppoSpeedModeResponse, OppoSimplePlaybackMutator('mode', ATTR_PLAYBACK_REV_SPEED)),
  OppoCode.FWD.value: ResponseMapping(OppoSpeedModeResponse, OppoSimplePlaybackMutator('mode', ATTR_PLAYBACK_FWD_SPEED)),
  OppoCode.FWD.value: ResponseMapping(OppoStringResponse, OppoSimplePlaybackMutator('value', ATTR_PLAYBACK_CAMERA_ANGLE)),
  OppoCode.ATB.value: ResponseMapping(OppoStringResponse, OppoSimplePlaybackMutator('value', ATTR_PLAYBACK_ATB_REPLAY)),

  OppoCode.UTC.value: ResponseMapping(OppoUpdateTimeResponse, OppoUpdateTimeMutator()),
}
