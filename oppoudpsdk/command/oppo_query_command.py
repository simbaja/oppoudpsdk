from typing import List
from ..codes import OppoQueryCode, OppoQueryCodeType, OppoCode, OppoCodeType
from .oppo_command import OppoCommand

class OppoQueryCommand(OppoCommand):
  def __init__(self, code: OppoQueryCodeType, parameters: List[str] = [], response_codes: List[str] = []):      
      super().__init__(code, parameters, response_codes)

  def _translate(self, code: OppoQueryCodeType):
      if isinstance(code, str):
        return OppoCode(OppoQueryCode(code).value)
      return OppoCode(code.value)

class OppoQueryCdCommand(OppoQueryCommand):
  def __init__(self):
      super().__init__(OppoQueryCode.QCD, [], ["QC2"] )

class OppoQueryDirectoryCommand(OppoQueryCommand):
  def __init__(self, item: int):
      super().__init__(OppoQueryCode.QDR, [item])
      