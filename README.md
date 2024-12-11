# CSV Cleaner

## Purpose
This Python script processes a CSV file to remove duplicates and/or validate data, making it useful for cleaning up messy datasets.

## Features
- Remove duplicate rows based on the "Email" column.
- Validate email fields using a regular expression.
- Save cleaned data to a new CSV file.

## Usage
Run the script with the following options:
```bash
python csv_cleaner.py -i input.csv -o output.csv [--remove-duplicates] [--validate-email]
```

### Arguments
- `-i` or `--input`: Path to the input CSV file.
- `-o` or `--output`: Path to the output CSV file.
- `--remove-duplicates`: Remove duplicate rows.
- `--validate-email`: Validate email addresses.

### Example
```bash
python csv_cleaner.py -i contacts.csv -o cleaned_contacts.csv --remove-duplicates --validate-email
```

## Why It’s Useful
Many professionals encounter CSV files with duplicate rows or improperly formatted fields (e.g., invalid emails). This script automates the cleanup process, saving time and ensuring data integrity.
