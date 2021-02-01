#!/usr/bin/env python3

import logging
import subprocess #Used to run airodump-ng for network and client scanning (w/ timeout)
import csv #Used for reading files created by airodump-ng
import json #Used for transmitting data back to JS nicely
import os #Used to delete files after they have been processed
import configparser #Used to handle configuration provided by user

from pineapple.modules import Module, Request

module = Module('CaptivePortalJumper', logging.DEBUG)

# Default Var Config
APScanInterface = "wlan2"
APScanTimeout = 5
ClientScanInterface = "wlan2"
ClientScanTimeout = 5

# Update global variables with user specified config
def getConfig():
    try:
        global APScanInterface, APScanTimeout, ClientScanInterface, ClientScanTimeout
        config = configparser.ConfigParser()
        config.read("config")
        APScanInterface = str(config["APScan"]["Interface"])
        APScanTimeout = int(config["APScan"]["Timeout"])
        ClientScanInterface = str(config["ClientScan"]["Interface"])
        ClientScanTimeout = int(config["ClientScan"]["Timeout"])
        return True
    except:
        pass
    return False

# Scan for APs using airodump with a timeout
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

# Scan for clients of specific AP using airodump with a timeout
def scanForClients(interface="wlan2", BSSID="" , channel="11", timeout=5):
    try:
        r = subprocess.run(['airodump-ng', '--bssid', BSSID, '-c', channel, '-w', 'dat', '--output-format', 'csv', '--write-interval', '1', interface], timeout=timeout)
    except subprocess.TimeoutExpired as e:
        clients = []
        with open("dat-01.csv") as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=",")
            for row in csv_reader:
                if len(row)==7 and "Station MAC" not in row:
                    clients.append(row[0].strip()) #Return client station mac
        os.remove("dat-01.csv")
        return json.dumps(clients)
    os.remove("dat-01.csv")
    return []

# Update config file and user variables with new user specified values (or reset)
def setConfig(reset = False, apInterface = None, apTimeout = None, clientInterface = None, clientTimeout = None):
    try:
        config = configparser.ConfigParser()
        config["DEFAULT"] = {"Interface = wlan2", "Timeout = 5"}
        if reset:
            config["APScan"]["Interface"] = config["DEFAULT"]["Interface"]
            config["APScan"]["Timeout"] = config["DEFAULT"]["Timeout"]
            config["ClientScan"]["Interface"] = config["DEFAULT"]["Interface"]
            config["ClientScan"]["Timeout"] = config["DEFAULT"]["Timeout"]
        else:
            config["APScan"]["Interface"] = apInterface
            config["APScan"]["Timeout"] = apTimeout
            config["ClientScan"]["Interface"] = clientInterface
            config["ClientScan"]["Timeout"] = clientTimeout
        with open("config") as configfile:
            config.write(configfile)
        if getConfig():
            return True
    except:
        pass
    return False

# Handle API Calls
@module.handles_action('getAP')
def getAP(request: Request):
    aps = scanForAPs(interface=APScanInterface, timeout=APScanTimeout)
    return aps

@module.handles_action('getClients')
def getClients(request: Request):
    clients = scanForClients(interface=ClientScanInterface, BSSID=request.bssid, channel=request.channel, timeout=ClientScanTimeout)
    return clients

@module.handles_action('loadConfig')
def loadConfig(request: Request):
    return getConfig()

@module.handles_action('setConfig')
def setConfig(request: Request):
    return setConfig(reset = request.reset, apInterface = request.ap_interface, apTimeout = request.ap_timeout, clientInterface = request.client_interface, clientTimeout = request.client_timeout)


if __name__ == '__main__':
    module.start()
