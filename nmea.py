class Nmea:
    def __init__(self, coordinate, direction):
        self.coordinate = coordinate
        self.direction = direction

    def convert_to_decimal(self):
        try:
            """ NMEA to Decimal Degrees"""
            if self.coordinate.find('.') is 5:
                """ longitude in the DDDMM.MMMMM format """
                dd = int(float(self.coordinate[:3].strip('0')))
                ss = float(self.coordinate) - dd * 100
                if self.direction == 'E':
                    return round(dd + (ss / 60), 6)
                elif self.direction == 'W':
                    return round(dd + (ss / 60),6) * -1
                else:
                    return 00.00000
            if self.coordinate.find('.') is 4:
                """  latitude in the DDMM.MMMMM format """
                dd = int(float(self.coordinate) / 100)
                ss = float(self.coordinate) - dd * 100
                if self.direction == 'N':
                    return round(dd + (ss / 60), 6)
                elif self.direction == 'S':
                    return round(dd + (ss / 60), 6) * -1
                else:
                    return 00.0000
        except:
            return 00.00000
