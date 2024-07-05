print("-------- START -----------")
import os
from flask import Flask, request, send_file, jsonify
import json5
import io
import tempfile
import logging
import time
import requests
from pathlib import Path
import tempfile
from pptx_helper import generate_powerpoint_presentation, generate_powerpoint_presentation_advanced
from global_config import GlobalConfig
import io
import json
import replicate
import re
import zipfile
import subprocess
import uuid
from schemas import BIG_PPTX_SCHEMA, BIG_DM_SLIDES_SCHEMA, GPT_TOOL_SLIDE_SCHEMA

#import aspose.slides

separator = '|||'
OBSCURE_CHARACTER = 'ˆ'
MD_TEMPLATE_PATH = "../md_templates/"
app = Flask(__name__, static_folder='static')
MD_PROCESSING_SCRIPT = Path(Path(__file__).parent,"md2pptx", "md2pptx.py")
#BIG_PPTX_SCHEMA = "{type:object,properties:{slides:{type:array,items:{type:object,properties:{heading:{title:Heading,description:The_slide_Heading,type:string},bullet_points:{title:Bullet_Points,description:The_bullet_points,type:array,items:{type:string}}},required:[heading,bullet_points]}}},required:[slides]}"
#BIG_DM_SLIDES_SCHEMA = "{type: object, properties: {slides: {type: array, items: {oneOf: [{type: object, properties: {introduction: {type: object, properties: {title: {type: string, description: The title text for the Introduction slide}, subtitle: {type: string, description: The optional subtitle text for the Introduction slide}}, required: [title]}}, required: [introduction]}, {type: object, properties: {section: {type: object, properties: {title: {type: string, description: The title text for the Section slide}, subtitle: {type: string, description: The optional subtitle text for the Section slide}}, required: [title]}}, required: [section]}, {type: object, properties: {bulletpoints: {type: object, properties: {elements: {type: array, items: {type: object, properties: {text: {type: string, description: Plain text element for the bullet point}, bullet_level: {type: string, enum: [1, 2, 3, 4, 5, 6], description: The indentation level for bullet points}}, required: [text, bullet_level]}, description: Array of text and bullet elements for the Bulletpoints slide}}, required: [elements]}}, required: [bulletpoints]}]}}}, required: [slides]}"



def convert_pptx_to_pdf(input_file: str, output_file: str):
    """
    Convert a PPTX file to a PDF file.

    :param input_file: Path to the input PPTX file.
    :param output_file: Path where the output PDF file will be saved.
    """
    with slides.Presentation(input_file) as presentation:
        presentation.save(output_file, slides.export.SaveFormat.PDF)
    #
#
    
def generate_presentation(slides: str, template_name: str = 'Blank', format: str = 'pptx') -> bytes:
    output_file_path = Path(tempfile.mkstemp(suffix=".pptx")[1])
    generate_powerpoint_presentation(slides, output_file_path=output_file_path, slides_template=template_name)
    print("-------------------------")
    print("Powerpoint generated using template:", template_name)
    
    if (format == 'pdf'):
        pdf_output_file = Path(tempfile.mkstemp(suffix=".pdf")[1])
        print("Generating pdf from powerpoint")
        convert_pptx_to_pdf(output_file_path, pdf_output_file)
        with open(pdf_output_file, "rb") as f:
            return f.read()
        #
    else:
        with open(output_file_path, "rb") as f:
            return f.read()
        #
    #
#

def call_openai_api(api_key, model, messages, tools=None):
    
    result = None
    error = None
    
    #print("************************")
    #print("api_key = ", api_key)
    #print("model= ", model)    
    #print("messages = ", messages)
    #print("tools = ", tools)
    #print("************************")
    
    url = 'https://api.openai.com/v1/chat/completions'
    headers = {
        'Authorization': f'Bearer {api_key}',
        'Content-Type': 'application/json',
    }
    data = None

    response_format = {"type": "json_object"}
    if tools:
        tool_choice = "required"
        
        data = json.dumps({
            "model": model,
            "messages": messages,
            "tools": tools,
            "tool_choice": tool_choice,
            "response_format": response_format
        })
    else:
        data = json.dumps({
            "model": model,
            "messages": messages,
            "response_format": response_format
        })
    #        
        
    response = requests.post(url, headers=headers, data=data)
    print("response = ", response)
    
    usage = None
    finish_reason = None


    if response.status_code == 200:
        
        status_code = None
        response_headers = None
        response_text = None
        try:
            print("response.status_code = ", response.status_code)
            status_code = response.status_code
            response_headers = response.headers
            response_text = response.text
        except Exception as e:
            print("Error accessing response data: ", e)
            error = f"Error accessing response data for response = {response}"
        #


        # campfire rule: leave the ratelimit in a good state
        try:
            #print("responde_headers = ", response_headers)
            rate_limit_remaining_requests = int(response_headers.get('x-ratelimit-remaining-requests', 0))
            print("rate_limit_remaining_requests = ", rate_limit_remaining_requests)

            if rate_limit_remaining_requests < 1:
                reset_time = int(response_headers.get('x-ratelimit-reset-requests', '0ms')[:-2])
                wait_time = reset_time - int(time.time() * 1000) if reset_time > int(time.time() * 1000) else 0
                print(f"Rate limit exceeded. Waiting for {wait_time / 1000} seconds.")
                
                if wait_time > 0: time.sleep(wait_time / 1000)
            #
        except Exception as e:
            print("Error handling rate limit: ", e)
            time.sleep(2)
        #

        response_json = None
        try:
            response_json = json.loads(response_text)
        except Exception as e:
            error = f"Failed to parse JSON response: {e}"
            print(error)
            logging.error(error)
        #

        try:
            usage = response_json['usage']
            print("response['usage'] = ", usage)
        except Exception as e:
            error += f"\nNo usage data: {e}"
            print(error)
            logging.error(error)
        #




        if False:
            print("response_text= ", response_text)
            print("response_json = ", response_json)
            print("response_json['choices'] = ", response_json['choices'])
            print("response_json['choices'][0] = ", response_json['choices'][0])  
            print("response_json['choices'][0]['message'] = ", response_json['choices'][0]['message'])
            print("response_json['choices'][0]['message']['content'] = ", response_json['choices'][0]['message']['content'])
            print("response_json['choices'][0]['message']['tool_calls'] = ", response_json['choices'][0]['message']['tool_calls'])
            print("response_json['choices'][0]['message']['tool_calls'][0] = ", response_json['choices'][0]['message']['tool_calls'][0])
            print("response_json['choices'][0]['message']['tool_calls'][0]['function'] = ", response_json['choices'][0]['message']['tool_calls'][0]['function'])
            print("response_json['choices'][0]['message']['tool_calls'][0]['function']['arguments'] = ", response_json['choices'][0]['message']['tool_calls'][0]['function']['arguments'])
            print("_----------------_________----------_______")              
        #        

        try:
            finish_reason = response_json['choices'][0]['finish_reason']
            print("finish_reason = ", finish_reason)
        except Exception as e:
            error += f"\nError extracting finish_reason from OpenAI response: {e}"
            print(error)
            logging.error(error)
        #

        if tools:
            try:
                tool_call_data = response_json['choices'][0]['message']['tool_calls'][0]['function']['arguments']
                print("finish_reason = ", finish_reason)
                #print("tool_call_data = ", tool_call_data)
            except Exception as e:
                error = f"Error extracting tool_call_data from OpenAI response {response_json}"
                logging.error(error)
            #
            
            try:  
                result = json.loads(tool_call_data)
                #print("data = ", data)
            except Exception as e:
                error = f"Error processing loading into json tool_call_data = {tool_call_data}"
                logging.error(error)
            #            
        else:
            try:
                result = response_json['choices'][0]['message']['content']
                #print("completed_answer = ", completed_answer)
            except (IndexError, KeyError) as e:
                error =  f"[tools = false] Error processing OpenAI response: {e} for response = {response_json}"
                logging.error(error)
            #
        #
    else:
        error = f"Failed to call API: {response.status_code} - {response.text}"
        logging.error(error)
    #
    result["finish_reason"]=finish_reason
    result["usage"]=usage
    
    return result, error
#

# we now need to use it both for regular chat completions and for chat completions with tools, and in a batch mode
def create_openai_chat(api_key, model, system_prompt, user_prompt, passed_schema):
    
    result = None
    error = None
    schema_dictionary = None
    tool = None
    tool_name = "json_answer"
    tool_description = "Generate output using the specified schema"

    if passed_schema:

        need_decoding = False
        try:
            print("--- naive try -->")
            schema_dictionary = json.loads(passed_schema)    
            if not schema_dictionary:
                need_decoding = True
            else:
                print("Did not need decoding")
                tool = {
                    "type": "function",
                    "function": {
                        "name": tool_name,
                        "description": tool_description,
                        "parameters": passed_schema
                    }
                }                
        except:
            print("Probably need to decode the string")
            need_decoding = True

        if need_decoding:
            schema_string = decode_schema_string(passed_schema)  

            print("------ decoded schema ---------")
            print(schema_string)
            print("-----------------------")        
            try:
                print("----->")
                schema_dictionary = json.loads(schema_string)
                print("schema_dictionary = ", schema_dictionary)
                print("<-----")
            except json.JSONDecodeError as e:
                error = f"Failed to parse schema JSON: {e}"
                #
        #

        
        # Convert JSON schema string to a dictionary


        print("------ schema_dictionary ---------")
        print(schema_dictionary)
        print("-----------------------")

        if schema_dictionary:        
            # Construct the tool with the schema
            tool = {
                "type": "function",
                "function": {
                    "name": tool_name,
                    "description": tool_description,
                    "parameters": schema_dictionary
                }
            }

            # Construct the messages for the chat
            messages = [
                {"role": "system", "content": system_prompt + "\nProduce your output as a JSON"},
                {"role": "user", "content": user_prompt}
            ]
        
            # Make the API call
            result, error = call_openai_api(api_key, model, messages, [tool])
        else:
            error = "No schema dictionary found"
        #
    else:
        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ]
        result, error = call_openai_api(api_key, model, messages)
    #
            
    print(result)
    print(error)            
    return result, error
#

def detect_missing_openai_inference_parameters(data):
    
    required_params = ["user_prompt", "api_key"]
    missing_params = [param for param in required_params if not data.get(param)]

    if missing_params:
        return jsonify({'error': f'Missing required parameters: {", ".join(missing_params)}'}), 400

    return None
#

def decode_schema_string(schema_string):
    # create a new array to store the parsed schema
    # go through the string character by character
    # if the character is a delimiter (either "{" "}" "[" "]" "," ":") then add it to the parsed array as is
    # if the character is not in that list, take note of the start index and keep going until you find the end index or the next delimiter
    # once you have the start and end index, extract the string and add it to the parsed array
    # however, if a fragment is between backticks ("`"), do not look for diminters between the backticks and remove the backticks from the final string
    
    # Now go through the parsed array and recreate the new string 'schema'
    # If the element is a string, add quotes around it and add it to the schema string
    # If the element is not a string, add it to the schema string as is
    # return schema
    
    parsed = []
    word = "" # a word is anyting that is between delimiters
    backtick_word = False
    
    delimiters = ['{', '}', '[', ']', ',', ':']
    
    length = len(schema_string) 
    for i in range(length):
        c = schema_string[i]
        
        if c == "`":
            if backtick_word:
                # end of a word between backticks. Note that the backticks themselves are discarded
                parsed.append(word)
                backtick_word = False
                word = ""
            else:
                if word == "":
                    # beginning of a word between backticks. Note that the backticks themselves are discarded
                    backtick_word = True
                else:
                    # mid sentence `, so we just add it to the word
                    word += c
                #
            #
        else:        
            if c in delimiters and backtick_word == False:
                # is it a closing delimiter?
                if word != "":
                    parsed.append(word)
                    word = ""
                #
                parsed.append(c)
            else:
                word += c
            #
    #
    if word != "":
        parsed.append(word)
    #

    schema = ""
    for p in parsed:
        if p in delimiters:
            schema += p
        else:
            word = p.strip()
            if word != "": schema += f'"{word}"'
        #
    #
    
    return schema    
#

def simple_inference(data):

    print("simple_inference data = ", data)
    
    result = None
    error = None
    
    ai_type = data.get('ai_type', 'openai')    
    if ai_type.lower() == 'openai':
        
        missing_parameters = detect_missing_openai_inference_parameters(data)
        if missing_parameters:
            error = "missing_parameters = ", missing_parameters
        #

        # required
        user_prompt = data['user_prompt']
        api_key = data['api_key']

        # optional        
        system_prompt = data.get('system_prompt','You are a useful assistant')
        model = data.get('model', 'gpt-3.5-turbo')
        simplified_schema = data.get('schema', None)

        result, error = create_openai_chat(api_key, model, system_prompt, user_prompt, simplified_schema)

        if result:
            print("result = ", result)
        else:
            error += "| No result received"
        #               
        
    else:
        error = f"Unsupported AI type: {data.get('ai_type')}"
    #
    
    print("result = ", result)
    print("error = ", error)
    return result, error
#

def sanitize_filename(name):
    """ Sanitize and create a safe filename """
    return re.sub(r'[^a-zA-Z0-9_\-]', '_', name)

def json_to_markdown_old(json_data):
    markdown_lines = []

    for item in json_data:
        level = item.get("level", 1)
        # convert level from string to integer
        level = int(level)
        title = item.get("title", "")
        elements = item.get("elements", [])

        # Add the title with appropriate heading level
        markdown_lines.append("#" * level + " " + title)

        for element in elements:
            if "text" in element:
                markdown_lines.append(element["text"])
            elif "bullet" in element:
                bullet_level = element.get("bullet_level", 1)
                # convert bullet_level from string to integer
                bullet_level = int(bullet_level)
                markdown_lines.append("  " * (bullet_level - 1) + "* " + element["bullet"])

    return "\n".join(markdown_lines)
#

def json_to_markdown(json_data):
    markdown = "\n"

    print("_________________")
    print("json_data = ", json.dumps(json_data, indent=4))
    print("_________________")
    
    previous_slide_type = ""
    for slide in json_data:
        if "introduction" in slide:
            title = slide["introduction"].get("title", "")
            
            # find if there is a "&" character in the title and replace it with †
            title = title.replace("&", "🫰")
            subtitle = slide["introduction"].get("subtitle", "")
            markdown += f"# {title}\n"
            if subtitle:
                markdown += f"{subtitle}\n"
            else:
                markdown += f"░░░░░░░░░░░░░░░░░░░░░░░░░\n"
            #
            previous_slide_type = "introduction"
        elif "section" in slide:
            title = slide["section"].get("title", "")
            title = title.replace("&", "🫰")
            subtitle = slide["section"].get("subtitle", "")
            markdown += f"## {title}\n"
            if subtitle:
                markdown += f"{subtitle}\n"
            else:
                markdown += f"░░░░░░░░░░░░░░░░░░░░░░░░░\n"
            #
            previous_slide_type = "section"
        elif "bullet_slide" in slide:
            title = slide["bullet_slide"].get("title", "")
            title = title.replace("&", "🫰")
            bullets = slide["bullet_slide"].get("bullets", [])
            markdown += f"### {title}\n"
            for bullet in bullets:
                text = bullet.get("text", "")
                bullet_level = int(bullet.get("bullet_level", "1"))
                # if bullet_level, prefix with one '*' character for each bullet level
                prefix = ""
                for _ in range(bullet_level):
                    prefix += "*" 
                #
                markdown += f"{prefix}{text}\n"
            #
            previous_slide_type = "bullet_slide"
        elif "card" in slide:
            title = slide["card"].get("title", "")
            title = title.replace("&", "🫰")
            if previous_slide_type != "bullet_slide" and previous_slide_type != "card":
                print("Adding a level 3 (bullet slide) as container for the card")
                markdown += f"### ░░░░░░░░░░░░░░░░░░░░░░░░░\n"
            #
            markdown += f"#### {title}\n"
            bullets = slide["card"].get("bullets", [])
            for bullet in bullets:
                text = bullet.get("text", "")
                bullet_level = int(bullet.get("bullet_level", "1"))
                # if bullet_level, prefix with one '*' character for each bullet level
                prefix = ""
                for _ in range(bullet_level):
                    prefix += "*" 
                #
                markdown += f"{prefix}{text}\n"
            #
            previous_slide_type = "card"
        #
        markdown += "\n"  # Add a blank line after each slide for separation
    #
    
    print("------ new mardkown -------")
    print(markdown)
    print("---------------------------")
    return markdown
#

def convert_markdown(markdown, output_filename):
    """
    Converts markdown content to another format using a specified script.
    
    :param processing_script: Path to the script that processes the markdown input.
    :param full_md: The content of the markdown that needs to be converted.
    :param download_filename: The filename for the output file.
    :return: Flask response object, either a file download or an error message.
    """
    #input_path = Path(tempfile.mkdtemp()) / 'input.md'
    input_path = Path(Path.cwd(), "temp", "markdown.md")    
    output_path = Path(Path.cwd(), "temp", f"{output_filename}.pptx")
    
    try:
        # Save the content to the input file
        with input_path.open('w') as input_file:
            input_file.write(markdown)
        #
        
        # Construct the command to run the script
        command = ['python', str(MD_PROCESSING_SCRIPT), str(input_path), str(output_path)]
        
        # Run the command
        result = subprocess.run(command, capture_output=True, text=True)
        
        # Check for errors
        if result.returncode != 0:
            return False, f"Error: {result.stderr}"
        
        # Send the output file back as a response
        if output_path.exists():
            return True, output_path
        else:
            #delete output_path file if it exists
            # if output_path.exists(): output_path.unlink()
            return False, "Output file was not created"
    finally:
        # Clean up the temporary input file
        try:
            #input_path.unlink()  # deletes the input file
            #input_path.parent.rmdir()  # deletes the temporary directory
            
            # if input_path.exists(): input_path.unlink()
            # if output_path.exists(): output_path.unlink()

            print("down with markdown convertion")
            pass
        
        except Exception as e:
            logging.error(f"Failed to clean up temporary files: {e}")
    #
#

# --------- APP ROUTES ----------------

@app.route('/')
def root_endpoint():
    return send_file('templates/index.html')

@app.route('/pptx/templates', methods=['GET'])
@app.route('/templates', methods=['GET'])
def get_templates_endpoint():
    config = GlobalConfig()
    templates = config.PPTX_TEMPLATE_FILES
    return jsonify([{name: template['caption']} for name, template in templates.items()])


@app.route('/pptx/generate_presentation', methods=['POST'])
@app.route('/generate_presentation', methods=['POST'])
def generate_presentation_endpoint():
    try:
        config = GlobalConfig()
        data = request.get_json()
        
        print("data = ", data)
        
        template_name = data.get('template', 'Blank')
        download_filename = data.get('filename', 'output.pptx')
        
        print("-------------------------")
        print("Using template:", template_name)
        print("Available templates:", config.PPTX_TEMPLATE_FILES)
        
        # Validate the template existence
        if template_name not in config.PPTX_TEMPLATE_FILES:
            return jsonify({"error": "Template not found: " + template_name}), 400
        
        # Exclude the template key from the data passed to generate the presentation
        if 'template' in data: del data['template']
        if 'filename' in data: del data['filename']

        try:
            generated_file = generate_presentation(json5.dumps(data), template_name)
            return send_file(
                io.BytesIO(generated_file),
                mimetype='application/vnd.openxmlformats-officedocument.presentationml.presentation',
                as_attachment=True,
                download_name=download_filename
            )
        except Exception as e:
            print("ERROR:", str(e))
            return jsonify({"error": str(e)}), 500
        
    except Exception as e:
        return jsonify({'error': f'Error during prediction processing: {str(e)}'}), 500
    #
    
    if prediction.status == "succeeded":
        response = requests.get(prediction.output, stream=True)
        content_disposition = f"attachment; filename={filename}"
        return Response(
            response.iter_content(chunk_size=1024),
            content_type = content_type,
            headers = {"Content-Disposition": content_disposition}
        )
    else:
        return jsonify({'error': f'Failed to generate resource, status: {prediction.status}'}), 500
    #
#

@app.route('/pptx/generate_presentation_advanced', methods=['POST'])
def generate_presentation_advanced_endpoint():
    try:
        config = GlobalConfig()
        data = request.get_json()
        
        template_name = data.get('template', 'Blank')
        download_filename = data.get('filename', 'output.pptx')
        
        print("-------------------------")
        print("Using template:", template_name)
        print("Available templates:", config.PPTX_TEMPLATE_FILES)
        
        # Validate the template existence
        if template_name not in config.PPTX_TEMPLATE_FILES:
            return jsonify({"error": "Template not found: " + template_name}), 400
        
        # Exclude the template key from the data passed to generate the presentation
        if 'template' in data: del data['template']
        if 'filename' in data: del data['filename']

        try:
            result_file_name = Path("temp", f"{uuid.uuid4().hex}.pptx")
            generated_file = generate_powerpoint_presentation_advanced(json5.dumps(data), template_name, result_file_name)
            return send_file(
                result_file_name,
                mimetype='application/vnd.openxmlformats-officedocument.presentationml.presentation',
                as_attachment=True,
                download_name=download_filename
            )
        except Exception as e:
            print("ERROR:", str(e))
            return jsonify({"error": str(e)}), 500
        
    except Exception as e:
        return jsonify({'error': f'Error during prediction processing: {str(e)}'}), 500
    #
    
    if prediction.status == "succeeded":
        response = requests.get(prediction.output, stream=True)
        content_disposition = f"attachment; filename={filename}"
        return Response(
            response.iter_content(chunk_size=1024),
            content_type = content_type,
            headers = {"Content-Disposition": content_disposition}
        )
    else:
        return jsonify({'error': f'Failed to generate resource, status: {prediction.status}'}), 500
    #
#

@app.route('/llm/infer', methods=['POST'])
def simple_inference_endpoint():
    print("simple_inference_endpoint")
    result = None
    error = None
    
    try: 
        data = request.json
    except Exception as e:
        error = f"Error getting JSON data from request {request}. Error = {e}"
    #

    print ("data = ", data)
    if data:
        try:
            result, error = simple_inference(data)
        except Exception as e:
            error = f"Error during inference processing: {e}"
        #
    else:
        error = f"No data found in request {request}"
    #

    print("result = ", result)
    print("error = ", error)

    if error:        
        return jsonify({'error': error}), 500
    else:
        return jsonify(result), 200    
    #    
#


def batch_infer(data):
    results = []
    errors = []
     
    #print("BATCH INFER data = ", data)
    
    if data.get('ai_type').lower() == 'openai':
        
        missing_parameters = detect_missing_openai_inference_parameters(data)
        if missing_parameters:
            return missing_parameters
        else:
            print("No missing parameters")
        #
    else:
        return jsonify({'error': f"Unsupported AI type: {data.get('ai_type')}"}), 400
    #
    
    # required
    user_prompts = data.get('user_prompt', '').split(separator)
    api_key = data.get('api_key')

    #optional    
    system_prompt = data.get('system_prompt', '')
    model = data.get('model', 'gpt-3.5-turbo')
    simplified_schema = data.get('schema', None)

    #schema_string = None
    #if simplified_schema: schema_string = decode_schema_string(simplified_schema)        
    
    index = 0
    total_number = len(user_prompts)
    for user_prompt in user_prompts:
        index += 1
        print(f"[{index}/{total_number}] user prompt = ", user_prompt)    
        result = None
        
        if simplified_schema:
            result, error = create_openai_chat(api_key, model, system_prompt, user_prompt, simplified_schema)
        else:
            messages = [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ]
            result, error = call_openai_api(api_key, model, messages)
        #
         
        if result:
            print(f"[{index}/{total_number}] - Done")
            results.append(result)
        else:
            print(f"[{index+1}/{total_number}] - Error")
            errors.append("No result " + separator)
        #               
        print("************************")
    #    
    
    
    return results, errors
#

@app.route('/llm/batch_infer', methods=['POST'])
def batch_inference_endpoint():
    data = request.json
    results, errors = batch_infer(data)
    return jsonify(result)
#

@app.route('/llm/batch_pptx', methods=['POST'])
def batch_pptx_endpoint():
    data = request.get_json()
    template_name = data.get('template', 'Blank')
    filename = data.get('filename', 'pptxs')
    inference_results, errors = batch_infer(data)
    # Container for generated files
    pptx_files = []
    file_names = set()

    
    for result in inference_results:
        json_data = json.dumps(result)
        generated_file = generate_presentation(json_data, template_name)
        sanitized_name = sanitize_filename(result.get('title', 'presentation'))
        count = 1
        unique_name = sanitized_name
        while unique_name in file_names:
            unique_name = f"{sanitized_name} ({count})"
            count += 1
        file_names.add(unique_name)

        # Save the file temporarily
        print(f"Saving file: {unique_name}.pptx")
        temp_path = Path(tempfile.mkstemp(suffix=".pptx", prefix=unique_name)[1])
        with open(temp_path, 'wb') as f:
            f.write(generated_file)
        #
        pptx_files.append(temp_path)
    #
    
    # Zip all the files
    file_count = len(inference_results)
    print(f"Zipping {file_count} files")
    
    zip_path = Path(tempfile.mkstemp(suffix=".zip", prefix=filename)[1])
    with zipfile.ZipFile(zip_path, 'w') as pptx_zip:
        for pptx_file in pptx_files:
            pptx_zip.write(pptx_file, arcname=os.path.basename(pptx_file))
            os.remove(pptx_file)  # Clean up the file after adding to zip
        #
    #

    print("*********** DONE *************")
    return send_file(zip_path, mimetype='application/zip', as_attachment=True, download_name=filename)
#

@app.route('/llm/big_pptx', methods=['POST'])
def big_pptx_endpoint():

    data = None
    print("BIG PPTX request")# = ", request)
    try:
        data = request.get_json()
    except Exception as e:
        print("Error getting JSON data: ", e)
        return jsonify({'error': 'Error getting JSON data'}), 500
    #
    #print("data = ", data)

    schema = BIG_PPTX_SCHEMA
    title = data.get('title', 'Presentation')
    subtitle = data.get('subtitle', '')
    filename = data.get('filename', 'default.pptx')    
    template_name = data.get('template', 'Blank')

    if not data.get('user_prompt'):
        return jsonify({'error': 'Missing user prompt'}), 400
    #
    
    subdata = {}
    subdata['ai_type'] = data.get('ai_type', 'openai')
    subdata['model'] = data.get('model', 'gpt-3.5-turbo')
    subdata['api_key'] = data.get('api_key', None)
    subdata['system_prompt'] = data.get('system_prompt', 'You are an helpful assistant')
    subdata['user_prompt'] = data.get('user_prompt', None)
    subdata['schema'] = schema
    
    #print("subdata = ", subdata)
    
    inference_results, errors = batch_infer(subdata)
    if inference_results:
        print("inference_results = ", inference_results)
                
        # Container for generated files
        pptx_files = []
        file_names = set()
        
        all_slides = []
        for result in inference_results:
            print("result = ", result)
            slides = result.get('slides', [])
            all_slides.extend(slides)
        #
        
        json_data = json.dumps({'title': title, 'subtitle': subtitle, 'slides': all_slides})

        try:    
            generated_file = generate_presentation(json_data, template_name)
        
            print("*********** DONE *************")
            return send_file(
                        io.BytesIO(generated_file),
                        mimetype='application/vnd.openxmlformats-officedocument.presentationml.presentation',
                        as_attachment=True,
                        download_name=filename
                    )
        except Exception as e:
            print("ERROR:", str(e))
            return jsonify({"error": str(e)}), 500
        #
    else:
        return jsonify({'error': f'No results found, errors = {errors}'}), 500
    #
#
       
       
def prepare_markdown(markdown, template, options):
    template_name = MD_TEMPLATE_PATH + template
    if "DeleteFirstSlide" not in options: options["DeleteFirstSlide"] = 'yes'    
    options_string = "\n".join([f"{key}: {value}" for key, value in options.items()])
    full_markdown = f"template: {template_name}\n{options_string}\n{markdown}"

    print("+++++++++++++++++++")
    print("Using template:", template_name)
    print("Using options: ", options)
    print("++++ markdown ++++")
    print(full_markdown)
    print("+++++++++++++++++++")

    return full_markdown
#
    
@app.route('/pptx/from_md', methods=['POST'])        
def md_to_pptx_endpoint():
    config = GlobalConfig()
    data = request.get_json()    
    download_filename = data.get('filename', 'output.pptx')

    if 'markdown' not in data: return jsonify({"error": "Invalid input, expected JSON with 'markdown' key"}), 400

    markdown = data.get('markdown')
    template = data.get('template', 'md_Urban_monochrome.pptx')
    options = data.get('options', {})
    result = md_to_pptx_handling(markdown, template, options, download_filename)
    return result
#
    
def md_to_pptx_handling(markdown, template, options, download_filename):
    
    full_markdown = prepare_markdown(markdown, template, options)
    
    success, content = convert_markdown(full_markdown, download_filename)
    if success == False:
        return jsonify({"error": content}), 500
    else:
        try:
            return send_file(content, as_attachment=True)
        finally:
            print("*********** DONE *************")
            #!!#if content.exists(): content.unlink()
        #
    #
#

@app.route('/llm/batch_text_to_dm', methods=['POST'])
def batch_text_to_dm_endpoint():

    data = None
    print("TEXT DM SLIDES")
    
    try:
        data = request.get_json()
    except Exception as e:
        print("Error getting JSON data: ", e)
        return jsonify({'error': 'Error getting JSON data'}), 500
    #
    if not data.get('user_prompt'): return jsonify({'error': 'Missing user prompt'}), 400
    download_filename = data.get('filename', 'default.pptx')    
    template = data.get('template', 'md_Urban_monochrome.pptx')
    options = data.get('options', {})
    format = data.get('format', 'pptx')    
    ai_type = data.get('ai_type', 'openai')
    model = data.get('model', 'gpt-3.5-turbo')
    api_key = data.get('api_key', None)
    system_prompt = data.get('system_prompt', f'You are an helpful assistant creating slides using a json schema.')
    user_prompt = data.get('user_prompt', None)
    markdown_only = data.get('markdown_only', False)
    result = batch_text_to_dm_handling(ai_type, model, api_key, system_prompt, user_prompt, download_filename)
    return result
#

def batch_text_to_dm_handling(ai_type, model, api_key, system_prompt, user_prompt, download_filename):    
    
    schema = BIG_DM_SLIDES_SCHEMA
    
    data = {}
    data['ai_type'] = ai_type
    data['model'] = model
    data['api_key'] = api_key
    data['system_prompt'] = system_prompt
    data['user_prompt'] = user_prompt
    data['schema'] = schema
    
    inference_results, errors = batch_infer(data)
    if not inference_results:
        return jsonify({'error': f'No results found, errors = {errors}'}), 500
    #
        
    print("inference_results = ", inference_results)
            
    # Container for generated files
    pptx_files = []
    file_names = set()
    
    all_slides = []
    for result in inference_results:
        print("result = ", result)
        slides = result.get('slides', [])
        all_slides.extend(slides)
    #        
    
    # Add the title and subtitle to the first slide as "slides": [{"level": 1, "title": "Presentation Title", "elements": [{"text": "Subtitle"}]}]
    # all_slides.insert(0, {""level": 1, ""title": title, "elements": [{"text": subtitle}]})        
    #json_data = json.dumps({'slides': all_slides})
    
    #convert json to markdown
    markdown = json_to_markdown(all_slides)
    
    temp_path = Path(Path.cwd(), "temp", f"{download_filename}.md")    
    
    print("saving to ", temp_path)
    with temp_path.open('w') as input_file:
        input_file.write(markdown)
    #
    # ensure the file is ready to be sent as a markdown file
    # set MIME type to markdown
    return send_file(temp_path)#, as_attachment=True)
#

@app.route('/llm/text_to_slides', methods=['POST'])
def text_to_slides_endpoint():

    data = None
    print("TEXT to SLIDES")
    
    try:
        data = request.get_json()
    except Exception as e:
        print("Error getting JSON data: ", e)
        return jsonify({'error': 'Error getting JSON data'}), 500
    #
    if not data.get('user_prompt'): return jsonify({'error': 'Missing user prompt'}), 400
    title = data.get('title', 'Presentation')
    subtitle = data.get('subtitle', '')
    download_filename = data.get('filename', 'default.pptx')    
    template = data.get('template', 'md_Urban_monochrome.pptx')
    options = data.get('options', {})
    format = data.get('format', 'pptx')    
    ai_type = data.get('ai_type', 'openai')
    model = data.get('model', 'gpt-3.5-turbo')
    api_key = data.get('api_key', None)
    system_prompt = data.get('system_prompt', f'You are an helpful assistant creating slides using a json schema.')
    user_prompt = data.get('user_prompt', None)
    
    temp_file_id = uuid.uuid4().hex
    temp_file = Path(Path.cwd(), "temp", f"{temp_file_id}.md")
    print("Saving temp to : ", temp_file)
    result = batch_text_to_dm_handling(ai_type, model, api_key, system_prompt, user_prompt, temp_file_id)

    markdown = ""
    try:
        with open(temp_file, 'r') as f:
            markdown = f.read()
    except FileNotFoundError:
        print(f"File {output_path} not found")
        exit(1)
    #
    
    result = md_to_pptx_handling(markdown, template, options, download_filename)
    return result
#

# Function to convert result to the specified schema
def convert_to_presentation_json(remedial_result):
    slides = []

    # check that resources as a gap field
    if 'remedial_resources' not in remedial_result:
        e = f"Error: No remedial resources found in the response, remedial_result = {remedial_result}"
        return None
    #    
    



    for resource in remedial_result['remedial_resources']:
        if 'gap' not in resource: resource['gap']= ''

        gap = resource['gap']
        gap_category = resource['gap_category']
        remedial = resource['remedial']
        sources = resource['sources']
        reasonings = resource['reasonings']

        print("gap = ", gap)
        print("gap_category = ", gap_category)
        print("remedial = ", remedial)
        print("sources = ", sources)
        print("reasonings = ", reasonings)


        slide = {
            "heading": gap,
            "bullet_points": [
                {
                    "bullet_type": "bullet",
                    "bullet_level": "0",
                    "bullet_text": f"Category: {gap_category}"
                },
                {
                    "bullet_type": "bullet",
                    "bullet_level": "0",
                    "bullet_text": f"Remedial Action: {remedial}"
                },
                {
                    "bullet_type": "bullet",
                    "bullet_level": "0",
                    "bullet_text": "SOURCES"  
                }
            ]
        }
        
        for url in sources:
            print("url =", url)
            slide['bullet_points'].append({
                "bullet_type": "bullet",
                "bullet_level": "1",
                "bullet_text": url
            })
        
        for reasoning in reasonings:
            print("reasoning =", reasoning)
            slide['bullet_points'].append({
                "bullet_type": "bullet",
                "bullet_level": "0",
                "bullet_text": f"Reasoning: {reasoning}"
            })
        
        print("-----------------")
        print("slide = ", slide)
        slides.append(slide)
    #
    print("------------------")
    print("Slides = ", slides)
    return {"slides": slides}
#

@app.route('/llm/remedial_resources', methods=['POST'])
def remedial_resources_endpoint():
    from schemas import REMEDIAL_SCHEMA, REMEDIAL_SYSTEM_PROMPT, REMEDIAL_REFERENCES
    data = None
    print("remedial_resources starting")
    
    try:
        data = request.get_json()
        print(data)
    except Exception as e:
        print("Error getting JSON data: ", e)
        return jsonify({'error': 'Error getting JSON data'}), 500
    #

    gaps = data.get('gaps', None)
    print("gaps", gaps)
    if not gaps: return jsonify({'error': 'Missing gaps'}), 400
    
    references = data.get('references', REMEDIAL_REFERENCES)
    print("references = ", len(references))
    ref_data = None
    ref_list = None
    ref_url_dict = None
    try:
        ref_data = json.loads(references)
        # Extract all the 'ref' values into an array
        ref_list = [resource["ref"] for resource in ref_data["resources"]]
        # Create the dictionary with 'ref' as keys and 'url' as values
        ref_url_dict = {resource["ref"]: resource["url"] for resource in ref_data["resources"]}
    except Exception as e:
        return jsonify({'error': 'Error parsing references'}), 400
    #
    #print("ref_data = ", ref_data)
    #print("ref_list = ", ref_list)
    #print("ref_url_dict = ", ref_url_dict)
    if not ref_data or not  ref_list or not ref_url_dict: return jsonify({'error': 'Could not obtain references data'}), 400
    print("Ref_data acquired")

    remedial_schema_dict = None
    try:
        remedial_schema_dict = json.loads(REMEDIAL_SCHEMA)
        remedial_schema_dict["properties"]["remedial_resources"]["items"]["properties"]["sources"]["items"]["enum"] = ref_list
        #print(remedial_schema)
    except Exception as e:
        error = f'Error parsing remedial schema, e={e}'
        print("ERROR: ",error)
        return jsonify({'error': error}), 400
    #

    # convert dictionary into a string
    
    remedial_schema = json.dumps(remedial_schema_dict)
    print("--")
    if not remedial_schema_dict: return jsonify({'error': 'Could not obtain remedial schema'}), 400
    print("--+")
    #print("remedial_schema = " , remedial_schema)
    print("Remedial schema generated")
    system_prompt = data.get('system_prompt', REMEDIAL_SYSTEM_PROMPT)
    system_prompt += "<REFERENCES>\n"+references+"\n</REFERENCES>\n\n"
    user_prompt = "<KNOWLEDGE_GAP>\n"+gaps+"\n</KNOWLEDGE_GAP>\n\n"
    api_key = data.get('api_key', None)
    if not api_key: return jsonify({'error': 'Missing API key'}), 400
    model = data.get('model', 'gpt-4o')#gpt-3.5-turbo')
    print("Ready to call create_openai_chat")
    remedial_result = None
    error = None
    try:
        remedial_result, error = create_openai_chat(api_key, model, system_prompt, user_prompt, remedial_schema)
    except Exception as e:
       ee = f'error when calling create_openai_chat(api_key={api_key}, model={model}, remedial_schema={remedial_schema_dict}, system_prompt={system_prompt}, user_prompt={user_prompt}), error={error}, e={e}'
       return jsonify({'error':ee}), 500
    #
    usage = remedial_result["usage"]
    print("Usage = ", usage)
    finish_reason = remedial_result["finish_reason"]
    print("finish_reason = ", finish_reason)

    print("-------")

    if not remedial_result: return jsonify({f'error when calling create_openai_chat(api_key={api_key}, model={model}, remedial_schema={remedial_schema_dict}, system_prompt={system_prompt}, user_prompt={user_prompt}), error=' : error}), 500

    if not remedial_result['remedial_resources']: 
        ee = f'No remedial resources in openai response found: response = {result}, error = {error}'
        print(ee)
        return jsonify({'error': ee}), 400
    #

    # Process each item in 'remedial_resources'
    for resource in remedial_result['remedial_resources']:
        # Extract the list of references
        references = resource['sources']
        
        # Validate and filter references
        valid_references = []
        for ref in references:
            if ref in ref_url_dict:
                valid_references.append(ref_url_dict[ref])
            else:
                print(f"Warning: Reference {ref} not found in the dictionary.")
            #
        #

        
        # Replace the references with URLs
        resource['sources'] = valid_references
    #

    print("remedial_result = ", remedial_result)
    # Now, we will make a presentation-compatible json using those gathered information
    slides = None
    try:
        slides = convert_to_presentation_json(remedial_result)
    except Exception as e:
        ee = f"Error converting to presentation json with passed arg: remedial_result = {remedial_result}, error = {e}"
        print(ee)
        return jsonify({'error': ee}), 500
    #

    if not slides:
        ee = f"Error converting to presentation json returned None result, passed arg: remedial_result was = {remedial_result}, error = {e}"
        print(ee)
        return jsonify({'error': ee}), 500
    
    print("Slides = ", slides)
    return slides
#



if __name__ == '__main__':
    # Example usage
    config = GlobalConfig()
    #print("log level = ", GlobalConfig.LOG_LEVEL)
    app.run(host='0.0.0.0', port=8501, debug=True)
