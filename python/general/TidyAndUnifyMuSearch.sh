#!/bin/bash

for i in `ls | grep MuSearch` ; do echo $i ; cd $i ; pwd ; mv *.png frames/ ; mkdir root ; mv txt/*.root root/ ; cd ../ ; done
