import requests
import json, sys
#from adventure import ADVENTURE1
from schemas import GPT_TOOL_SLIDE_SCHEMA
import uuid
from pathlib import Path

def gen_pptx(output_path, title, subtitle, template = "Entrevue_template_advanced", url = "pptx/generate_presentation_advanced"):
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
        "title": title,
        "subtitle": subtitle
    }
    
    
    url = f'http://localhost:{PORT}/{url}'
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
        json_path = f'./input/test_slide_advanced.json'
        gen_pptx(json_path, "D&D", "A case study")

    if test_number == 8:
        json_path = f'./input/test_slide_simple.json'
        gen_pptx(json_path,"Presentation Title", "Presentation Subtitle", "Entrevue_template" ,"pptx/generate_presentation")

    if test_number == 9:
        from references import GPT_TOOL_SCHEMA__BOOK_REFERENCE_small

        print(GPT_TOOL_SCHEMA__BOOK_REFERENCE_small)
        url = f'http://localhost:{PORT}/llm/infer'
        print("requesting to ", url)
        
        headers = {'Content-Type': 'application/json'}
        data = {
            "system_prompt": "Recommend a book based on the user's input, explain your choice, provide the url and book title as a json according to the provided json schema.",
            "model":"gpt-4o",
            "user_prompt": "I'm looking for a classic science fiction book to read. What would you recommend?",
            "api_key": api_key,
            "filename": "book.json",
            "schema": GPT_TOOL_SCHEMA__BOOK_REFERENCE_small
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

    if test_number == 10:
        from references import GPT_TOOL_SCHEMA_FINANCIAL_REFERENCES
        url = f'http://localhost:{PORT}/llm/infer'
        print("requesting to ", url)
        
        headers = {'Content-Type': 'application/json'}
        data = {
            "system_prompt": "Recommend a financial reference based on the user's input, explain your choice, provide the url and book title as a json according to the provided json schema.",
            "model":"gpt-4o",
            "user_prompt": "I'm looking for something to help me understand venture capital and what interview questions I'm likely to get for a VC job",
            "api_key": api_key,
            "filename": "book.json",
            "schema": GPT_TOOL_SCHEMA_FINANCIAL_REFERENCES
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

    if test_number == 11:
        from references import GPT_TOOL_SCHEMA_30_REFS, INSTRUCTION_30_REFS

        resume_string = ""
        # read resume from input/resume.txt
        try:
            with open('input/resume.txt', 'r') as resume_file:
                resume_string = resume_file.read()
        except FileNotFoundError:
            print("Error: resume.txt file not found.")
            return
        #
        
        knowledge_gap_string = ""
        # read the knowledge_gap from input/knowledge_gap.txt
        try:
            with open('input/knowledge_gap.txt', 'r') as knowledge_gap_file:
                knowledge_gap_string = knowledge_gap_file.read()
        except FileNotFoundError:
            print("Error: knowledge_gap.txt file not found.")
            return
        #

        job_description_string = ""
        # read the job_description from input/job_description.txt
        try:
            with open('input/job_description.txt', 'r') as job_description_file:
                job_description_string = job_description_file.read()
        except FileNotFoundError:
            print("Error: job_description.txt file not found.")
            return

        #instruction_string = INSTRUCTION_30_REFS
        instruction_string = "Based on the KNOWLEDGE GAP and the JOB DESCRIPTION, generate 6 groups of up to 5 references each. Each group should be a list of up to 5 references that would help the user fill in the gaps in their knowledge. Provide the references as a json according to the provided json schema. Do not reuse references from one group to another."
        #instruction_string = "Based on the KNOWLEDGE GAP, generate 6 groups of up to 5 references each. Each group should be a list of up to 5 references that would help the user fill in the gaps in their knowledge. Provide the references as a json according to the provided json schema. Do not reuse references from one group to another."
        #instruction_string = "For each gap identified in the KNOWLEDGE GAP section, generate up to 5 references that will help the candidate fill that gap in their knowledge. Ensure that each reference is not used more than once. Provide the references as a json according to the provided json schema. "
        prompt_string = ""
        #prompt_string += "<RESUME>\n"+resume_string+"\n</RESUME>\n\n"
        prompt_string += "<KNOWLEDGE_GAP>\n"+knowledge_gap_string+"\n</KNOWLEDGE_GAP>\n\n"
        prompt_string += "<JOB_DESCRIPTION>\n"+job_description_string+"\n</JOB_DESCRIPTION>\n\n"


        url = f'http://localhost:{PORT}/llm/infer'
        print("requesting to ", url)
        
        headers = {'Content-Type': 'application/json'}
        data = {
            "system_prompt": instruction_string,
            "model":"gpt-4o",
            "user_prompt": prompt_string,
            "api_key": api_key,
            "filename": "30ref.json",
            "schema": GPT_TOOL_SCHEMA_30_REFS
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
            output_path = Path('./test/',json_file+"_"+uuid.uuid4().hex+".txt")
            with open(output_path, 'wb') as f:
                f.write(response.content)
            print(f"Presentation saved to {output_path}")
        except requests.exceptions.RequestException as e:
            print(f"Error during request: {e}")
        #                    
    #         

    if test_number == 12:
        from references import GPT_TOOL_SCHEMA_JULY

        resume_string = ""
        # read resume from input/resume.txt
        try:
            with open('input/resume.txt', 'r') as resume_file:
                resume_string = resume_file.read()
        except FileNotFoundError:
            print("Error: resume.txt file not found.")
            return
        #
        
        knowledge_gap_string = ""
        # read the knowledge_gap from input/knowledge_gap.txt
        try:
            with open('input/knowledge_gap.txt', 'r') as knowledge_gap_file:
                knowledge_gap_string = knowledge_gap_file.read()
        except FileNotFoundError:
            print("Error: knowledge_gap.txt file not found.")
            return
        #

        job_description_string = ""
        # read the job_description from input/job_description.txt
        try:
            with open('input/job_description.txt', 'r') as job_description_file:
                job_description_string = job_description_file.read()
        except FileNotFoundError:
            print("Error: job_description.txt file not found.")
            return

        #instruction_string = INSTRUCTION_30_REFS
        #instruction_string = "Based on the KNOWLEDGE GAP and the JOB DESCRIPTION, generate 6 groups of up to 5 references each. Each group should be a list of up to 5 references that would help the user fill in the gaps in their knowledge. Provide the references as a json according to the provided json schema. Do not reuse references from one group to another."
        #instruction_string = "Based on the KNOWLEDGE GAP, generate 6 groups of up to 5 references each. Each group should be a list of up to 5 references that would help the user fill in the gaps in their knowledge. Provide the references as a json according to the provided json schema. Do not reuse references from one group to another."
        instruction_string = "List each gap present in the KNOWLEDGE GAP section. For each gap identified in the KNOWLEDGE GAP section, generate up to 5 references that will help the candidate fill that gap in their knowledge. Ensure that each reference is not used more than once. Provide the references as a json according to the provided json schema. "
        prompt_string = ""
        #prompt_string += "<RESUME>\n"+resume_string+"\n</RESUME>\n\n"
        prompt_string += "<KNOWLEDGE_GAP>\n"+knowledge_gap_string+"\n</KNOWLEDGE_GAP>\n\n"
        #prompt_string += "<JOB_DESCRIPTION>\n"+job_description_string+"\n</JOB_DESCRIPTION>\n\n"

        print("KNOWLEDGE GAP = ", knowledge_gap_string);
        url = f'http://localhost:{PORT}/llm/infer'
        print("requesting to ", url)
        
        headers = {'Content-Type': 'application/json'}
        data = {
            "system_prompt": instruction_string,
            "model":"gpt-4o",
            "user_prompt": prompt_string,
            "api_key": api_key,
            "filename": "gaps_refs.json",
            "schema": GPT_TOOL_SCHEMA_JULY
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
            output_path = Path('./test/',json_file+"_"+uuid.uuid4().hex+".txt")
            with open(output_path, 'wb') as f:
                f.write(response.content)
            print(f"Presentation saved to {output_path}")
        except requests.exceptions.RequestException as e:
            print(f"Error during request: {e}")
        #                    
    # 

    if test_number == 13:
        from references import GPT_TOOL_SCHEMA_JULY4, LINK_REFERENCES

        schema = GPT_TOOL_SCHEMA_JULY4
        resume_string = ""
        # read resume from input/resume.txt
        try:
            with open('input/resume.txt', 'r') as resume_file:
                resume_string = resume_file.read()
        except FileNotFoundError:
            print("Error: resume.txt file not found.")
            return
        #
        
        knowledge_gap_string = ""
        # read the knowledge_gap from input/knowledge_gap.txt
        try:
            with open('input/knowledge_gap.txt', 'r') as knowledge_gap_file:
                knowledge_gap_string = knowledge_gap_file.read()
        except FileNotFoundError:
            print("Error: knowledge_gap.txt file not found.")
            return
        #

        job_description_string = ""
        # read the job_description from input/job_description.txt
        try:
            with open('input/job_description.txt', 'r') as job_description_file:
                job_description_string = job_description_file.read()
        except FileNotFoundError:
            print("Error: job_description.txt file not found.")
            return

        instruction_string = "List each gap present in the KNOWLEDGE GAP section. For each identified gap, generate 2 to 5 references taken from the <REFERENCES> section that can help the candidate fill that gap in their knowledge. Ensure that each gap is addressed. Ensure that each reference is not used more than once. Provide the references as a json according to the provided json schema. "
        instruction_string += LINK_REFERENCES
        prompt_string = "<KNOWLEDGE_GAP>\n"+knowledge_gap_string+"\n</KNOWLEDGE_GAP>\n\n"

        print("KNOWLEDGE GAP = ", knowledge_gap_string);
        url = f'http://localhost:{PORT}/llm/infer'
        print("requesting to ", url)
        
        headers = {'Content-Type': 'application/json'}
        data = {
            "system_prompt": instruction_string,
            "model":"gpt-4o",
            "user_prompt": prompt_string,
            "api_key": api_key,
            "filename": "gaps_refs.json",
            "schema": schema
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
            output_path = Path('./test/',json_file+"_"+uuid.uuid4().hex+".txt")
            with open(output_path, 'wb') as f:
                f.write(response.content)
            print(f"Presentation saved to {output_path}")
        except requests.exceptions.RequestException as e:
            print(f"Error during request: {e}")
        #                    
    #   
    # 
    # 
    # 
    #

    if test_number == 14:
        
        knowledge_gap_string = ""
        # read the knowledge_gap from input/knowledge_gap.txt
        try:
            with open('input/knowledge_gap.txt', 'r') as knowledge_gap_file:
                knowledge_gap_string = knowledge_gap_file.read()
        except FileNotFoundError:
            print("Error: knowledge_gap.txt file not found.")
            return
        #

    
        url = f'http://localhost:{PORT}/llm/remedial_resources'
        print("requesting to ", url)
        
        headers = {'Content-Type': 'application/json'}
        data = {
            "gaps": knowledge_gap_string,
            "api_key": api_key,
            "model:": "gpt-4o",
            "filename": "gaps_refs14.json"        
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
            output_path = Path('./test/',json_file+"_"+uuid.uuid4().hex+".txt")
            with open(output_path, 'wb') as f:
                f.write(response.content)
            print(f"Presentation saved to {output_path}")
        except requests.exceptions.RequestException as e:
            print(f"Error during request: {e}")
        #                    
    # 

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