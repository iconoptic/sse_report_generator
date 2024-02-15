#!/bin/bash

#check for running process
if [[ $(ps aux | grep " $0" | wc -l) -ne 3 ]]; then
    exit
fi

cd "/home/btgrant/OneDrive/Student Evals/Qualtrics/Auto"
rFile="$(ls -lt /home/bgrant14/SSE_CSV/SE* | head -1 | rev | cut -d\  -f1 | rev)"
resultStr="No files added."
fileCount="$(find Student\ Eval\ Reports/ -type f | wc -l)"

if [[ $(echo $rFile | wc -l) -eq 1 ]]; then
	lSum="$(sha512sum se.csv | cut -d\  -f1)"
	rSum="$(sha512sum "$rFile" | cut -d\  -f1)"

	if [ "$lSum" != "$rSum" ]; then
		cp "$rFile" se.csv
		./gen-files.sh
		newFileNum=$(($(find Student\ Eval\ Reports/ -type f | wc -l)-$fileCount))
		resultStr="$newFileNum files added."
	fi
fi

echo "$(date +"%Y-%m-%d %T %Z"): $resultStr" >> eval_service.log
