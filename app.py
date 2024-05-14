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
from pptx_helper import generate_powerpoint_presentation
from global_config import GlobalConfig
import io
import json
import replicate
import re
import zipfile

separator = '|||'
OBSCURE_CHARACTER = 'ˆ'

app = Flask(__name__, static_folder='static')

def generate_presentation(slides: str, template_name: str = 'Blank') -> bytes:
    output_file_path = Path(tempfile.mkstemp(suffix=".pptx")[1])
    generate_powerpoint_presentation(slides, output_file_path=output_file_path, slides_template=template_name)
    print("-------------------------")
    print("Powerpoint generated using template:", template_name)
    with open(output_file_path, "rb") as f:
        return f.read()

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

        except json.JSONDecodeError as e:
            error = f"Failed to parse JSON response: {e} , for response_json = {response_json}"
            logging.error(error)
        #
        
        if tools:
            try:
                tool_call_data = response_json['choices'][0]['message']['tool_calls'][0]['function']['arguments']
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
    
    return result, error
#

# we now need to use it both for regular chat completions and for chat completions with tools, and in a batch mode
def create_openai_chat(api_key, model, system_prompt, user_prompt, simplified_schema):
    
    result = None
    error = None
    
    if simplified_schema:
        schema_string = decode_schema_string(simplified_schema)        
        
        tool_name = "json_answer"
        tool_description = "Generate output using the specified schema"
        
        # Convert JSON schema string to a dictionary
        schema_dictionary = None
        try:
            schema_dictionary = json.loads(schema_string)
        except json.JSONDecodeError as e:
            error = f"Failed to parse schema JSON: {e}"
        #

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
            result = call_openai_api(api_key, model, messages, [tool])
        else:
            error = "No schema dictionary found"
        #
    else:
        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ]
        result = call_openai_api(api_key, model, messages)
    #
            
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
    # Step 1: Replace spaces within backticks with a rare character and remove the backticks
    schema_string = re.sub(r'`([^`]*)`', lambda match: match.group(1).replace(' ', OBSCURE_CHARACTER), schema_string)

    # Step 2: Split the string using regex to match sequences of word characters or non-word characters
    split_list = re.findall(r'\w+|\W+', schema_string)

    # Step 3: Reconstitute the string, adding quotes around words
    schema = ''.join(f'"{part}"' if re.match(r'^[a-zA-Z_]\w*$', part) else part for part in split_list)

    # Step 4: Replace the rare character back with spaces
    schema = schema.replace(OBSCURE_CHARACTER, ' ')
    return schema


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

    schema_string = None
    if simplified_schema: schema_string = decode_schema_string(simplified_schema)        
    
    index = 0
    total_number = len(user_prompts)
    for user_prompt in user_prompts:
        index += 1
        print(f"[{index}/{total_number}] user prompt = ", user_prompt)    
        result = None
        
        if schema_string:
            result = create_openai_chat(api_key, model, system_prompt, user_prompt, schema_string)
        else:
            messages = [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ]
            result = call_openai_api(api_key, model, messages)
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
    
    
    return {'results': results, 'errors': errors}
#

@app.route('/llm/batch_infer', methods=['POST'])
def batch_inference_endpoint():
    data = request.json
    result = batch_infer(data)
    return jsonify(result)
#

@app.route('/llm/batch_pptx', methods=['POST'])
def batch_pptx_endpoint():
    data = request.get_json()
    template_name = data.get('template', 'Blank')
    filename = data.get('filename', 'pptxs')
    inference_result = batch_infer(data)
    inference_results = inference_result.get('results', [])
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

    schema = "{type:object,properties:{slides:{type:array,items:{type:object,properties:{heading:{title:Heading,description:The_slide_Heading,type:string},bullet_points:{title:Bullet_Points,description:The_bullet_points,type:array,items:{type:string}}},required:[heading,bullet_points]}}},required:[slides]}"
    
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
    
    inference_result = batch_infer(subdata)
    print("inference_result = ", inference_result)
            
    inference_results = inference_result.get('results', [])
    # Container for generated files
    pptx_files = []
    file_names = set()
    
    all_slides = []
    for result in inference_results:
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
#
        
def sanitize_filename(name):
    """ Sanitize and create a safe filename """
    return re.sub(r'[^a-zA-Z0-9_\-]', '_', name)


if __name__ == '__main__':
    # Example usage
    config = GlobalConfig()
    #print("log level = ", GlobalConfig.LOG_LEVEL)
    app.run(host='0.0.0.0', port=8501, debug=True)
