#!/usr/bin/python2

from distutils.core import setup

setup(name='wifiz',
      version='0.9.0',
      description = "GUI for netctl",
      author = "Cody Dostal, Gregory Mullen",
      author_email = "greg@grayhatter.com",
      url = "https://github.com/GrayHatter/WiFiz",
      py_modules=['foo'],
      #'runner' is in the root.
      scripts = ['scripts/wifiz']
      )