""" 
    Autor: Maier-Lohmann, Rainer
"""

# -----------------------------------------------------------------------------
# Klasse zur Verwaltung eines Maerklin CANbus Datenframes
# -----------------------------------------------------------------------------
class McanMsgArray():
  __bytenames = [ 'prio', 'cmdAndResp'
                , 'hashH', 'hashL'
                , 'dlc'
                , 'd0', 'd1', 'd2', 'd3'
                , 'd4', 'd5', 'd6', 'd7'
                ]

  def __init__(self, canMsgArr=None):
    if canMsgArr is None:
      self.__canMsgArr = [0,0,0,0,0,0,0,0,0,0,0,0,0]
    else:
      self.__canMsgArr = canMsgArr

  def __str__(self):
    out = ''
    for msgByte in self.__canMsgArr:
      out += '{:02x} '.format(msgByte)
    return out

  def __repr__(self):
    out =''
    for i in range (0,5,1):
     out += '{}={:02x} '.format(self.__bytenames[i]
                               , self.__canMsgArr[i])
    out += 'data='
    for i in range (5,13,1):
      out += '{:02x} '.format(self.__canMsgArr[i])
    return out

  @property
  def bytenames(self):
    return self.__bytenames

  @property
  def array(self):
    return self.__canMsgArr

  def getByte(self, byteName):
    return self.__canMsgArr[self.__bytenames.index(byteName)]

  def setByte(self, byteName, val):
    self.__canMsgArr[self.__bytenames.index(byteName)] = val
