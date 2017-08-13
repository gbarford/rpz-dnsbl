#!/usr/bin/env python2.7

import os.path
import re
import requests
from config import config

setOfMaliciousDomains=set()
rpzZone=""

blocklistZoneFilePath=os.path.join(config['bindZoneFilePath'],config['blocklistName'])
rpzZoneFilePath=os.path.join(config['bindZoneFilePath'],config['rpzListName'])

if os.path.isfile('serialnumber'):
   with open('serialnumber') as serialNumberFile:
      serialNumber=int(serialNumberFile.read())+1
      serialNumberFile.close()
else:
   serialNumber=1

serialNumberFile=open("serialnumber", "w")
serialNumberFile.write(str(serialNumber))
serialNumberFile.close()

for intelList in config['intelUrls']:
   intelRequest = requests.get(intelList) 
   if intelRequest.status_code == 200:
      for domain in intelRequest.iter_lines():
         domain=domain.strip()
         if re.search("^\S+\.\S+$",domain):
            if len(domain + config['blocklistName']) < 255:
               setOfMaliciousDomains.add(domain)

# Create RPZ zone file

rpzZone="$TTL " + str(config['rpzTTL']) + "\n"
rpzZone+="@    SOA "
count=1
for nameserver in config['blocklistDnsServers']:
   rpzZone+="ns" + str(count) + "." + config['blocklistName'] + ". "
   count+=1
rpzZone+=" ( " + str(serialNumber) + " " + str(config['rpzRefresh'])
rpzZone+=" " + str(config['rpzRetry']) + " " + str(config['rpzExpiry']) + " " + str(config['rpzNxDomainTTL']) + " )\n"
rpzZone+="     NS ns." + config['rpzListName'] + ".\n\n"

for maliciousDomain in setOfMaliciousDomains:
   rpzZone+="*." + maliciousDomain + "    IN CNAME " + config['rpzCnameTo'] + "\n" 
   rpzZone+=maliciousDomain + "      IN CNAME " + config['rpzCnameTo'] + "\n"

# Create block list

blocklistZone="$TTL " + str(config['blocklistTTL']) + "\n"
blocklistZone+="$ORIGIN " + config['blocklistName'] + ".\n"
blocklistZone+=config['blocklistName'] + ".    SOA "
count=1
for nameserver in config['blocklistDnsServers']:
   blocklistZone+="ns" + str(count) + "." + config['blocklistName'] + ". "
   count+=1
blocklistZone+=" ( " + str(serialNumber) + " " + str(config['blocklistRefresh'])
blocklistZone+=" " + str(config['blocklistRetry']) + " " + str(config['blocklistExpiry']) + " " + str(config['blocklistNxDomainTTL']) + " )\n"

count=1
for nameserver in config['blocklistDnsServers']:
   blocklistZone+="     NS ns" + str(count) + "\n"
   count+=1

count=1
for nameserver in config['blocklistDnsServers']:
   blocklistZone+="ns" + str(count) + "     IN A " + nameserver + "\n"
   count+=1

for maliciousDomain in setOfMaliciousDomains:
   blocklistZone+="*." + maliciousDomain + "    IN A " + config['blocklistA'] + "\n"
   blocklistZone+=maliciousDomain + "      IN A " + config['blocklistA'] + "\n"


rpzZoneFile=open(rpzZoneFilePath, "w")
rpzZoneFile.write(rpzZone)
rpzZoneFile.close()

blocklistZoneFile=open(blocklistZoneFilePath, "w")
blocklistZoneFile.write(blocklistZone)
blocklistZoneFile.close()
