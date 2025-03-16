import json
import re
from datetime import datetime, timedelta

def validate_name(name):
    """Validate that the name contains only alphabetic characters and spaces."""
    return bool(re.match(r'^[A-Za-z\s]+$', name))

def validate_date(date_str, format="%Y-%m-%d"):
    """Validate that the date is in the correct format."""
    try:
        datetime.strptime(date_str, format)
        return True
    except ValueError:
        return False

def is_at_least_21(birth_date_str, consent_date_str, format="%Y-%m-%d"):
    """Check if the recipient is at least 21 years old at the time of consent."""
    birth_date = datetime.strptime(birth_date_str, format)
    consent_date = datetime.strptime(consent_date_str, format)
    age = consent_date.year - birth_date.year - ((consent_date.month, consent_date.day) < (birth_date.month, birth_date.day))
    return age >= 21

def is_30_days_before(consent_date_str, sterilization_date_str, format="%Y-%m-%d"):
    """Check if the consent date is at least 30 days before the sterilization date."""
    consent_date = datetime.strptime(consent_date_str, format)
    sterilization_date = datetime.strptime(sterilization_date_str, format)
    return (sterilization_date - consent_date) >= timedelta(days=30)

def validate_json(json_data):
    """Validate the JSON data against the rules and return a list of errors."""
    errors = []

    # Validate name
    if not validate_name(json_data.get("recipient_name", "")):
        errors.append("Invalid recipient name. Name should contain only alphabetic characters and spaces.")

    # Validate dates
    birth_date = json_data.get("birth_date", "")
    consent_date = json_data.get("consent_date", "")
    sterilization_date = json_data.get("sterilization_date", "")

    if not validate_date(birth_date):
        errors.append("Invalid birth date format. Expected format: YYYY-MM-DD.")
    if not validate_date(consent_date):
        errors.append("Invalid consent date format. Expected format: YYYY-MM-DD.")
    if not validate_date(sterilization_date):
        errors.append("Invalid sterilization date format. Expected format: YYYY-MM-DD.")

    # Check if recipient is at least 21 years old
    if birth_date and consent_date and not is_at_least_21(birth_date, consent_date):
        errors.append("Recipient must be at least 21 years old at the time of consent.")

    # Check if consent date is at least 30 days before sterilization date
    if consent_date and sterilization_date and not is_30_days_before(consent_date, sterilization_date):
        errors.append("Consent date must be at least 30 days before the sterilization date.")

    return errors

def validate_and_create_output_json(input_file, output_file):
    """Validate JSON data and create a new JSON file with id and error details."""
    with open(input_file, 'r') as f:
        data = json.load(f)

    output_records = []

    for record in data:
        errors = validate_json(record)
        if errors:
            # If there are errors, include them in the output
            output_records.append({
                "id": record.get("id"),
                "error": errors  # List of errors
            })
        else:
            # If no errors, include "No Error"
            output_records.append({
                "id": record.get("id"),
                "error": "No Error"
            })

    # Save the output records to the output file
    with open(output_file, 'w') as f:
        json.dump(output_records, f, indent=4)

    print(f"Validation completed. Output saved to {output_file}.")


# Example JSON file (input)
input_json_file = r"D:\pdf files for code\test.json"

# Output JSON file for all records (valid and invalid)
output_json_file = r"D:\pdf files for code\sterilization_errors.json"

# Validate the JSON data and create an output JSON file
validate_and_create_output_json(input_json_file, output_json_file)