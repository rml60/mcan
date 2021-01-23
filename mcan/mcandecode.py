""" MCAN Modul
    Modul zur Verwaltung, Analyse und Ersstellung
    von Maerklin CAN-Bus Meldungen

    Author: Rainer Maier-Lohmann
    ---------------------------------------------------------------------------
    "THE BEER-WARE LICENSE" (Revision 42):
    <r.m-l@gmx.de> wrote this file.  As long as you retain this notice you
    can do whatever you want with this stuff. If we meet some day, and you 
    think this stuff is worth it, you can buy me a beer in return.
    ---------------------------------------------------------------------------
    (c) 2020
"""
from struct import unpack
from os import linesep

from .mcanmsgarray import McanMsgArray

# -----------------------------------------------------------------------------
# Klasse zur Analyse eines Maerklin CANbus Datenframes
# -----------------------------------------------------------------------------
class McanDecode(McanMsgArray):
  __commands = {  0 : 'System command'
               ,  2 : 'MFX Discovery'
               ,  4 : 'MFX Bind'
               ,  6 : 'MFX Verify'
               ,  8 : 'Loc speed'
               , 10 : 'Loc direction'
               , 12 : 'Loc function'
               , 14 : 'Loc read config'
               , 16 : 'Loc write config'
               , 22 : 'Equipment switch'
               , 34 : 'Track state'
               , 48 : 'Member ping'
               , 58 : 'Statusdata config'
               }
  __subcmds =  {  0 : 'STOPP'
               ,  1 : 'GO'
               ,  2 : 'HALT'
               ,  3 : 'Loc emergency stop'
               ,  4 : 'Loc end cycle'
               ,  9 : 'MFX new notifying counter'
               , 10 : 'SYSTEM OVERLOAD'
               , 11 : 'System status'
               , 48 : 'System ???'
               }
  
  __cmdType =  {  0: 'command'
               ,  1: 'response'
               }

  __directions={  0 : 'remain'
               ,  1 : 'forward'
               ,  2 : 'backward'
               ,  3 : 'switch'
               }

  __outFormat = '   {:15} {}'

# 1  4  7  10 13 16 19 22 25 28 31 33 36 : Laenge: 37
# 0  3  6  9  12 15 18 21 24 27 30 32 35
# 00 00 cf 52 06 43 54 5a 86 30 01 00 00
# p  cr hh hl dl d0 d1 d2 d3 d4 d5 d6 d7

  def __init__(self, message):

    super().__init__(unpack('13B', message))
    self.__command = self.getByte('cmdAndResp') & 0xfe
    self.__response = self.getByte('cmdAndResp') & 0x01

  def decode(self):
    out = str(self)
    out += linesep
    out += self.__getFormatedOut('Msg-Type:', self.__cmdType[self.__response])
    out += self.__getFormatedOut('Command:', self.__decodeCmd())
    out += self.__getFormatedOut('DataLenCount:', self.getByte('dlc'))
    if self.__isValidCmd():
      decodeFuncs = {  0 : self.__decodeCmd00
                    ,  2 : self.__decodeCmd02
                    ,  4 : self.__decodeCmd04
                    ,  6 : self.__decodeCmd06
                    ,  8 : self.__decodeCmd08
                    , 10 : self.__decodeCmd10
                    , 12 : self.__decodeCmd12
                    , 14 : self.__decodeCmd14
                    , 16 : self.__decodeCmd16
                    , 22 : self.__decodeCmd22
                    , 34 : self.__decodeCmd34
                    , 48 : self.__decodeCmd48
                    , 58 : self.__decodeCmd58
                    }
      out += decodeFuncs[self.__command]()
    return out

  def __isValidCmd(self):
    return self.__command in self.__commands.keys()

  def __isValidSubCmd(self):
    return self.getByte('d4') in self.__subcmds.keys()

  def __getFormatedOut(self, msg, val):
    return self.__outFormat.format(msg, val) + linesep

  def __getFormatedIdOut(self):
    deviceId = '{:02x}'.format(self.getByte('d0'))
    deviceId += ' {:02x}'.format(self.getByte('d1'))
    deviceId += ' {:02x}'.format(self.getByte('d2'))
    deviceId += ' {:02x}'.format(self.getByte('d3'))
    return self.__getFormatedOut('Device-ID:', deviceId)

  def __decodeCmd00(self):
    out = self.__getFormatedIdOut()
    if self.__isValidSubCmd():
      subCmd = self.getByte('d4')
      subCmdB = self.getByte('d4').to_bytes(1, 'little')
      subCmdName = '{} ({}) {}'.format(subCmd, subCmdB.hex(), self.__subcmds[subCmd])
      out += self.__getFormatedOut('Subcommand:',subCmdName)
      decodeFuncs = {  0 : self.__decodeCmd00Sub00
                    ,  1 : self.__decodeCmd00Sub01
                    ,  2 : self.__decodeCmd00Sub02
                    ,  3 : self.__decodeCmd00Sub03
                    ,  4 : self.__decodeCmd00Sub04
                    ,  9 : self.__decodeCmd00Sub09
                    , 10 : self.__decodeCmd00Sub0a
                    , 11 : self.__decodeCmd00Sub0b
                    , 48 : self.__decodeCmd00Sub30
                    }
      out += decodeFuncs[subCmd]()
    else:
      out += self.__getFormatedOut('Subcommand:','{} ({}) unknown subcommand'.format(subCmd, subCmdB.hex()))
    return out
  def __decodeCmd00Sub00(self):
    return ''
  def __decodeCmd00Sub01(self):
    return ''
  def __decodeCmd00Sub02(self):
    return ''
  def __decodeCmd00Sub03(self):
    return ''
  def __decodeCmd00Sub04(self):
    return ''
  def __decodeCmd00Sub09(self):
    return self.__getFormatedOut('NN-counter:','{} {}'.format(self.getByte('d5')
                                                             ,self.getByte('d6')))
  def __decodeCmd00Sub0a(self):
    return self.__getFormatedOut('Chanel:',self.getByte('d5'))
  def __decodeCmd00Sub0b(self):
    return self.__getFormatedOut('Chanel:',self.getByte('d5'))
  def __decodeCmd00Sub30(self):
    return self.__getFormatedOut('Value:',self.getByte('d5'))

  def __decodeCmd02(self):
    out = ''
    if self.__dlc in [1,5,6]:
      decodeFuncs = {  1 : self.__decodeCmd02Dlc01
                    ,  5 : self.__decodeCmd02Dlc05
                    ,  6 : self.__decodeCmd02Dlc06
                    }
      out += decodeFuncs[self.__dlc]()
    else:
      out += self.__getFormatedOut('Subcommand:','unknown datalength for this subcommand')
    return out
  def __decodeCmd02Dlc01(self):
    out = ''
    if self.__d0 == 33:
      out  += self.__getFormatedOut('Protocol:','MM2')
    else:
      if self.__d0 < 33:
        out += self.__getFormatedOut('Protocol:','MFX-ProgRail - {:02x}'.format(self.getByte('d0')))
      else:
        out += self.__getFormatedOut('Protocol:','MFX-MainRail - {:02x}'.format(self.getByte('d0')))
    return out
  def __decodeCmd02Dlc05(self):
    out = self.__getFormatedIdOut()
    if self.__d4 == 33:
      out  += self.__getFormatedOut('Protocol:','MM2')
    else:
      if self.__d4 < 33:
        out += self.__getFormatedOut('Protocol:','MFX-ProgRail - {:02x}'.format(self.getByte('d4')))
      else:
        out += self.__getFormatedOut('Protocol:','MFX-MainRail - {:02x}'.format(self.getByte('d4')))
    return out
  def __decodeCmd02Dlc06(self):
    out = self.__decodeCmd02Dlc05()
    out += self.__getFormatedOut('Signal-Quality:',self.__bToHex(self.__d5))
    return out

  def __decodeCmd04(self):
    out = self.__getFormatedIdOut()
    return out

  def __decodeCmd06(self):
    out = self.__getFormatedIdOut()
    return out

  def __decodeCmd08(self):
    out = self.__getFormatedIdOut()
    return out

  def __decodeCmd10(self):
    out = self.__getFormatedIdOut()
    return out

  def __decodeCmd12(self):
    out = self.__getFormatedIdOut()
    return out

  def __decodeCmd14(self):
    out = self.__getFormatedIdOut()
    return out

  def __decodeCmd16(self):
    out = self.__getFormatedIdOut()
    return out

  def __decodeCmd22(self):
    out = self.__getFormatedIdOut()
    out += self.__getFormatedOut('Position:', self.getByte('d4'))
    out += self.__getFormatedOut('Strom:', self.getByte('d5'))
    if self.getByte('dlc') == 8:
      out += self.__getFormatedOut('Schaltzeit:', '{} {}'.format(self.getByte('d6'), self.getByte('d7')))
    return out

  def __decodeCmd34(self):
    out  = self.__getFormatedIdOut()
    out += self.__getFormatedOut('device:', self.getByte('d0')*256 + self.getByte('d1'))
    out += self.__getFormatedOut('contact:', self.getByte('d2')*256 + self.getByte('d3'))
    out += self.__getFormatedOut('state(recent):', self.getByte('d4'))
    out += self.__getFormatedOut('state:', self.getByte('d5'))
    return out

  def __decodeCmd48(self):
    out = self.__getFormatedIdOut()
    if self.__response != 1:
      pass
    else:
      out += self.__getFormatedOut('SW-Version:', '{}.{}'.format(self.getByte('d4'), self.getByte('d5')))
      out += self.__getFormatedOut('DB-Version:', '{}.{}'.format(self.getByte('d6'), self.getByte('d7')))
    return out

  def __decodeCmd58(self):
    dlc = self.getByte('dlc')
    if dlc == 5 or dlc == 6:
      return self.__getFormatedIdOut()

  def __decodeCmd(self):
    out = '{0} ({0:02x}) - '.format(self.__command)
    if self.__isValidCmd():
      out += self.__commands[self.__command]
    else:
      out += 'unknown command'
    return out
