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

app = Flask(__name__, static_folder='static')

def generate_presentation(slides: str, template_name: str = 'Blank') -> bytes:
    output_file_path = Path(tempfile.mkstemp(suffix=".pptx")[1])
    generate_powerpoint_presentation(slides, output_file_path=output_file_path, slides_template=template_name)
    print("-------------------------")
    print("Powerpoint generated using template:", template_name)
    with open(output_file_path, "rb") as f:
        return f.read()

@app.route('/')
def index():
    return send_file('templates/index.html')

@app.route('/pptx/templates', methods=['GET'])
@app.route('/templates', methods=['GET'])
def list_templates():
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
    
    print("************************")
    print("api_key = ", api_key)
    print("model= ", model)    
    print("messages = ", messages)
    print("tools = ", tools)
    print("************************")
    
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
            return jsonify({'error': f"Error accessing response data for response = {response}"}), 500
        #
        
        # campfire rule: leave the ratelimit in a good state
        try:
            rate_limit_remaining = int(response_headers.get('Openai-Ratelimit-Remaining', 0))
            if rate_limit_remaining < 1:
                reset_time = int(response_headers.get('Openai-Ratelimit-Reset', 0))
                wait_time = reset_time - time.time() if reset_time > time.time() else 0
                print(f"Rate limit exceeded. Waiting for {wait_time} seconds.")
                time.sleep(wait_time)
            #
        except Exception as e:
            print("Error handling rate limit: ", e)
            time.sleep(2)
        #

        response_json = None
        try:
            response_json = json.loads(response_text)
            
            if True:
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
            logging.error(f"JSON decode error: {e}")
            return {"error": f"Failed to parse JSON response: {e} , for response_json = {response_json}"}, 500
        #
        
        if tools:
            try:
                tool_call_data = response_json['choices'][0]['message']['tool_calls'][0]['function']['arguments']
                print("tool_call_data = ", tool_call_data)
            except Exception as e:
                logging.error(f"[tools = true] Error accessing tool call data: {e} for response = {response_json}")
                return jsonify({'error': 'Error processing OpenAI response'}), 500
            #
            
            try:  
                data = json.loads(tool_call_data)
                print("data = ", data)
            except Exception as e:
                logging.error(f"[tools = true] Error accessing tool call data: {e} for response = {response_json}")
                return jsonify({'error': 'Error processing OpenAI response'}), 500
            #
            
            return data
        else:
            try:
                completed_answer = rresponse_json['choices'][0]['message']['content']
                print("completed_answer = ", completed_answer)
            except (IndexError, KeyError) as e:
                logging.error(f"[tools = false] Error processing OpenAI response: {e} for response = {response_json}")
                return jsonify({'error': 'Error processing OpenAI response'}), 500
            #
            return completed_answer
        #
    else:
        raise Exception(f"Failed to call API: {response.status_code} - {response.text}")
    #
#

# we now need to use it both for regular chat completions and for chat completions with tools, and in a batch mode
def create_openai_chat_with_tool(api_key, model, system_prompt, user_prompt, schema_string):
    
    tool_name = "json_answer"
    tool_description = "Generate output using the specified schema"
    
    # Convert JSON schema string to a dictionary
    try:
        schema_dictionary = json.loads(schema_string)
    except json.JSONDecodeError as e:
        logging.error(f"JSON decode error: {e}")
        return {"error": f"Failed to parse schema JSON: {e}"}, 400
    #
    
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
    return result
#

def detect_missing_openai_inference_parameters(data):
    required_params = ["model", "system_prompt", "user_prompt", "api_key"]
    missing_params = [param for param in required_params if not data.get(param)]

    if missing_params:
        return jsonify({'error': f'Missing required parameters: {", ".join(missing_params)}'}), 400

    return None
#

def decode_schema_string(schema_string):
    schema = None
    # Convert the simplified schema string to a valid JSON schema
    # schema = schema_str.replace("~", "\"")  # Replace placeholder with actual quotes

    # Split the string using regex to match sequences of word characters or non-word characters
    split_list = re.findall(r'\w+|\W+', schema_string)

    # Reconstitute the string, adding quotes around words
    schema = ''.join(f'"{part}"' if re.match(r'^[a-zA-Z_]\w*$', part) else part for part in split_list)
 
    print("schema = ", schema)
    return schema
#

@app.route('/llm/infer', methods=['POST'])
def handle_post():
    data = request.json

    if data.get('ai_type').lower() == 'openai':
        
        missing_parameters = detect_missing_openai_inference_parameters(data)
        if missing_parameters:
            return missing_parameters
        #
        
        system_prompt = data['system_prompt'] 
        user_prompt = data['user_prompt']
        model = data['model']
        api_key = data['api_key']
        schema = data.get('schema')

        print("************************")        
        print("schema = ", schema)
        print("model= ", model)
        print("system_prompt = ", system_prompt)
        print("user_prompt = ", user_prompt)
        print("api_key = ", api_key)
        print("************************")
              
        #openai_client = OpenAI(api_key=api_key)
        
        if schema:
            schema = decode_schema_string(schema)            
            response = create_openai_chat_with_tool(api_key, model, system_prompt, user_prompt, schema)
            
            if response:
                print("-------------------")
                print("response = ", response)
                try:
                    # Assuming the function call arguments contain the data as a JSON string
                    tool_call_data = response.choices[0].message.tool_calls[0].function.arguments

                    print("************************")
                    print("tool_call_data = ", tool_call_data)
                    print("************************")
                    # If tool_call_data is a string, convert it to a dictionary
                    data = json.loads(tool_call_data)
                    return jsonify(data)
                except Exception as e:
                    logging.error(f"Error accessing tool call data: {e}, Full response: {response}")
                    return jsonify({'error': 'Error processing OpenAI response'}), 500
            else:
                return jsonify({'error': 'Failed to get response from OpenAI'}), 500
            
        else:
            messages = [
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ]
                         
            result = call_openai_api(api_key, model, messages)
            
            if result:
                return jsonify(result), 200
            else:
                return jsonify({'error': 'Failed to get response from OpenAI'}), 500
            #
        #
    else:
        return jsonify({'error': f"Unsupported AI type: {data.get('ai_type')}"}), 400
    #
#


def batch_infer(data):
    results = []
    errors = []
     
    print("BATCH INFER data = ", data)
    
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
    
    system_prompt = data.get('system_prompt', '')
    user_prompts = data.get('user_prompt', '').split(separator)
    api_key = data.get('api_key')
    model = data.get('model')
    simplified_schema = data.get('schema', None)

    schema_string = None
    if simplified_schema: schema_string = decode_schema_string(simplified_schema)        
    
    for user_prompt in user_prompts:
        
        result = None
        
        if schema_string:
            result = create_openai_chat_with_tool(api_key, model, system_prompt, user_prompt, schema_string)
        else:
            messages = [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ]
            result = call_openai_api(api_key, model, messages)
        #
         
        if result:
            results.append(result)
            errors.append(None)
        else:
            results.append(None)
            errors.append("No result " + separator)
        #               
    #    
    
    return {'results': results, 'errors': errors}
#

@app.route('/llm/batch_infer', methods=['POST'])
def handle_batch_post():
    data = request.json
    result = batch_infer(data)
    return jsonify(result)
#

@app.route('/llm/batch_pptx', methods=['POST'])
def combined_batch_pptx():
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

def sanitize_filename(name):
    """ Sanitize and create a safe filename """
    return re.sub(r'[^a-zA-Z0-9_\-]', '_', name)


if __name__ == '__main__':
    # Example usage
    config = GlobalConfig()
    #print("log level = ", GlobalConfig.LOG_LEVEL)
    app.run(host='0.0.0.0', port=8501, debug=True)
