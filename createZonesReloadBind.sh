#!/bin/bash

rndNumber=$RANDOM+`date +%s`
blocklistCheck=100
rpzCheck=100

DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd $DIR

echo "----------------Create Zones---------------" >> /tmp/createErrors$rndNumber
./buildZoneFiles.py >> /tmp/createErrors$rndNumber 2>&1


echo "----------------Blocklist checkzone---------------" >> /tmp/createErrors$rndNumber

if [ -f `./zonePath.py blocklist new` ]; then
   named-checkzone `./zoneName.py blocklist` `./zonePath.py blocklist new` >> /tmp/createErrors$rndNumber 2>&1
   blocklistCheck=$?
else
   echo "New blocklist didn't exist" >> /tmp/createErrors$rndNumber
   blocklistCheck=10
fi

echo "----------------Blocklist mv---------------" >> /tmp/createErrors$rndNumber

if [ $blocklistCheck -eq 0 ]; then
   mv `./zonePath.py blocklist new` `./zonePath.py blocklist` >> /tmp/createErrors$rndNumber 2>&1
   blocklistMove=$?
else
   echo "mv failed file doesn't exist or check failed" >> /tmp/createErrors$rndNumber
fi

echo "----------------RPZ checkzone---------------" >> /tmp/createErrors$rndNumber

if [ -f `./zonePath.py rpz new` ]; then
   named-checkzone `./zoneName.py rpz` `./zonePath.py rpz new` >> /tmp/createErrors$rndNumber 2>&1
   rpzCheck=$?
else
   echo "New rpz didn't exist" >> /tmp/createErrors$rndNumber
   rpzCheck=10
fi

echo "----------------RPZ mv---------------" >> /tmp/createErrors$rndNumber

if [ $rpzCheck -eq 0 ]; then
   mv `./zonePath.py rpz new` `./zonePath.py rpz` >> /tmp/createErrors$rndNumber 2>&1
   rpzMove=$?
else
   echo "mv failed file doesn't exist or check failed" >> /tmp/createErrors$rndNumber
fi

if [ $rpzCheck -eq 0 ] && [ $rpzMove -eq 0 ] && [ $blocklistCheck -eq 0 ] && [ $blocklistMove -eq 0 ]; then
   service bind9 reload
else
   # Replace with mail command
   cat /tmp/createErrors$rndNumber
fi  

rm /tmp/createErrors$rndNumber 
