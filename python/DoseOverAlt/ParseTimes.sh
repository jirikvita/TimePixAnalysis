#!/bin/bash

year=2019

#for sdir in PrgFrkJan2019 FrkGvaJan2019 ; do
#for sdir in  ZurPrgFeb2019 GvaZurFeb2019 ; do
#for sdir in PrgRomMay2019  ; do
for sdir in RomPrgMay2019  ; do

    if [ -d $sdir ] ; then
	cd $sdir
        for i in `ls *.txt` ; do
           j=`basename $i .txt`
	   echo $j
	   tname=${j}.time
	   cat ${i}.dsc | grep $year > $tname
       done
	cd -

    fi
    
done
