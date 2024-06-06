import requests
import json, sys
#from adventure import ADVENTURE1
from schemas import GPT_TOOL_SLIDE_SCHEMA
import uuid

def gen_pptx(output_path, template = "Entrevue_template_advanced", URL = "pptx/generate_presentation_advanced"):
    json_response = ""
    try:
        with open(output_path, 'r') as f:
            json_response = f.read()
    except FileNotFoundError:
        print(f"File {output_path} not found")
        exit(1)
    #

    print("json_slides = ", json_response)
    json_dict = json.loads(json_response)
    print("json_dict = ", json_dict)
    slides = json.dumps(json_dict["slides"])
    print("slides = ", slides)
    result_file_name = f"{uuid.uuid4().hex}.pptx"
    data = {
        "filename": result_file_name,
        "slides": slides,
        "template": template,
        "title": "Dungeons And Dragons",
        "subtitle": "A presentation on the popular tabletop role-playing game"
    }
    
    
    url = f'http://localhost:{PORT}/{URL}'
    print("requesting to ", url)

    headers = {'Content-Type': 'application/json'}


    try:
        response = requests.post(url, headers=headers, data=json.dumps(data))
        response.raise_for_status()  # Raise an exception for HTTP errors

        # Get the presentation name from the response headers
        json_file = response.headers.get('Content-Disposition',"default.pptx").split("filename=")[-1].strip('"' + "'")
        print(f"Presentation name: {json_file}")
        
        # Save the response content to a file
        output_path = './test/'+json_file
        with open(output_path, 'wb') as f:
            f.write(response.content)
        print(f"Presentation saved to {output_path}")

    except requests.exceptions.RequestException as e:
        print(f"Error during request: {e}")
    #
#            
    

PORT = 8501
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

        url = f'http://localhost:{PORT}/llm/big_pptx'
        #url = 'https://text2pptx.onrender.com/llm/big_pptx'
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
            json_file = response.headers.get('Content-Disposition',"default.pptx").split("filename=")[-1].strip('"' + "'")
            print(f"Presentation name: {json_file}")
            
            # Save the response content to a file
            output_path = './test/'+json_file
            with open(output_path, 'wb') as f:
                f.write(response.content)
            print(f"Presentation saved to {output_path}")

        except requests.exceptions.RequestException as e:
            print(f"Error during request: {e}")
        #
    #
            
    if test_number == 2:
        url = f'http://localhost:{PORT}/llm/infer'
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
            json_file = response.headers.get('Content-Disposition',"result.out").split("filename=")[-1].strip('"' + "'")
            print(f"Presentation name: {json_file}")
            
            # Save the response content to a file
            output_path = './test/'+json_file
            with open(output_path, 'wb') as f:
                f.write(response.content)
            print(f"Presentation saved to {output_path}")

        except requests.exceptions.RequestException as e:
            print(f"Error during request: {e}")
                    
        
        pass        
    #
    

    if test_number == 3:

        url = f'http://localhost:{PORT}/llm/big_dm_slides'
        print("requesting to ", url)
        
        headers = {'Content-Type': 'application/json'}
        data = {
            "title": "Dungeons And Dragons",
            "subtitle": "A presentation on the popular tabletop role-playing game",
            "user_prompt": "Generate a presentation on what Dungeons And Dragons is|||Generate a presentation on Dungeons And Dragons Adventurers League and how it contributed to the renewal of interest in the game",
            "api_key": api_key,
            "filename": "example_output3.md",
            "options": {"sectionsExpand":"yes"}
        }
        #            "template": "md_Bespoke.pptx",

        try:
            response = requests.post(url, headers=headers, data=json.dumps(data))
            response.raise_for_status()  # Raise an exception for HTTP errors

            # Get the presentation name from the response headers
            json_file = response.headers.get('Content-Disposition',"default.md").split("filename=")[-1].strip('"' + "'")
            print(f"Presentation name: {json_file}")
            
            # Save the response content to a file
            output_path = './test/'+json_file
            with open(output_path, 'wb') as f:
                f.write(response.content)
            print(f"Presentation saved to {output_path}")




        except requests.exceptions.RequestException as e:
            print(f"Error during request: {e}")
        #
    #
    
    if test_number == 4:

        markdown_only = True
        url = f'http://localhost:{PORT}/llm/big_dm_slides'
        print("requesting to ", url)
        
        headers = {'Content-Type': 'application/json'}
        data = {
            "title": "Dungeons And Dragons",
            "subtitle": "A presentation on the popular tabletop role-playing game",
            "user_prompt": "Generate a presentation on what Dungeons And Dragons is|||Generate a presentation on Dungeons And Dragons Adventurers League and how it contributed to the renewal of interest in the game",
            "api_key": api_key,
            "filename": "example_output5.pptx",
            "options": {"sectionsExpand":"yes"},
            "template": "md_Bespoke.pptx",
            "markdown_only": markdown_only
        }
        #            "template": "md_Bespoke.pptx",

        try:
            response = requests.post(url, headers=headers, data=json.dumps(data))
            response.raise_for_status()  # Raise an exception for HTTP errors

            # Get the presentation name from the response headers
            json_file = response.headers.get('Content-Disposition',"default.pptx").split("filename=")[-1].strip('"' + "'")
            print(f"Presentation name: {json_file}")
            
            
            # Save the response content to a file
            output_path = f'./test/{json_file}.md'
            with open(output_path, 'wb') as f:
                f.write(response.content)
                f.close()
            print(f"Presentation saved to {output_path}")

            markdown = ""
            try:
                with open(output_path, 'r') as f:
                    markdown = f.read()
            except FileNotFoundError:
                print(f"File {output_path} not found")
                exit(1)
            #

            print("markdown = ", markdown)
            
            data = {
                "filename": 'dnd4.pptx',
                "markdown": markdown,
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
                json_file = response.headers.get('Content-Disposition',"default.pptx").split("filename=")[-1].strip('"' + "'")
                print(f"Presentation name: {json_file}")
                
                # Save the response content to a file
                output_path = './test/'+json_file
                with open(output_path, 'wb') as f:
                    f.write(response.content)
                print(f"Presentation saved to {output_path}")

            except requests.exceptions.RequestException as e:
                print(f"Error during request: {e}")
            #
        #            

        except requests.exceptions.RequestException as e:
            print(f"Error during request: {e}")
        #
    #
          
    if test_number == 5:

        markdown_only = True
        url = f'http://localhost:{PORT}/llm/text_to_slides'
        print("requesting to ", url)
        
        headers = {'Content-Type': 'application/json'}
        data = {
            "title": "Dungeons And Dragons",
            "subtitle": "A presentation on the popular tabletop role-playing game",
            "user_prompt": "Generate a presentation on what Dungeons And Dragons is|||Generate a presentation on Dungeons And Dragons Adventurers League and how it contributed to the renewal of interest in the game",
            "api_key": api_key,
            "filename": "test_output_option_5",
            "options": {"sectionsExpand":"yes"},
            "template": "md_Bespoke.pptx"
        }
        #            "template": "md_Bespoke.pptx",

        try:
            response = requests.post(url, headers=headers, data=json.dumps(data))
            response.raise_for_status()  # Raise an exception for HTTP errors

            # Get the presentation name from the response headers
            json_file = response.headers.get('Content-Disposition',"default.pptx").split("filename=")[-1].strip('"' + "'")
            print(f"Presentation name: {json_file}")
            
            
            # Save the response content to a file
            output_path = f'./out/{json_file}.final.pptx'
            with open(output_path, 'wb') as f:
                f.write(response.content)
                f.close()
            print(f"Presentation saved to {output_path}")

        except requests.exceptions.RequestException as e:
            print(f"Error during request: {e}")
        #
    #

    if test_number == 6:

        url = f'http://localhost:{PORT}/llm/infer'
        print("requesting to ", url)
        
        headers = {'Content-Type': 'application/json'}
        data = {
            "ai_type":"openai",
            "model":"gpt-3.5-turbo",
            "schema": GPT_TOOL_SLIDE_SCHEMA,
            "user_prompt": "Generate detailed slides using the provided schema on what Dungeons And Dragons is, its origin, how to play, what is a DM, why it is popular again. Use bullet points, numbered lists, etc. to present a clear and well organized presentation.",
            "api_key": api_key,
            "filename": "example_output_10.json"
        }
        #            "template": "md_Bespoke.pptx",

        try:
            response = requests.post(url, headers=headers, data=json.dumps(data))
            response.raise_for_status()  # Raise an exception for HTTP errors

            # Get the presentation name from the response headers
            json_file = response.headers.get('Content-Disposition',"default.json").split("filename=")[-1].strip('"' + "'")
            print(f"json_file name: {json_file}")
                                    
            # Save the response content to a file
            output_path = f'./test/{json_file}.json'
            with open(output_path, 'wb') as f:
                f.write(response.content)
                f.close()
            print(f"json_file saved to {output_path}")

            gen_pptx(output_path)
            
        except requests.exceptions.RequestException as e:
            print(f"Error during request: {e}")
        #
    #

    if test_number == 7:
        output_path = f'./test/manu_test.json'
        gen_pptx(output_path)

    if test_number == 8:
        output_path = f'./test/manu_test.json'
        gen_pptx(output_path,"Entrevue_template" ,"pptx/generate_presentation")
                      
if __name__ == "__main__":
    # read the test number as the first passed argument
    test_number = 1
    if len(sys.argv) > 1:
        test_number = int(sys.argv[1])
    #
    print(f"Running test {test_number}")
    print("----------------")
    main(test_number)
#