def test_server(ip, port):
    try:
        connection = telnetlib.Telnet(ip, port, timeout=0.1)
        connection.read_very_lazy()
        return True
    except Exception as e:
        if log_to_syslog:
            syslog.syslog('Server error: {} IP: {} PORT: {}'.format(e, ip, port))
        return False


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


def qtime_to_osmand_timestamp(qdate, qtime):
    day = qdate[:2]
    month = qdate[2:4]
    year = '20{}'.format(qdate[4:])
    hour = qtime[:2]
    minute = qtime[2:4]
    second = qtime[4:]
    return '{}-{}-{} {}:{}:{}'.format(year, month, day, hour, minute, second)


def q_to_osmand_params(q_message):
    chunks = q_message.split(',')
    params = {
        'id': '{}'.format(chunks[1].replace(':', '')),
        'name': '{}'.format(chunks[1]),
        'timestamp': '{}'.format(qtime_to_osmand_timestamp(chunks[3], chunks[4])),
        'lat': '{}'.format(nmea_to_dd(chunks[5], chunks[6])),
        'lon': '{}'.format(nmea_to_dd(chunks[7], chunks[8])),
        'nos': '{}'.format(chunks[10]),
        'speed': '{}'.format(chunks[11]),
        'memory / Realtime': '{}'.format(chunks[12]),
        'name': '{}'.format(chunks[13]),
        'type': '{}'.format(chunks[14]),
        'heading': '{}'.format(chunks[15]),
        'altitude': '{}'.format(chunks[16]),
        'hdop': '{}'.format(chunks[17]),
        'voltage': '{}'.format(chunks[18]),
        'consumption': '{}'.format(chunks[19]),
        'country': '{}'.format(chunks[20]),
        'network': '{}'.format(chunks[21]),
        'signal strength': '{}'.format(chunks[25]),
        'delivery route': '{}'.format(chunks[27]),
    }
    return params


def play():
    try:
        connection = telnetlib.Telnet(QSERVER, QPORT, timeout=0.1)
    except Exception as e:
        if log_to_syslog:
            syslog.syslog('Q Server error: {}'.format(e))
        pass
    try:
        message = str(connection.read_until(b'QQQ'))

    except Exception as e:
        if log_to_syslog:
            syslog.syslog('Q server error, could not read Q message from telnet port, error: {}'.format(e))
        pass

    try:
        url = 'http://{}:{}/'.format(TSERVER, TPORT)
        params = q_to_osmand_params(message)
        r = requests.post(url, params, headers={'content-type': 'text/plain; charset=utf-8'})
    except Exception as e:
        if log_to_syslog:
            syslog.syslog('T server error, could not send HTTP post, error: {}'.format(e))
        pass


def wait():
    r = random.randint(1, 60)
    if log_to_syslog:
        syslog.syslog('Initializing Squid daemon, process starts in : {} seconds, threads: {}'.format(r, threads))
    time.sleep(r)


def main():
    wait()
    while True:
        if test_server(QSERVER, QPORT) and test_server(TSERVER, TPORT):
            play()
        else:
            if log_to_syslog:
                syslog.syslog('Connection lost, reconnecting...')
            wait()


thread_list = []

for i in range(threads):
    t = threading.Thread(target=main)
    thread_list.append(t)
    t.start()
