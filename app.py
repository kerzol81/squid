#!/usr/bin/env python3

# Production code v. 1.0

import requests
import threading
import telnetlib
import time
import random
import syslog

QSERVER = '1.2.3.4'    
QPORT = 23               

TSERVER = '5.6.7.8'  
TPORT = 5055         

log_to_syslog = True
threads = 2


def test_server(ip, port):
    try:
        connection = telnetlib.Telnet(ip, port, timeout=0.1)
        connection.read_very_lazy()
        return True
    except Exception as e:
        if log_to_syslog:
            syslog.syslog('Server error: {} IP: {} PORT: {}'.format(e, ip, port))
        return False


def latitude_convert(latitude, direction):
    """ NMEA to Decimal Degrees"""
    dd = int(float(latitude)/100)
    ss = float(latitude) - dd * 100
    if direction == 'N':
        return dd + (ss / 60)
    elif direction == 'S':
        return dd + (ss / 60) * -1
    else:
        return '00.000000'


def longitude_convert(longitude, direction):
    """ NMEA to Decimal Degrees"""
    dd = int(float(longitude[:3].strip('0')))
    ss = float(longitude) - dd * 100
    if direction == 'E':
        return dd + (ss / 60)
    elif direction == 'W':
        return dd + (ss / 60) * -1
    else:
        return '00.0000000'


def qtime_to_osmand_timestamp(qdate, qtime):
    day = qdate[:2]
    month = qdate[2:4]
    year = '20{}'.format(qdate[4:])
    hour = qtime[:2]
    minute = qtime[2:4]
    second = qtime[4:]
    return '{}-{}-{} {}:{}:{}'.format(year, month, day, hour, minute, second)


def qsm_to_osmand_params(qsm_message):
    chunks = qsm_message.split(',')
    params = {
        'id': '{}'.format(chunks[1].replace(':', '')),
        'name': '{}'.format(chunks[1]),
        'timestamp': '{}'.format(qtime_to_osmand_timestamp(chunks[3], chunks[4])),
        'lat': '{}'.format(latitude_convert(chunks[5], chunks[6])),
        'lon': '{}'.format(longitude_convert(chunks[7], chunks[8])),
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
        message = str(connection.read_until(b'QEM'))

    except Exception as e:
        if log_to_syslog:
            syslog.syslog('Q server error, could not read Q message from telnet port, error: {}'.format(e))
        pass

    try:
        url = 'http://{}:{}/'.format(TSERVER, TPORT)
        params = qsm_to_osmand_params(message)
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


threads = []

for i in range(threads):
    t = threading.Thread(target=main)
    threads.append(t)
    t.start()
