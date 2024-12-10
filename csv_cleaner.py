import argparse
import csv
import re
import os
import sys

def clean_csv(input_file, output_file, remove_duplicates, validate_email):
    if not os.path.exists(input_file):
        print(f"Error: The file {input_file} does not exist.")
        sys.exit(1)

    cleaned_data = []
    seen = set()  # For duplicate removal
    email_regex = re.compile(r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$")

    try:
        with open(input_file, mode="r", newline="", encoding="utf-8") as infile:
            reader = csv.DictReader(infile)
            if not reader.fieldnames:
                print("Error: CSV file is empty or improperly formatted.")
                sys.exit(1)

            for row in reader:
                # Remove duplicates
                if remove_duplicates:
                    identifier = row.get("Email", "")  # Assume "Email" column
                    if identifier in seen:
                        continue
                    seen.add(identifier)

                # Validate email
                if validate_email:
                    email = row.get("Email", "")
                    if not email_regex.match(email):
                        continue

                cleaned_data.append(row)

        # Write to output file
        with open(output_file, mode="w", newline="", encoding="utf-8") as outfile:
            writer = csv.DictWriter(outfile, fieldnames=reader.fieldnames)
            writer.writeheader()
            writer.writerows(cleaned_data)

        print(f"Cleaned data written to {output_file}")

    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)

def main():
    parser = argparse.ArgumentParser(description="A tool to clean up messy CSV data.")
    parser.add_argument("-i", "--input", required=True, help="Path to the input CSV file.")
    parser.add_argument("-o", "--output", required=True, help="Path to the output CSV file.")
    parser.add_argument("--remove-duplicates", action="store_true", help="Remove duplicate rows based on the 'Email' column.")
    parser.add_argument("--validate-email", action="store_true", help="Validate email addresses in the 'Email' column.")
    parser.add_argument("-h", "--help", action="help", help="Show this help message and exit.")

    args = parser.parse_args()

    clean_csv(
        input_file=args.input,
        output_file=args.output,
        remove_duplicates=args.remove_duplicates,
        validate_email=args.validate_email,
    )

if __name__ == "__main__":
    main()
