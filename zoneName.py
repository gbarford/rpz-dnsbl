#!/usr/bin/env python2.7

import sys
import os.path
from config import config

zoneName=""

if len(sys.argv) > 1:
   if sys.argv[1] == "rpz":
      zoneName=config['rpzListName']
   elif sys.argv[1] == "blocklist":
      zoneName=config['blocklistName']

if zoneName != "":
   print(zoneName)
else:
   exit(1)
