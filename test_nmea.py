import unittest
from nmea import *


class TestNmeaConverter(unittest.TestCase):
    def test_valid_lat_1(self):
        n = Nmea('5132.0000', 'N')
        self.assertAlmostEqual(n.convert_to_decimal(), 51.533333)

    def test_valid_lat_2(self):
        n = Nmea('5132.0000', 'S')
        self.assertAlmostEqual(n.convert_to_decimal(), -51.533333)

    def test_valid_lon_1(self):
        n = Nmea('01323.629', 'E')
        self.assertAlmostEqual(n.convert_to_decimal(), 13.393817)

    def test_valid_lon_2(self):
        n = Nmea('01323.629', 'W')
        self.assertAlmostEqual(n.convert_to_decimal(), -13.393817)
        
        
