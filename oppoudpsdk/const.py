MAX_RETRIES = 3
RETRY_INTERVAL = 2

#occurs when the client is connected
EVENT_CONNECTED = "connected"
#occurs when the client is disconnected
EVENT_DISCONNECTED = "disconnected"
#occurs when the client state has changed
EVENT_STATE_CHANGED = "state_changed"
#occurs when the client is ready
EVENT_READY = "ready"
#occurs when the client receives a message
EVENT_MESSAGE_RECEIVED = "message_received"
#occurs when a command is about to be sent to the device
EVENT_COMMAND_SENDING = "command_sending"
#occurs when a command has been sent to the device
EVENT_COMMAND_SENT = "command_sent"
#occurs when the command response has been received
EVENT_COMMAND_RESPONSE = "command_response"
#occurs when the command processing has been completed
EVENT_COMMAND_COMPLETE = "command_complete"
#occurs when the device is updating
EVENT_DEVICE_STATE_UPDATING = "device_state_updating"
#occurs after the device state has been updated
EVENT_DEVICE_STATE_UPDATED = "device_state_updated"
#occurs when the disc id changes
EVENT_DISC_ID_CHANGED = "disc_changed"

#per Oppo documentation, assume 10 second timeout
COMMAND_TIMEOUT = 10

ATTR_DEVICE_FIRMWARE_VERSION = "firmware_version"
ATTR_DEVICE_IS_MUTED = "is_muted"
ATTR_DEVICE_VOLUME = "volume"
ATTR_DEVICE_HDMI_MODE = "hdmi_mode"
ATTR_DEVICE_SUBTITLE_SHIFT = "subtitle_shift"
ATTR_DEVICE_OSD_POSITION = "osd_position"
ATTR_DEVICE_INPUT_SOURCE = "input_source"
ATTR_DEVICE_ZOOM_MODE = "zoom_mode"
ATTR_DEVICE_HDR_SETTING = "hdr_setting"
ATTR_DEVICE_DISC_TYPE = "disc_type"
ATTR_DEVICE_PLAYBACK_STATUS = "playback_status"
ATTR_DEVICE_POWER_STATUS = "power_status"
ATTR_DEVICE_CDDB_ID_1 = 'cddb_id_1'
ATTR_DEVICE_CDDB_ID_2 = 'cddb_id_2'
ATTR_DEVICE_CDDB_ID = "cddb_id"

ATTR_PLAYBACK_TRACK = "track"
ATTR_PLAYBACK_TRACK_TOTAL = "track_total"
ATTR_PLAYBACK_CHAPTER = "chapter"
ATTR_PLAYBACK_CHAPTER_TOTAL = "chapter_total"
ATTR_PLAYBACK_TRACK_ELAPSED_TIME = "track_elapsed_time"
ATTR_PLAYBACK_TRACK_REMAINING_TIME = "track_remaining_time"
ATTR_PLAYBACK_TRACK_DURATION = "track_duration"
ATTR_PLAYBACK_CHAPTER_ELAPSED_TIME = "chapter_elapsed_time"
ATTR_PLAYBACK_CHAPTER_REMAINING_TIME = "chapter_remaining_time"
ATTR_PLAYBACK_CHAPTER_DURATION = "chapter_duration"
ATTR_PLAYBACK_TOTAL_ELAPSED_TIME = "total_elapsed_time"
ATTR_PLAYBACK_TOTAL_REMAINING_TIME = "total_remaining_time"
ATTR_PLAYBACK_TOTAL_DURATION = "total_duration"
ATTR_PLAYBACK_AUDIO_TYPE = "audio_type"
ATTR_PLAYBACK_SUBTITLE_TYPE = "subtitle_type"
ATTR_PLAYBACK_ASPECT_RATIO = "aspect_ratio"
ATTR_PLAYBACK_REPEAT_MODE = "repeat_mode"
ATTR_PLAYBACK_VIDEO_3D_STATUS = "video_3d_status"
ATTR_PLAYBACK_VIDEO_HDR_STATUS = "video_hdr_status"
ATTR_PLAYBACK_MEDIA_FILE_FORMAT = "media_file_format"
ATTR_PLAYBACK_MEDIA_FILE_NAME = "media_file_name"
ATTR_PLAYBACK_TRACK_NAME = "track_name"
ATTR_PLAYBACK_TRACK_ALBUM = "track_album"
ATTR_PLAYBACK_TRACK_PERFORMER = "track_performer"
ATTR_PLAYBACK_REV_SPEED = "rev_speed"
ATTR_PLAYBACK_FWD_SPEED = "fwd_speed"
ATTR_PLAYBACK_CAMERA_ANGLE = "camera_angle"
ATTR_PLAYBACK_ZOOM_RATIO = "zoom_ratio"
ATTR_PLAYBACK_ATB_REPLAY = "atb_replay"