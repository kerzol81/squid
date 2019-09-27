import unittest
from nmea import *


class TestNmeaConverter(unittest.TestCase):
    def test_valid_lat_1(self):
        self.assertAlmostEqual(Nmea('5132.0000', 'N').convert_to_decimal(), 51.533333)

    def test_valid_lat_2(self):
        self.assertAlmostEqual(Nmea('5132.0000', 'S').convert_to_decimal(), -51.533333)

    def test_valid_lon_1(self):
        self.assertAlmostEqual(Nmea('01323.629', 'E').convert_to_decimal(), 13.393817)

    def test_valid_lon_2(self):
        self.assertAlmostEqual(Nmea('01323.629', 'W').convert_to_decimal(), -13.393817)
