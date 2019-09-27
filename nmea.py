class Nmea:
    def __init__(self, coordinate, direction):
        self.coordinate = coordinate
        self.direction = direction

    @property
    def convert_to_decimal(self):
        zero = '00.00000'
        try:
            """ NMEA to Decimal Degrees"""
            if self.coordinate.find('.') is 5:
                """ longitude in the DDDMM.MMMMM format """
                dd = int(float(self.coordinate[:3].strip('0')))
                ss = float(self.coordinate) - dd * 100
                if self.direction == 'E':
                    result = str(round(dd + (ss / 60), 6))
                elif self.direction == 'W':
                    result = str(round(dd + (ss / 60, 6), 6) * -1)
                else:
                    result = zero
                return result
            if self.coordinate.find('.') is 4:
                """  latitude in the DDMM.MMMMM format """
                dd = int(float(self.coordinate) / 100)
                ss = float(self.coordinate) - dd * 100
                if self.direction == 'N':
                    result = str(round(dd + (ss / 60), 6))
                elif self.direction == 'S':
                    result = str(round(dd + (ss / 60), 6) * -1)
                else:
                    result = zero
                return result
        except:
            return zero
