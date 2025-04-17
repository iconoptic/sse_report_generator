# SSE Report Generator

This project automates the generation of Microsoft Word reports from **Qualtrics survey data**, streamlining the analysis and documentation of **simulation-based educational sessions (SSEs)**. It was originally developed to support medical simulation feedback workflows, where dozens of reports had to be produced quickly and consistently.

## Features

- Parses **Qualtrics CSV exports** with structured survey data
- Organizes results by **date**, **instructor**, and **patient**
- Outputs `.docx` reports with readable formatting
- Ready for **batch processing** and scheduled execution

## How It Works

- Survey data is exported from Qualtrics as `.csv`
- Python scripts read and organize the responses
- Reports are formatted using the **python-docx** library
- Each session generates one or more `.docx` files grouped by instructor/patient/session

## Use Case

Used in **nursing simulation labs** to reduce the burden of manually summarizing survey results. Ensures standardization across:
- Instructors
- Patient case scenarios
- Clinical dates
- Student feedback

## Technologies

- **Python** (core logic and data processing)
- **Shell Scripting** (optional for automation)
- **python-docx** (for Word document generation)
- **Qualtrics CSV** structure awareness

## Example Output

The output folder contains one `.docx` per simulation grouping. Each document includes:
- Instructor and date header
- Aggregated survey comments
- Embedded formatting for readability

## Automation Friendly

You can use a **cron job** or task scheduler to run this project at regular intervals, ideal for organizations processing surveys weekly or monthly.

## License

MIT License
