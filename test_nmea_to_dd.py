import unittest
from converter import *


class TestNmeaToDD(unittest.TestCase):
    def test_valid(self):
        self.assertAlmostEqual(nmea_to_dd('5132.0000', 'N'), 51.533333)
        self.assertAlmostEqual(nmea_to_dd('5132.0000', 'S'), -51.533333)
        self.assertAlmostEqual(nmea_to_dd('01323.629', 'E'), 13.393817)
        self.assertAlmostEqual(nmea_to_dd('01323.629', 'W'), -13.393817)

    def test_invalid_directions(self):
        with self.assertRaises(TypeError):
            nmea_to_dd('5132.0000', 'A')
        with self.assertRaises(TypeError):
            nmea_to_dd('5132.0000', 'B')
        with self.assertRaises(TypeError):
            nmea_to_dd('5132.0000', 9)
        with self.assertRaises(TypeError):
            nmea_to_dd('5132.0000', True)

    def test_invalid_Lenght_coordinates(self):
        with self.assertRaises(TypeError):
            nmea_to_dd('5132.00', 'N')
        with self.assertRaises(TypeError):
            nmea_to_dd('5132.0000000', 'N')

    def test_point_exist_in_coordinate(self):
        with self.assertRaises(TypeError):
            nmea_to_dd('51320000', 'W')

    def test_point_position(self):
        with self.assertRaises(TypeError):
            nmea_to_dd('51.320000', 'W')
