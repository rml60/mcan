""" Schoen-Wetter Tests fuer das Modul mcan

    Author: Rainer Maier-Lohmann
    ---------------------------------------------------------------------------
    "THE BEER-WARE LICENSE" (Revision 42):
    <r.m-l@gmx.de> wrote this file.  As long as you retain this notice you
    can do whatever you want with this stuff. If we meet some day, and you 
    think this stuff is worth it, you can buy me a beer in return.
    ---------------------------------------------------------------------------
    (c) 2020
"""
import unittest
import sys
sys.path.insert(0, "../")

from mcan import mcanhash, mcancommand, mcandecode

class McanTest(unittest.TestCase):

  def test_Mcanhash(self):
    macHash = mcanhash.McanHash(0xF0B0149FADE0)
    self.assertEqual(int(macHash), 0xcb7f )

    uidHash = mcanhash.McanHash(0x43539A40)
    self.assertEqual(int(uidHash), 0xcb13 )

  def test_McanCommand(self):
    macHash = mcanhash.McanHash(0xF0B0149FADE0)
    mcanCmd = mcancommand.McanCommand(int(macHash))
    mcanCmd.setCommand(0x22)
    mcanCmd.setDevice(0, 30) # Rueckmelder 0, Kontakt 30(1e)
    expected = b'\x00"\xcb\x7f\x08\x00\x00\x00\x1e\x00\x00\x00\x00'
    self.assertEqual(mcanCmd.frame, expected)
    mcanCmd.toggleTrackState()
    expected = b'\x00"\xcb\x7f\x08\x00\x00\x00\x1e\x00\x01\x00\x00'
    self.assertEqual(mcanCmd.frame, expected)
    mcanCmd.toggleTrackState()
    expected = b'\x00"\xcb\x7f\x08\x00\x00\x00\x1e\x01\x00\x00\x00'
    self.assertEqual(mcanCmd.frame, expected)
    expected = b'\x00#\xcb\x7f\x08\x00\x00\x00\x1e\x01\x00\x00\x00'
    self.assertEqual(mcanCmd.response, expected)

    mcanCmd.toggleTrackState(0)
    mcanCmd.setDevice(20, 45) # Rueckmelder 20, Kontakt 45(2d)
    expected = b'\x00"\xcb\x7f\x08\x00\x14\x00\x2d\x00\x00\x00\x00'
    self.assertEqual(mcanCmd.frame, expected)
    expected = b'\x00#\xcb\x7f\x08\x00\x14\x00\x2d\x00\x00\x00\x00'
    self.assertEqual(mcanCmd.response, expected)

    mcanCmd.setDevice(898, 486)
    expected = b'\x00"\xcb\x7f\x08\x03\x82\x01\xe6\x00\x00\x00\x00'
    self.assertEqual(mcanCmd.frame, expected)
    expected = b'\x00#\xcb\x7f\x08\x03\x82\x01\xe6\x00\x00\x00\x00'
    self.assertEqual(mcanCmd.response, expected)

  def test_McanDecode(self):
    macHash = mcanhash.McanHash(0xF0B0149FADE0)
    mcanCmd = mcancommand.McanCommand(int(macHash))
    mcanCmd.setCommand(0x22)
    mcanCmd.setDevice(0, 30) # Kontakt 30(1e)
    mcanCmd.toggleTrackState()
    expected =  '00 22 cb 7f 08 00 00 00 1e 00 01 00 00 \r\n'\
              + '   Msg-Type:       command\r\n'\
              + '   Command:        34 (22) - Track state\r\n'\
              + '   DataLenCount:   8\r\n'\
              + '   Device-ID:      00 00 00 1e\r\n'\
              + '   device:         0\r\n'\
              + '   contact:        30\r\n'\
              + '   state(recent):  0\r\n'\
              + '   state:          1\r\n'
    actual = mcandecode.McanDecode(mcanCmd.frame).decode()
    self.assertEqual(actual, expected)

    expected =  '00 23 cb 7f 08 00 00 00 1e 00 01 00 00 \r\n'\
              + '   Msg-Type:       response\r\n'\
              + '   Command:        34 (22) - Track state\r\n'\
              + '   DataLenCount:   8\r\n'\
              + '   Device-ID:      00 00 00 1e\r\n'\
              + '   device:         0\r\n'\
              + '   contact:        30\r\n'\
              + '   state(recent):  0\r\n'\
              + '   state:          1\r\n'
    actual = mcandecode.McanDecode(mcanCmd.response).decode()
    self.assertEqual(actual, expected)

if __name__ == '__main__':
  unittest.main()
