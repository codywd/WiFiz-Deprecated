#!/usr/bin/python2
# connection functions

import os

def __init__():
    pass

def start(network):
    os.system("netctl start " + network)
    print "netctl:: start " + network

def stop(network):
    os.system("netctl stop " + network)
    print "netctl:: stop " + network

def stopall():
    os.system("netctl stop-all")
    print "netctl:: stop-all"

def restart(network):
    os.system("netctl restart " + profile)
    print "netctl:: restart " + network