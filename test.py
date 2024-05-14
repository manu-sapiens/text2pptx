import requests
import json

def main():
    # Read the OpenAI API key from the file
    try:
        with open('openai.key', 'r') as key_file:
            api_key = key_file.read().strip()
    except FileNotFoundError:
        print("Error: openai.key file not found.")
        return
    except Exception as e:
        print(f"Error reading openai.key file: {e}")
        return

    if not api_key:
        print("Error: OpenAI API key is empty.")
        return

    url = 'http://localhost:8501/llm/big_pptx'
    headers = {'Content-Type': 'application/json'}
    data = {
        "title": "Dungeons And Dragons",
        "subtitle": "A presentation on the popular tabletop role-playing game",
        "user_prompt": "Generate a presentation on what Dungeons And Dragons is|||Generate a presentation on Dungeons And Dragons Adventurers League and how it contributed to the renewal of interest in the game",
        "api_key": api_key,
        "template": "Bespoke",
        "filename": "example_output.pptx"
    }

    try:
        response = requests.post(url, headers=headers, data=json.dumps(data))
        response.raise_for_status()  # Raise an exception for HTTP errors

        # Get the presentation name from the response headers
        presentation_name = response.headers.get('Content-Disposition',"default.pptx").split("filename=")[-1].strip('"' + "'")
        print(f"Presentation name: {presentation_name}")
        
        # Save the response content to a file
        output_path = './test/'+presentation_name
        with open(output_path, 'wb') as f:
            f.write(response.content)
        print(f"Presentation saved to {output_path}")

    except requests.exceptions.RequestException as e:
        print(f"Error during request: {e}")

if __name__ == "__main__":
    main()
