""" mcanhash.py

    Autor: Maier-Lohman, Rainer
"""
# -----------------------------------------------------------------------------
# Klasse zur Erstellung bzw. Verwaltung eines MCAN-Hashes
# -----------------------------------------------------------------------------
class McanHash():
  """ Klasse zur Erstellung bzw. Verwaltung eines MCAN-Hashes
      Ausgewertet werden die letzten 4 Bytes des angegebenen Wertes.
      z.B.: MAC-Adresse: F0-B0-14-9F-AD-E0 -> 0x149fde0
  """
  def __init__(self, val):
    self.__val = val
    self.__val4Bytes = val & 0xffffffff
    self.__msb = self.__val4Bytes >> 16;
    self.__lsb = self.__val4Bytes & 0xffff
    hash = self.__msb ^ self.__lsb
    self.__mcanhash = (((hash << 3) & 0xFF00) | 0x0300) | (hash & 0x7F)

  def __str__(self):
    return '{:04x}'.format(self.__mcanhash)

  def __int__(self):
    return self.__mcanhash

  def __repr__(self):
    """ f-String in MicroPython nicht implentiert.
    """
    out  = 'value:     {:>12x}\n'.format(self.__val)
    out += '  last 4B: {:>12x}\n'.format(self.__val4Bytes)
    out += '  msb:     {:>12x}\n'.format(self.__msb)
    out += '  lsb:     {:>12x}\n'.format(self.__lsb)
    out += '  msb^lsb: {:>12x}\n'.format(self.__msb^self.__lsb)
    out += 'mcanhash:  {:>12x}'.format(self.__mcanhash)
    return out

  @property
  def __call__(self):
    """ Liefert einen 2Byte langen Hash als int.
    """
    return self.__mcanhash
