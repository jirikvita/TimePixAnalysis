#!/bin/bash

script=_plot.sh
rm -f $script

for rfile in `ls *.root` ; do
#for rfile in `ls gva*/*.root` ; do
#for rfile in `ls gva3*/*.root` ; do
#for rfile in `ls bg*/*.root gamma*/*.root` ; do
#for rfile in `ls *.root */*.root` ; do
  echo "root -b -q -l '../DrawHistoFromFile.C+(\"${rfile}\")'" >> $script
done

chmod +x $script
./$script

mkdir txt ; mv *.txt txt/
mkdir dsc ; mv *.dsc dsc/
mkdir root ; mv *.root root/
mkdir frames ; mv *.png frames/
