#!/usr/bin/python2
# Interface functions
import os

def down(interface):
    os.system("ip link set down dev " + interface)
    print interface

def up(interface):
    os.system("ip link set up dev " + interface)

