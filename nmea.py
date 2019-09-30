class Nmea:
    def __init__(self, coordinate, direction):
        self.coordinate = coordinate
        self.direction = direction

    """ NMEA to Decimal Degrees"""
    def convert_to_decimal(self):
        if not isinstance(self.coordinate, str) or not len(self.coordinate) is 9:
            raise TypeError('invalid coordinate')
        if not self.coordinate.find('.'):
            raise TypeError('invalid coordinate, missing .')
        if not self.coordinate.find('.') in [4, 5]:
            raise TypeError('invalid coordinate, point is not in proper position')
        if self.direction not in ['N', 'S', 'W', 'E']:
            raise TypeError('only N, S, E or W are valid directions')

        if self.coordinate.find('.') is 5:
            """ longitude in the DDDMM.MMMMM format """
            dd = int(float(self.coordinate[:3].strip('0')))
            ss = float(self.coordinate) - dd * 100
            if self.direction == 'E':
                return round(dd + (ss / 60), 6)
            elif self.direction == 'W':
                return round(dd + (ss / 60), 6) * -1
            else:
                return 0.0

        elif self.coordinate.find('.') is 4:
            """  latitude in the DDMM.MMMMM format """
            dd = int(float(self.coordinate) / 100)
            ss = float(self.coordinate) - dd * 100
            if self.direction == 'N':
                return round(dd + (ss / 60), 6)
            elif self.direction == 'S':
                return round(dd + (ss / 60), 6) * -1
            else:
                return 0.0
        else:
            return 0.0
