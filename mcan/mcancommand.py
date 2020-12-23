"""
"""
from .mcanmsgarray import McanMsgArray

# -----------------------------------------------------------------------------
# Klasse zur Verwaltung eines Maerklin CANbus Befehls
# -----------------------------------------------------------------------------
class McanCommand(McanMsgArray):
  def __init__(self, mcanHash):
    super().__init__()
    self.setHash(mcanHash)

  @property
  def frame(self):
    return bytearray(self.array)

  def setPrio(self, prio):
    self.setByName(prio, 'prio')

  def setCommand(self, cmd, response=False, dlc=8 ):
    if response:
      cmd += 1
    self.setByte('cmdAndResp', cmd)
    self.setDlc(dlc)

  def setHash(self, mcanHash):
    self.setByte('hashH', mcanHash >> 8)
    self.setByte('hashL', mcanHash & 0xff)

  def setDlc(self, dlc):
    """ data len count
    """
    self.setByte('dlc', dlc)

  def setTrackStateDevice(self, devId, subId):
    self.setByte('d0', devId >> 8)
    self.setByte('d1', devId & 0xff)
    self.setByte('d2', subId >> 8)
    self.setByte('d3', subId & 0xff)

  def toggleTrackState(self, newState=None):
    self.setByte('d4', self.getByte('d5'))
    if newState is None:
      self.setByte('d5', self.getByte('d5') ^ 0x01)
    else:
      self.setByte('d5', newState)
