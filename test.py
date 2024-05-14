import requests
import json
from adventure import ADVENTURE1
def main(test_number):
    
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

    if test_number == 1:

        #url = 'http://localhost:8501/llm/big_pptx'
        url = 'https://text2pptx.onrender.com/llm/big_pptx'
        print("requesting to ", url)
        
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
        #
    #
            
    if test_number == 2:
        url = 'http://localhost:8501/llm/infer'
        print("requesting to ", url)
        
        headers = {'Content-Type': 'application/json'}
        data = {
            "system_prompt": "Extract the entities in the prompt and return it as a json",
            "model":"gpt-4o",
            "user_prompt": ADVENTURE1,
            "api_key": api_key,
            "filename": "adventure.json",
            "schema": "{`title`:`Entities and Relationships`,`type`:`object`,`properties`:{`entities`:{`type`:`array`,`items`:{`type`:`object`,`properties`:{`id`:{`type`:`string`,`description`:`Unique identifier for the entity`},`name`:{`type`:`string`,`description`:`Name of the entity`},`category`:{`type`:`string`,`description`:`Main category of the entity`},`subcategory`:{`type`:`string`,`description`:`Subcategory under the main category`},`related_entities`:{`type`:`array`,`items`:{`type`:`object`,`properties`:{`id`:{`type`:`string`,`description`:`Unique identifier of the related entity`},`relation_type`:{`type`:`string`,`description`:`Type of the relationship`},`relation_subtype`:{`type`:`string`,`description`:`Subtype of the relationship`},`commentary`:{`type`:`string`,`description`:`Commentary or description of the relationship`}},`required`:[`id`,`relation_type`,`relation_subtype`]},`description`:`List of related entities`}},`required`:[`id`,`name`,`category`,`subcategory`]}}},`required`:[`entities`]}"
        }

        try:
            response = requests.post(url, headers=headers, data=json.dumps(data))
            response.raise_for_status()  # Raise an exception for HTTP errors

            print("----------")
            print("response = ", response)
            print("----------")
            print("headers =", response.headers)
            print("----------")

            # Get the presentation name from the response headers
            presentation_name = response.headers.get('Content-Disposition',"result.out").split("filename=")[-1].strip('"' + "'")
            print(f"Presentation name: {presentation_name}")
            
            # Save the response content to a file
            output_path = './test/'+presentation_name
            with open(output_path, 'wb') as f:
                f.write(response.content)
            print(f"Presentation saved to {output_path}")

        except requests.exceptions.RequestException as e:
            print(f"Error during request: {e}")
                    
        
        pass
            
    #

if __name__ == "__main__":
    main(1)
