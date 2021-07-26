"""
Client example.  Hooks the state updated event to show playback updates as they occur.
"""
import asyncio
import logging
from oppoudpsdk.const import EVENT_DISC_ID_CHANGED
from oppoudpsdk import EVENT_DEVICE_STATE_UPDATED, EVENT_READY
from oppoudpsdk import OppoClient, OppoDevice, SetVerboseMode, OppoSetVerboseModeCommand
from example.secrets import HOST_NAME

_LOGGER = logging.getLogger(__name__)

async def on_ready(client: OppoClient):
  await client.async_send_command(OppoSetVerboseModeCommand(SetVerboseMode.VERBOSE))

async def on_disc_id_changed(device: OppoDevice):
  print(f'New Disc ID: {device.cddb_id}')

async def on_device_state_updated(device: OppoDevice):
  print(f'Status: {device.playback_status}')
  print(f'Disc Type: {device.disc_type}')
  print(f'Disc ID: {device.cddb_id}')
  print(f'Track Number: {device.playback_attributes.track}')
  print(f'Track Name: {device.playback_attributes.track_name}')
  print(f'Track Elapsed: {device.playback_attributes.track_elapsed_time}')
  print(f'Track Remaining: {device.playback_attributes.track_remaining_time}')
  print(f'Track Duration: {device.playback_attributes.track_duration}')
  print(f'Chapter Number: {device.playback_attributes.chapter}')
  print(f'Chapter Elapsed: {device.playback_attributes.chapter_elapsed_time}')
  print(f'Chapter Remaining: {device.playback_attributes.chapter_remaining_time}')
  print(f'Chapter Duration: {device.playback_attributes.chapter_duration}')
  print(f'Total Elapsed: {device.playback_attributes.total_elapsed_time}')
  print(f'Total Remaining: {device.playback_attributes.total_remaining_time}')
  print(f'Total Duration: {device.playback_attributes.total_duration}')

async def main():
  logging.basicConfig(level=logging.DEBUG, format='%(asctime)-15s %(levelname)-8s %(message)s')

  loop = asyncio.get_event_loop()
  client = OppoClient(HOST_NAME, 23, loop)
  client.add_event_handler(EVENT_READY, on_ready)
  client.add_event_handler(EVENT_DEVICE_STATE_UPDATED, on_device_state_updated)
  client.add_event_handler(EVENT_DISC_ID_CHANGED, on_disc_id_changed)
  await asyncio.ensure_future(client.async_run_client(), loop=loop)

if __name__ == "__main__":
  asyncio.run(main())
