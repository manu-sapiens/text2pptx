import json
import requests

PORT = "8501"

md = """
# Dungeons & Dragons - A Timeless Hobby
Author: Bobo
Date: Today

## Introduction
Hello

### Also Introduction
* Brief history of Dungeons & Dragons
* Importance in pop culture

#### And now a CARD

#### And another
* That’s exciting
  * in a way
  * 
#### What is that?
* I don’t know

### Why Dungeons & Dragons is Popular

* Creativity and Imagination
    * Creating unique characters and stories
    * Exploring fantastical worlds
* Social Interaction
* Strategic Thinking

### Key Elements of Dungeons & Dragons

* Player Characters
    1. Roles and classes
    1. Character development
* Dungeon Master
    * Role in guiding the story
    * Creating challenges and scenarios

## Conclusion
So I was thinking...

### So...
* Summary of D&D's impact
* Future of Dungeons & Dragons
* But did it work?
"""

data = {
    "filename": 'dnd3.pptx',
    "md": md,
    "template": "md_Bespoke.pptx",
    "options": {"sectionsExpand":"yes"}
}

url = f'http://localhost:{PORT}/pptx/from_md'
print("requesting to ", url)

headers = {'Content-Type': 'application/json'}

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

#curl -X POST http://localhost:8501/generate_presentation -H 'Content-Type: application/json' -d '{"template":"Urban_monochrome","filename":"dnd.pptx","title":"Dungeons & Dragons: A Billion-Dollar Franchise","subtitle":"Uncovering the Commercial Success of D&D", "slides":[{"heading":"Dungeons & Dragons: A Billion-Dollar Franchise","bullet_points":["Revenue: $822 million (2021)","Market Share: 75% of tabletop RPG market","Community: 50 million+ players worldwide","Partnerships: Netflix, Amazon, Paramount Pictures, and more","Cultural Impact: Featured in The New York Times, Forbes, NPR, and more"]}]}' -o ./test/output.pptx
#curl -X POST http://localhost:8501/ -H 'Content-Type: application/json' -d json_string -o ./test/output.pptx