#!/bin/bash

rFile="$(find ~/Downloads | grep "$(date +'%B+%-d,+%Y')")"

mv "$rFile" ./se.csv
./gen-files.sh
