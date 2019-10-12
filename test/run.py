#!/usr/bin/python
# -*- coding: utf-8 -*-
# Copyright: (c) 2019, Dag Wieers (@dagwieers) <dag@wieers.com>
# GNU General Public License v3.0 (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
''' Run any Kodi VTM GO plugin:// URL on the commandline '''

from __future__ import absolute_import, division, print_function, unicode_literals
import os
import sys

# Add current working directory to import paths
cwd = os.path.abspath(os.path.join(os.path.dirname(os.path.realpath(os.path.realpath(__file__))), os.pardir))
sys.path.insert(0, cwd)
print(cwd)
from resources.lib import plugin  # noqa: E402  pylint: disable=wrong-import-position

xbmc = __import__('xbmc')
xbmcaddon = __import__('xbmcaddon')
xbmcgui = __import__('xbmcgui')
xbmcplugin = __import__('xbmcplugin')
xbmcvfs = __import__('xbmcvfs')

if len(sys.argv) <= 1:
    print("%s: URI argument missing\nTry '%s plugin://plugin.video.vtm.go/recent/1' to test." % (sys.argv[0], sys.argv[0]))
    sys.exit(1)

# Also support bare paths like /recent/2
if not sys.argv[1].startswith('plugin://'):
    sys.argv[1] = 'plugin://plugin.video.vtm.go' + sys.argv[1]

print('** Running URI: %s' % sys.argv[1])
plugin = plugin.routing
plugin.run([sys.argv[1], 0, ''])
