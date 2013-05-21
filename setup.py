#!/usr/bin/python2

from distutils.core import setup

setup(name='wifiz',
      version='0.9.1/1',
      description = "GUI for netctl",
      author = "Cody Dostal, Gregory Mullen",
      author_email = "dostalcody@gmail.com",
      url = "https://github.com/codywd/WiFiz",
      #py_modules=['main'],
      #'runner' is in the root.
      scripts = ['scripts/wifiz'],
      data_files=[('/usr/share/wifiz/', ['main.py']),
                  ('/usr/share/wifiz/imgs/',
        ['imgs/APScan.png', 'imgs/connect.png', 'imgs/exit.png',
        'imgs/newprofile.png', 'imgs/aboutLogo.png', 'imgs/disconnect.png',
        'imgs/logo.png', 'imgs/preferences.png' ]),
                  ('/usr/share/licenses/wifiz/',['WiFiz.license']
                 ]
      )