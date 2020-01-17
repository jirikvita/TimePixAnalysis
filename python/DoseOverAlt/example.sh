#!/bin/bash

# jk 12.5.2019

cat GvaZurFeb2019/GvaZurFeb2019021.time
# Fri Feb 01 10:06:35.558146 2019
grep 100635 *.parsed
# GPS_PrgFrkGva_19012900.LOG.parsed:100635.000 7923.0

# need to e careful about exceptions, or do not use the data, or find closest?
# careful if multiple lines are found?
# need to add energy, convert to dose and count frames to divide afterwards!
# this to happen in py script which would already print dose as function of elevation
