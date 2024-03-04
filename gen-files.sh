#!/bin/bash

verbose=0
while getopts 'v' OPTION; do
	case "$OPTION" in
		v)
			verbose=1
			;;
		?)
			echo "Run the script with no arguments."
			echo "Add '-v' to print the html output."
			exit 1
			;;
	esac
done

#Pre-process:

#Remove newlines
if [[ $(tail -n+4 se.csv | grep "^[^0-9]" | wc -l) -gt 0 ]]; then
	awk -v ORS= '{sub(/\r$/,"\n")} 1' se.csv > .tmp
	mv .tmp se.csv
fi

#Survey updated 2/29/2024 -- all previous results will no longer be processed by updated python script
grep -v "^202[23]" se.csv | while read line; do
	if test "$(echo "$line" | grep -v "^[2024]" | wc -l)" -eq 1; then
		echo "$line"
	elif [[ "$(echo "$line" | cut -d\  -f1)" > "2024-02-29" ]]; then
		echo "$line"
	fi
done > .tmp
mv .tmp se.csv

fileName=""
subDir=""
python3 parse-out.py | while read line; do
	if [ "$(echo $line | grep -E ^'<>:')" ]; then
		if [ "$fileName" != "" ]; then
			subDir="$(echo "$fileName" | cut -d\  -f1 | cut -d\- -f3)"
			if [[ $(find Student\ Eval\ Reports/ -mindepth 1 -type d | grep "$subDir" | wc -l) -eq 0 ]]; then
				mkdir "Student Eval Reports/$subDir"
			fi
			pandoc temp.md -o "Student Eval Reports/$subDir/$fileName"
			ls | grep "$(echo "$fileName" | sed 's/.docx//g')" | grep ".png$" | while read line; do rm "$line"; done
		fi
		lastfn="$fileName"
		fileName="$(echo $line | cut -d\: -f2 | sed 's/\//-/g')"
		echo $fileName
		echo '' > temp.md
	else
		echo "$line" >> temp.md
		if [[ $verbose -eq 1 ]]; then
			echo "$line"
		fi
	fi
done
fileName="$(echo $(echo $(cat temp.md | grep '^##' | head -3 | sed 's/^## //g')).docx)"
subDir="$(echo "$fileName" | cut -d\  -f1 | cut -d\- -f3)"
pandoc temp.md -o "Student Eval Reports/$subDir/$fileName"
rm temp.md
ls | grep "$(echo "$fileName" | sed 's/.docx//g')" | grep ".png$" | while read line; do rm "$line"; done


#rm *.png
