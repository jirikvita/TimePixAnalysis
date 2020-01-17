#!/bin/bash

for i in GPS_RomPrgFeb2019.LOG ; do
#for i in `ls GPS*.LOG` ; do
  cat $i | grep GGA | cut -d "," -f 2,10 | sed "s|,| |g" > ${i}.parsed
done
