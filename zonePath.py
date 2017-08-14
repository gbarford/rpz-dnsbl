#!/usr/bin/env python2.7

import sys
import os.path
from config import config

zoneFilePath=""

if len(sys.argv) > 1:
   if sys.argv[1] == "rpz":
      zoneFilePath=os.path.join(config['bindZoneFilePath'],config['rpzListName'])
   elif sys.argv[1] == "blocklist":
      zoneFilePath=os.path.join(config['bindZoneFilePath'],config['blocklistName'])
   if len(sys.argv) > 2:
      if sys.argv[2] == "new":
         zoneFilePath+="-new"

if zoneFilePath != "":
   print(zoneFilePath)
else:
   exit(1)
