""" states.py

    Author: Rainer Maier-Lohmann
    ---------------------------------------------------------------------------
    "THE BEER-WARE LICENSE" (Revision 42):
    <r.m-l@gmx.de> wrote this file.  As long as you retain this notice you
    can do whatever you want with this stuff. If we meet some day, and you 
    think this stuff is worth it, you can buy me a beer in return.
    ---------------------------------------------------------------------------
    (C) 2021
"""

class States():
  """ class for management of state-bits
  """
  def __init__(self, maxStateBits = 16):
    self.__maxStateBits = maxStateBits
    self.__recentStates = 0
    self.__states = 0
    self.__changed = False
    #self.__isNotSend = True

  def __str__(self):
    """ string-output of states
    """
    out = ''
    for stateBit in range(1, self.__maxStateBits+1, 1):
      tmpState, tmpRecentState = self.getStateBit(stateBit)
      out += 'stateBit: {:>2}   state: {}  recent: {}\n'.format(stateBit, tmpState, tmpRecentState)
    return out

  def getStateBit(self, stateBit):
    """ returns a tupple with recentState and state for the stateNo
    """
    state = (self.__states>>stateBit)&1
    recentState = (self.__recentStates>>stateBit)&1
    return (state, recentState)

  def reset(self):
    """ reset all statebits to off
    """
    self.__recentStates = 0
    self.__states = 0

  def setStateBit(self, stateBit, value):
    """ set the state of the given stateBit
    """
    if value != 0:
      self.__states |= 2**stateBit
    else:
      self.__states &= 0xFFFF - 2**stateBit
    self.__changed = self.__recentStates != self.__states
    #self.__isNotSend = True

  def setStateBitOn(self, stateBit):
    """ set the state of the given stateBit On
    """
    self.setStateBit(stateBit,1)

  def setStateBitOff(self, stateBit):
    """ set the state of the given stateBit Off
    """
    self.setStateBit(stateBit,0)

  def setStateBits(self, states):
    """ set all state bits
    """
    for stateBit in range(1, self.__maxStateBits+1, 1):
      self.setStateBit(stateBit, (states>>(stateBit-1))&1)

  def setRecentToCurrent(self):
    """ set recentStates to current states
    """
    self.__recentStates = self.__states
    self.__changed = False

  @property
  def isChanged(self):
    """ Is one or more bit changed?
    """
    return self.__changed

  @property
  def changedStates(self):
    """ returns a list of changed stateBits
    """
    states = list()
    #if self.__isNotSend:
    for stateBit in range(1, self.__maxStateBits+1, 1):
      stateBitState, stateBitRecentState = self.getStateBit(stateBit)
      #currstateNoRecentState = (self.__recentStates>>stateNo)&1
      if stateBitState != stateBitRecentState:
        states.append([stateBit, stateBitState, stateBitRecentState] )
    #self.__recentStates = self.__states
    #self.__isNotSend = False
    return states

  @property
  def shortStr(self):
    """ returns a string with all states
        f.e.: 0101100000000001 - states 2,4,5 and 16 are on
    """
    shortStr = ''
    for stateBit in range(1, self.__maxStateBits+1, 1):
      shortStr += '{}'.format((self.__states>>stateBit)&1)
    return shortStr
