#!/bin/bash

# modify first what you want to convert, then
# call this script from ToSort directory:
# cd ToSort
# ../ConvertInSubdirs.sh
# i.e. to be run in Spectra/ directory with the scripts files one level up ;-)

convert=`ls ${PWD}/../ReadToRoot.py`

#for i in `ls  | grep JeskyneJune2016` ; do
#for i in `ls  | grep 90deg` ; do
#for i in `ls  | grep LetNY` ; do
#for i in `ls  | egrep "MuSearch_90x600s_22_open|MuSearch_6x600s_20|MuSearch_36x600s_21"` ; do
#for i in `ls | egrep "MuSearch_290x600s_17|MuSearch_324x600_16"` ; do
#for i in `ls  | grep LetFrk1` ; do
for i in `ls | grep MuSearch ` ; do
#for i in `ls | grep MuSearch | grep 570x600s_14` ; do
#for i in `ls | grep MuSearch | grep 430x600s_12` ; do
#for i in `ls | grep MuSearch | grep 432x600s_13` ; do
#for i in `ls | grep MuSearch_30x600s_2` ; do
#for i in `ls | grep MuSearch_280x600s_10` ; do
#for i in `ls | grep MuSearch_144x600s_9` ; do
#for i in `ls | grep MuSearch_432x600s_7` ; do
#for i in `ls | grep inches` ; do
#for i in `ls | egrep "bg|gamma"` ; do
#for i in `ls | grep gva3` ; do
#for i in let6 let5 let7 let8 let9 let10 ; do
#for i in `ls` ; do
  
  if [ -d $i ] ; then
      parent=`pwd`
      cd $i
      mkdir -p txt
      cd txt
      mv ../frames/*.txt* ./ 
      #../../Sort.sh
      #for ascii in `ls spill*/*.txt | grep -v -i readme | egrep -v "spec|etot|rate|size|ene"` ; do
      for ascii in `ls *.txt | grep -v -i readme | egrep -v "spec|etot|rate|size|ene"` ; do
	  echo "Converting $i/$ascii ..."
	  $convert $ascii
      done
      #../../MakePlots.sh
      cd $parent
  fi

done
