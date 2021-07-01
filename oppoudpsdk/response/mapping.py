from .enums import *

_UPDATE_PLAY_STATUS_TO_PLAY_STATUS = {
  UpdatePlayStatus.PLAY: PlayStatus.PLAY,
  UpdatePlayStatus.PAUSED: PlayStatus.PAUSE,
  UpdatePlayStatus.STOPPED: PlayStatus.STOP,
  UpdatePlayStatus.STP_FWD: PlayStatus.SLOW_FORWARD,
  UpdatePlayStatus.STP_REV: PlayStatus.SLOW_REVERSE,
  UpdatePlayStatus.FFWD_1: PlayStatus.FAST_FORWARD,
  UpdatePlayStatus.FFWD_2: PlayStatus.FAST_FORWARD,
  UpdatePlayStatus.FFWD_3: PlayStatus.FAST_FORWARD,
  UpdatePlayStatus.FFWD_4: PlayStatus.FAST_FORWARD,
  UpdatePlayStatus.FFWD_5: PlayStatus.FAST_FORWARD,
  UpdatePlayStatus.FREV_1: PlayStatus.FAST_REVERSE,
  UpdatePlayStatus.FREV_2: PlayStatus.FAST_REVERSE,
  UpdatePlayStatus.FREV_3: PlayStatus.FAST_REVERSE,
  UpdatePlayStatus.FREV_4: PlayStatus.FAST_REVERSE,
  UpdatePlayStatus.FREV_5: PlayStatus.FAST_REVERSE,
  UpdatePlayStatus.SFWD_1: PlayStatus.SLOW_FORWARD,
  UpdatePlayStatus.SFWD_2: PlayStatus.SLOW_FORWARD,
  UpdatePlayStatus.SFWD_3: PlayStatus.SLOW_FORWARD,
  UpdatePlayStatus.SFWD_4: PlayStatus.SLOW_FORWARD,
  UpdatePlayStatus.SFWD_5: PlayStatus.SLOW_FORWARD,
  UpdatePlayStatus.SREV_1: PlayStatus.SLOW_REVERSE,
  UpdatePlayStatus.SREV_2: PlayStatus.SLOW_REVERSE,
  UpdatePlayStatus.SREV_3: PlayStatus.SLOW_REVERSE,
  UpdatePlayStatus.SREV_4: PlayStatus.SLOW_REVERSE,
  UpdatePlayStatus.SREV_5: PlayStatus.SLOW_REVERSE,
  UpdatePlayStatus.HOME: PlayStatus.HOME_MENU,
  UpdatePlayStatus.MEDIA_CENTER: PlayStatus.MEDIA_CENTER,
  UpdatePlayStatus.SCREEN_SAVER: PlayStatus.SCREEN_SAVER,
  UpdatePlayStatus.DISC_MENU:  PlayStatus.DISC_MENU
}

_UPDATE_PLAY_STATUS_TO_TRAY_STATUS = {
  UpdatePlayStatus.NO_DISC: TrayStatus.CLOSE,
  UpdatePlayStatus.LOADING: TrayStatus.CLOSE,
  UpdatePlayStatus.TRAY_OPEN: TrayStatus.OPEN,
  UpdatePlayStatus.TRAY_CLOSING: TrayStatus.CLOSE
}

_UPDATE_PLAY_STATUS_TO_SPEED_MODE = {
  UpdatePlayStatus.STP_FWD: SpeedMode.STEP,
  UpdatePlayStatus.STP_REV: SpeedMode.STEP,
  UpdatePlayStatus.FFWD_1: SpeedMode.NORMAL,
  UpdatePlayStatus.FFWD_2: SpeedMode.FAST_2,
  UpdatePlayStatus.FFWD_3: SpeedMode.FAST_3,
  UpdatePlayStatus.FFWD_4: SpeedMode.FAST_4,
  UpdatePlayStatus.FFWD_5: SpeedMode.FAST_5,
  UpdatePlayStatus.FREV_1: SpeedMode.NORMAL,
  UpdatePlayStatus.FREV_2: SpeedMode.FAST_2,
  UpdatePlayStatus.FREV_3: SpeedMode.FAST_3,
  UpdatePlayStatus.FREV_4: SpeedMode.FAST_4,
  UpdatePlayStatus.FREV_5: SpeedMode.FAST_5,
  UpdatePlayStatus.SFWD_1: SpeedMode.SLOW_1_2,
  UpdatePlayStatus.SFWD_2: SpeedMode.SLOW_1_4,
  UpdatePlayStatus.SFWD_3: SpeedMode.SLOW_1_8,
  UpdatePlayStatus.SFWD_4: SpeedMode.SLOW_1_16,
  UpdatePlayStatus.SFWD_5: SpeedMode.SLOW_1_32,
  UpdatePlayStatus.SREV_1: SpeedMode.SLOW_1_2,
  UpdatePlayStatus.SREV_2: SpeedMode.SLOW_1_4,
  UpdatePlayStatus.SREV_3: SpeedMode.SLOW_1_8,
  UpdatePlayStatus.SREV_4: SpeedMode.SLOW_1_16,
  UpdatePlayStatus.SREV_5: SpeedMode.SLOW_1_32,
}

_UPDATE_DISC_TYPE_TO_DISC_TYPE = {
  UpdateDiscType.UNKNOWN: DiscType.UNKNOWN,
  UpdateDiscType.BLURAY: DiscType.BLURAY,
  UpdateDiscType.DVD_VIDEO: DiscType.DVD_VIDEO,
  UpdateDiscType.DVD_AUDIO: DiscType.DVD_AUDIO,
  UpdateDiscType.SACD: DiscType.SACD,
  UpdateDiscType.CDDA: DiscType.CDDA,
  UpdateDiscType.UHD_BLURAY: DiscType.UHD_BLURAY,
  UpdateDiscType.DATA: DiscType.DATA,
  UpdateDiscType.VCD2: DiscType.VCD2,
  UpdateDiscType.SVCD: DiscType.SVCD
}