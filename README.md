# Scripts to generate reports from Qualtrics survey data

The script is designed up to parse and process results for a student survey hosted on Qualtrics. The python script generates reports organized by date, instructor, and patient. The output format is docx.

The input csv is assumed to have the name "se.csv" and may contain all surveys completed to date, or partial results transferred automatically via ssh.

## Usage

Set up the service as a cron job to run after Qualtrics sends a partial csv.

Or, run the script using `./gen-files.sh`