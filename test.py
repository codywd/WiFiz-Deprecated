import os

file = os.getcwd() + "/iwconfig.log"

if "MomAndKids" in open(file).read():
    print "Yes"