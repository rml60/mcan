""" mcancommand.py

    Author: Rainer Maier-Lohmann
    ---------------------------------------------------------------------------
    "THE BEER-WARE LICENSE" (Revision 42):
    <r.m-l@gmx.de> wrote this file.  As long as you retain this notice you
    can do whatever you want with this stuff. If we meet some day, and you 
    think this stuff is worth it, you can buy me a beer in return.
    ---------------------------------------------------------------------------
    (c) 2020
"""
from .mcanmsgarray import McanMsgArray

# -----------------------------------------------------------------------------
# Klasse zur Verwaltung eines Maerklin CANbus Befehls
# -----------------------------------------------------------------------------
class McanCommand(McanMsgArray):
  """ Klasse zur Verwaltung eines Maerklin CANbus Befehls
  """
  def __init__(self, mcanHash):
    super().__init__()
    self.setHash(mcanHash)

  @property
  def frame(self):
    """ Liefert den can-Datenrahmen als 13-byte-langes bytearray
    """
    return bytearray(self.array)

  @property
  def response(self):
    """ Liefert den can-Datenrahmen als 13-byte-langes bytearray mit
        aktiviertem Antwortbit.
    """
    response = McanMsgArray(self.frame)
    response.setByte('cmdAndResp', response.getByte('cmdAndResp')|0x01)
    return bytearray(response.array)

  def setPrio(self, prio):
    """ Setzt das prio-Byte im can-Datenrahmen
    """
    self.setByName(prio, 'prio')

  def setCommand(self, cmd, response=False, dlc=8 ):
    """ Setzt das Befehls-Byte im can-Datenrahmen
    """
    if response:
      cmd += 1
    self.setByte('cmdAndResp', cmd)
    self.setDlc(dlc)

  def setHash(self, mcanHash):
    """ Setzt die beiden Hash-Bytes im can-Datenrahmen
    """
    self.setByte('hashH', mcanHash >> 8)
    self.setByte('hashL', mcanHash & 0xff)

  def setDlc(self, dlc):
    """ Setzt das dlc-Byte im can-Datenrahmen
        data len count
    """
    self.setByte('dlc', dlc)

  def setDevice(self, devId, subId):
    """ Setzt die 4 ersten Datenbytes im can-Datenrahmen
    """
    self.setByte('d0', devId >> 8)
    self.setByte('d1', devId & 0xff)
    self.setByte('d2', subId >> 8)
    self.setByte('d3', subId & 0xff)

  def toggleTrackState(self, devId=None, subId=None, newState=None):
    """ deprecated: recentState wird nicht pro subId gespeichert 
                    Es ist sicherer setTrackState zu nutzen.
        Setzt das Status-Byte (Rueckmelder)
        Der letzte(recent) Status wird entsprechend gesetzt.
    """
    if devId is not None and subId is not None:
      self.setDevice(devId, subId)
    self.setByte('d4', self.getByte('d5'))
    if newState is None:
      self.setByte('d5', self.getByte('d5') ^ 0x01)
    else:
      self.setByte('d5', newState)

  def setTrackState(self, devId, subId, state, recentState):
    """ Setzt die Status-Bytes (Rueckmelder)

    """
    self.setDevice(devId, subId)
    self.setByte('d4', recentState)
    self.setByte('d5', state)

