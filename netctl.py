#!/usr/bin/python2
# connection functions

import os

def __init__():
    pass

def start(network):
    os.system("netctl start " + network)
    print "start " + network

def stop(network):
    os.system("netctl stop " + network)
    print "stop " + network

def stopall():
    os.system("netctl stop-all")
    print "stop-all"

def restart(network):
    os.system("netctl restart " + profile)
    print "restart " + network