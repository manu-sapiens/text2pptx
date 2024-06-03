import json
import sys
import os
from app import decode_schema_string

def process_file(input_filename):
    # Ensure the input file has a .json extension
    schema_string = ""
    
    
    try:
        with open(input_filename, 'r') as text_file:
            # load text from file
            schema_string = text_file.read()
    except Exception as e:
        print(f"Error reading text file: {e}")
        return
    
    # Convert JSON data to custom format
    json_string = ""
    try:
        json_string = decode_schema_string(schema_string)
    except Exception as e:
        print(f"Error converting JSON to custom format: {e}")
        return
    #
    
    # Generate the output filename with .txt extension
    output_filename = os.path.splitext(input_filename)[0] + '.json'

    # Write the custom format data to the output file
    try:
        with open(output_filename, 'w') as json_file:
            json_file.write(json_string)
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
