import json

def append_acceptance_probability(original_file, probability_file, output_file):
    """Append acceptance probability to the original JSON file based on matching IDs."""
    # Load the original JSON file
    with open(original_file, 'r') as f:
        original_data = json.load(f)

    # Load the probability JSON file
    with open(probability_file, 'r') as f:
        probability_data = json.load(f)

    # Create a dictionary for quick lookup of acceptance probabilities by ID
    probability_dict = {entry["id"]: entry["AcceptanceProbability"] for entry in probability_data}

    # Append acceptance probability to the original data
    updated_data = []
    for entry in original_data:
        id = entry["id"]
        if id in probability_dict:
            # Add the acceptance probability to the entry
            entry["AcceptanceProbability"] = probability_dict[id]
        else:
            # If no matching ID is found, set acceptance probability to None or a default value
            entry["AcceptanceProbability"] = None
        updated_data.append(entry)

    # Save the updated data to the output file
    with open(output_file, 'w') as f:
        json.dump(updated_data, f, indent=4)

    print(f"Updated data saved to {output_file}.")

# Example file paths
original_json_file = r"D:\pdf files for code\sterilization_errors.json"  # Original JSON file with id and errors
probability_json_file = r"D:\pdf files for code\test_full_predictions.json"  # JSON file with acceptance probabilities
output_json_file = r"D:\pdf files for code\final_output.json"  # Output file with appended acceptance probabilities

# Append acceptance probabilities and save the updated JSON
append_acceptance_probability(original_json_file, probability_json_file, output_json_file)

# Example file paths
original_json_file = r"D:\pdf files for code\sterilization_errors.json"  # Original JSON file with id and errors
probability_json_file = r"D:\pdf files for code\test_full_predictions.json"  # JSON file with acceptance probabilities
output_json_file = r"D:\pdf files for code\final_output.json"  # Output file with appended acceptance probabilities

# Append acceptance probabilities and save the updated JSON
append_acceptance_probability(original_json_file, probability_json_file, output_json_file)