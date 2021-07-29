import asyncio
from asyncio.exceptions import InvalidStateError
import logging
from typing import Callable, DefaultDict, Dict, List, Optional, Tuple

from .codes import *
from .command import *
from .const import *
from .device import OppoDevice
from .exceptions import OppoCommandError, OppoInvalidStateError
from .response import *
from .states import OppoClientState
from .async_helpers import OppoStreamIterator, CancellableAsyncIterator

_LOGGER = logging.getLogger(__name__)

class OppoClient:
  """
  Creates a client that can communicate with an Oppo UDP-20x device.
  The command reference can be found at: http://download.oppodigital.com/UDP203/OPPO_UDP-20X_RS-232_and_IP_Control_Protocol.pdf
  
  Must supply the host/IP address and port (default 23).
  """
  def __init__(self, host_name: str, port_number: int = 23, mac_address: str = None, event_loop: Optional[asyncio.AbstractEventLoop] = None):
    self._host_name = host_name
    self._port_number = port_number
    self._loop = event_loop
    self._disconnect_requested = asyncio.Event()
    self._command_response_received = asyncio.Event()
    self._command_lock = asyncio.Lock()
    self._command_timeouts = 0
    self._retries_since_last_connect = -1
    self._has_successful_connect = False   
    self._state = OppoClientState.INITIALIZING
    self._reader = None
    self._writer = None
    self._initialize_event_handlers()
    self._device = OppoDevice(self, mac_address)

  @property
  def state(self) -> OppoClientState:
    """Gets the state of the client"""
    return self._state

  @property
  def loop(self) -> asyncio.AbstractEventLoop:
    """Gets the asyncio event loop"""
    if self._loop is None:
      self._loop = asyncio.get_event_loop()
    return self._loop

  @property
  def device(self) -> OppoDevice:
    """Gets the device associated with this client"""
    return self._device

  @property
  def connected(self) -> bool:
    """Indicates whether the client is in a connected state"""
    return self._state not in [OppoClientState.DISCONNECTING, OppoClientState.DISCONNECTED]

  @property
  def available(self) -> bool:
    """Indicates whether the client is available for sending/receiving commands"""
    return self._state == OppoClientState.CONNECTED

  @property
  def event_handlers(self) -> Dict[str, List[Callable]]:
    return self._event_handlers

  async def async_event(self, event: str, *args, **kwargs):
    """Trigger event callbacks sequentially"""
    for cb in self.event_handlers[event]:
      asyncio.ensure_future(cb(*args, **kwargs), loop=self.loop)

  def add_event_handler(self, event: str, callback: Callable, disposable: bool = False):
    """Adds an event handler to an event"""
    if disposable:
      raise NotImplementedError('Support for disposable callbacks not yet implemented')
    self.event_handlers[event].append(callback)

  def remove_event_handler(self, event: str, callback: Callable):
    """Removes an event handler for an event"""
    try:
      self.event_handlers[event].remove(callable)
    except:
      _LOGGER.warn(f"could not remove event handler {event}-{callable}")

  def clear_event_handlers(self):
    """Clears all non-internal event handlers"""
    self._initialize_event_handlers()

  async def async_run_client(self):
    """Runs the client in an event loop including auto-reconnects if the client drops."""
    #reset the disconnect event
    self._disconnect_requested.clear()

    _LOGGER.info('Starting Oppo client')
    while not self._disconnect_requested.is_set():
      if self._retries_since_last_connect > MAX_RETRIES:
        _LOGGER.debug(f'Tried auto-reconnecting {MAX_RETRIES} times, giving up.')
        break
      try:
        await self._async_run_client()
      except OppoCommandError as err:
        _LOGGER.info(f'Error executing command {err}')
      except Exception as err:
        if not self._has_successful_connect:
          _LOGGER.warn(f'Unhandled exception before successful connect: {err}')
        _LOGGER.info(f'Unhandled exception while running client: {err}, ignoring and restarting', exc_info=True)  
      finally:
        if not self._disconnect_requested.is_set():
          await self._set_state(OppoClientState.DROPPED)
          await self._set_state(OppoClientState.WAITING)
          _LOGGER.debug('Waiting before reconnecting')
          await asyncio.sleep(RETRY_INTERVAL)
        self._retries_since_last_connect += 1

    #initiate the disconnection            
    await self.disconnect()

  async def disconnect(self):
    """Disconnect and cleanup."""
    if not self._disconnect_requested.is_set():
      _LOGGER.info("Disconnecting")
      await self._set_state(OppoClientState.DISCONNECTING)         
      self._disconnect_requested.set()
      await self._disconnect()
      await self._set_state(OppoClientState.DISCONNECTED)

  async def test_connection(self) -> bool:
    if self._state != OppoClientState.INITIALIZING:
      raise OppoInvalidStateError
    
    reader = None
    writer = None

    try:
      await self._set_state(OppoClientState.CONNECTING)
      reader, writer = await asyncio.open_connection(self._host_name, self._port_number)
    except:
      return False
    finally:
      if writer:
        writer.close()
        await writer.wait_closed()
    
    return True

  async def async_send_command(self, command: OppoCommand):
    """Sends a command to the client"""
    try:
      await self._send_command(command)
      self._command_timeouts = 0
    except asyncio.exceptions.TimeoutError:
      _LOGGER.debug("Timeout waiting for command response.")
      self._command_timeouts += 1
      if self._command_timeouts > MAX_TIMEOUTS:
        _LOGGER.warn("Multiple timeouts while waiting for command response, will disconnect and retry.")    
        asyncio.ensure_future(self.disconnect())

  async def _set_state(self, new_state: OppoClientState) -> bool:
    """Indicate that the state changed and raise an event"""
    if self._state != new_state:
      old_state = self._state
      self._state = new_state
      await self.async_event(EVENT_STATE_CHANGED, old_state, new_state)
      return True
    return False

  def _initialize_event_handlers(self):
    """Initializes the internal event handlers"""
    self._event_handlers = DefaultDict(list)  # type: Dict[str, List[Callable]]
    self.add_event_handler(EVENT_STATE_CHANGED, self._on_state_change)
    self.add_event_handler(EVENT_COMMAND_RESPONSE, self._on_command_response)
    pass

  async def _on_state_change(self, old_state: OppoClientState, new_state: OppoClientState):
    """Handles the on state change event"""
    _LOGGER.debug(f'Client changed state: {old_state} to {new_state}')

    if new_state == OppoClientState.CONNECTED:
      await self.async_event(EVENT_CONNECTED, self)
    if new_state == OppoClientState.DISCONNECTED:
      await self.async_event(EVENT_DISCONNECTED, self)

  async def _on_command_response(self, response: OppoResponse):
    """Handles a command response received event"""
    _LOGGER.debug(f'Received command response: {response}')
    self._current_command = None
    self._command_response_received.set()

  async def _set_connected(self):
    """Marks the client as connected"""
    self._retries_since_last_connect = -1
    self._has_successful_connect = True
    await self._set_state(OppoClientState.CONNECTED)

  async def _async_run_client(self):
    """Run the client (internal)."""
    try:
      await self._set_state(OppoClientState.CONNECTING)
      reader, writer = await asyncio.open_connection(self._host_name, self._port_number)
      self._reader = reader
      self._writer = writer

      await self._set_connected()
      self._initialize_device()
      try:
        async for message in CancellableAsyncIterator(OppoStreamIterator(reader), self._disconnect_requested):
          await self._process_message(message)
      except RuntimeError as err:
        #do nothing if it's a StopAsyncIteration, we just stopped the iteration
        #as part of the disconnect
        if not isinstance(err.__cause__, StopAsyncIteration):
          raise
    finally:
      await self._disconnect()    

  async def _disconnect(self) -> None:
    """Disconnects the client (internal)"""
    if self._writer:
      self._writer.close()
      await self._writer.wait_closed()

  def _initialize_device(self):
    """Initializes the device (gets power status, and triggers a future initialization)"""
    async def _async_initialize_device():   
      #query the power status to try to determine state
      await self.async_send_command(OppoQueryCommand(OppoQueryCode.QPW))
      #indicate we're ready to go
      await self.async_event(EVENT_READY, self)
    
    asyncio.ensure_future(_async_initialize_device())

  async def _send_command(self, command: OppoCommand):
    """Sends a command to the client (internal)"""
    _LOGGER.debug(f'Sending command: {command}')
    async with self._command_lock:
      await self.async_event(EVENT_COMMAND_SENDING, command)
      self._current_command = command.expected_response_codes
      self._command_response_received.clear()
      if self._writer:
        try:
          #write the command to the stream
          self._writer.write(command.encode())  
          await self._writer.drain()
          await self.async_event(EVENT_COMMAND_SENT, command)
        except ConnectionResetError:
          _LOGGER.info("Could not send command, connection reset.")
      await asyncio.wait_for(self._command_response_received.wait(), COMMAND_TIMEOUT)

  async def _process_message(self, message: bytes) -> OppoResponse:
    """Processes a message received from the Oppo server"""
    _LOGGER.debug(f'Received message: {message}')
    response = get_response(message)
    _LOGGER.debug(f'Parsed message: {response}')
    await self.async_event(EVENT_MESSAGE_RECEIVED, response)

    #if we're not in the right mode, we just need to assume that everything is good
    if response.raw_value[:3] in [b"@OK",b"@ER"] and self._current_command is not None:
      await self.async_event(EVENT_COMMAND_RESPONSE, response)
    #if this event paired to the current command, we need to indicate we've received
    #the response so that we can initiate more commands
    elif (
      self._current_command is not None and 
      isinstance(response.code, OppoCode) and 
      response.code.value in self._current_command
    ):
      await self.async_event(EVENT_COMMAND_RESPONSE, response)

    return response
