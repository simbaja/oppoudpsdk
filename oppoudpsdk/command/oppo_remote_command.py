from ..codes import OppoRemoteCode, OppoRemoteCodeType, OppoCode, OppoCodeType
from .oppo_command import OppoCommand

class OppoRemoteCommand(OppoCommand):
  def __init__(self, code: OppoRemoteCodeType):      
      super().__init__(code)

  def _translate(self, code: OppoRemoteCodeType):
      if isinstance(code, str):
        return OppoCode(OppoRemoteCode(code).value)
      return OppoCode(code.value)