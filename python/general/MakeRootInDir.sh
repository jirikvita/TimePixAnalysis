#!/bin/bash
for i in `ls *.txt | grep -v dsc` ; do 
    pyroot /home/qitek/cernbox/TimePix/ReadToRoot.py $i
done
mkdir root ; 
hadd all.root *.root ; mv *.root root/
