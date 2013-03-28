#!/usr/bin/python2
# connection functions

import os

def __init__():
    pass

def start(network):
    os.system("netctl start " + network)

def stop(network):
    os.system("netctl stop " + network)

def stopall():
    os.system("netctl stop-all")

def restart(network):
    os.system("netctl restart " + profile)