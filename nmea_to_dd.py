def nmea_to_dd(coordinate, direction):
    if not isinstance(coordinate, str) or not len(coordinate) is 9:
        raise TypeError('invalid coordinate')
    if not coordinate.find('.'):
        raise TypeError('invalid coordinate, missing .')
    if not coordinate.find('.') in [4, 5]:
        raise TypeError('invalid coordinate, point is not in proper position')
    if direction not in ['N', 'S', 'W', 'E']:
        raise TypeError('only N, S, E or W are valid directions')

    if coordinate.find('.') is 5:
        """ longitude in the DDDMM.MMMMM format """
        dd = int(float(coordinate[:3].strip('0')))
        ss = float(coordinate) - dd * 100
        if direction == 'E':
            return round(dd + (ss / 60), 6)
        elif direction == 'W':
            return round(dd + (ss / 60), 6) * -1
        else:
            return 0.0
    if coordinate.find('.') is 4:
        """  latitude in the DDMM.MMMMM format """
        dd = int(float(coordinate) / 100)
        ss = float(coordinate) - dd * 100
        if direction == 'N':
            return round(dd + (ss / 60), 6)
        elif direction == 'S':
            return round(dd + (ss / 60), 6) * -1
        else:
            return 0.0
