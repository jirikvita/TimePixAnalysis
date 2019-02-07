#!/bin/bash

cat HoughTransfFrames.py | grep MuS | cut -d _ -f 2 | cut -d x -f 1 | awk 'BEGIN{n=1};{n=n+$1};END{print n};'

