#!/usr/bin/env python3

import logging
import subprocess #Used to run airodump-ng for network and client scanning (w/ timeout)
import csv #Used for reading files created by airodump-ng
import json #Used for transmitting data back to JS nicely
import os #Used to delete files after they have been processed

from pineapple.modules import Module, Request

module = Module('CaptivePortalJumper', logging.DEBUG)

def scanForAPs(interface="wlan2", timeout=5):
    try:
        r = subprocess.run(['airodump-ng', '-w', 'dat', '--output-format', 'csv', '--write-interval', '1', interface], timeout=timeout)
    except subprocess.TimeoutExpired as e:
        aps = []
        with open("dat-01.csv") as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=",")
            for row in csv_reader:
                if len(row)==15 and ' OPN' in row:
                    if(row[-2].strip()):
                        aps.append([row[-2].strip(), [row[0].strip(), row[3].strip()]]) #Return AP Name, BSSID, and Channel
        os.remove("dat-01.csv")
        return json.dumps(aps)
    os.remove("dat-01.csv")
    return []

def scanForClients(interface="wlan2", BSSID="" , channel="11", timeout=5):
    try:
        r = subprocess.run(['airodump-ng', '--bssid', BSSID, '-c', channel, '-w', 'dat', '--output-format', 'csv', '--write-interval', '1', interface], timeout=timeout)
    except subprocess.TimeoutExpired as e:
        clients = []
        with open("dat-01.csv") as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=",")
            for row in csv_reader:
                if len(row)==7:
                    clients.append(row[0].strip()) #Return client station mac
        os.remove("dat-01.csv")
        return json.dumps(clients)
    os.remove("dat-01.csv")
    return []

@module.handles_action('getAP')
def getAP(request: Request):
    aps = scanForAPs()
    return aps

@module.handles_action('getClients')
def getClients(request: Request):
    clients = scanForClients(interface="wlan2", BSSID=request.bssid, channel=request.channel, timeout=5)
    return clients

if __name__ == '__main__':
    module.start()
