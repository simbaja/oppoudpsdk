"""
Client example
"""

import asyncio
import logging
from datetime import timedelta
from oppoudpsdk.device import OppoDevice
from oppoudpsdk.const import EVENT_DEVICE_STATE_UPDATED, EVENT_MESSAGE_RECEIVED
from typing import Any, Dict, Tuple

from oppoudpsdk import (
  OppoClient
)

_LOGGER = logging.getLogger(__name__)

HOST_NAME = '10.0.30.27'

async def on_device_state_updated(device: OppoDevice):
  print(f'Status: {device.playback_status}')
  print(f'Chapter Number: {device.playback_attributes.chapter}')
  print(f'Chapter Elapsed: {device.playback_attributes.chapter_elapsed_time}')
  print(f'Chapter Remaining: {device.playback_attributes.chapter_remaining_time}')
  print(f'Total Elapsed: {device.playback_attributes.total_elapsed_time}')
  print(f'Total Remaining: {device.playback_attributes.total_remaining_time}')


async def main():
  logging.basicConfig(level=logging.DEBUG, format='%(asctime)-15s %(levelname)-8s %(message)s')

  loop = asyncio.get_event_loop()
  client = OppoClient(HOST_NAME, 23, loop)
  client.add_event_handler(EVENT_DEVICE_STATE_UPDATED, on_device_state_updated)
  await asyncio.ensure_future(client.async_run_client(), loop=loop)

if __name__ == "__main__":
  asyncio.run(main())
