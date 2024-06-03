import json
import sys
import os

def needs_backticks(value):
    """Check if the string value contains special characters that need backticks."""
    special_chars = {',', ':', '[', '{', '}', ']'}
    return any(char in value for char in special_chars)

def convert_to_custom_format(data):
    """Recursively convert a JSON object to a custom format."""
    if isinstance(data, dict):
        items = []
        for key, value in data.items():
            converted_key = key
            converted_value = convert_to_custom_format(value)
            items.append(f"{converted_key}: {converted_value}")
        return "{" + ", ".join(items) + "}"
    
    elif isinstance(data, list):
        items = [convert_to_custom_format(item) for item in data]
        return "[" + ", ".join(items) + "]"
    
    elif isinstance(data, str):
        # Check if the string needs backtick quoting
        if needs_backticks(data):
            return f"`{data}`"
        else:
            return data
    
    else:
        return str(data)

def process_file(input_filename):
    # Ensure the input file has a .json extension
    if not input_filename.endswith('.json'):
        print(f"Error: {input_filename} is not a JSON file.")
        return

    # Read JSON data from the file
    try:
        with open(input_filename, 'r') as json_file:
            json_data = json.load(json_file)
    except Exception as e:
        print(f"Error reading JSON file: {e}")
        return

    # Convert JSON data to custom format
    try:
        custom_format_data = convert_to_custom_format(json_data)
    except Exception as e:
        print(f"Error converting JSON to custom format: {e}")
        return

    # Generate the output filename with .txt extension
    output_filename = os.path.splitext(input_filename)[0] + '.txt'

    # Write the custom format data to the output file
    try:
        with open(output_filename, 'w') as txt_file:
            txt_file.write(custom_format_data)
        print(f"Converted data saved to: {output_filename}")
    except Exception as e:
        print(f"Error writing to output file: {e}")

if __name__ == "__main__":
    # Get the input filename from the command-line arguments
    if len(sys.argv) != 2:
        print("Usage: python json2txt.py <filename.json>")
    else:
        input_filename = sys.argv[1]
        process_file(input_filename)
