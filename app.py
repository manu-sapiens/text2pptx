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
from openai import OpenAI
import json
import replicate

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

def create_openai_chat_with_tool(client, system_prompt, user_prompt, model, schema_string, tool_name, tool_description):
    # Convert JSON schema string to a dictionary
    try:
        schema = json.loads(schema_string)
    except json.JSONDecodeError as e:
        logging.error(f"JSON decode error: {e}")
        return {"error": f"Failed to parse schema JSON: {e}"}, 400
    
    # Construct the tool with the schema
    tool = {
        "type": "function",
        "function": {
            "name": tool_name,
            "description": tool_description,
            "parameters": schema
        }
    }

    # Construct the messages for the chat
    messages = [
        {"role": "system", "content": system_prompt + "\nProduce your output as a JSON"},
        {"role": "user", "content": user_prompt}
    ]
    
    # Make the API call
    response = client.chat.completions.create(
        model=model,
        messages=messages,
        tools=[tool],
        tool_choice="required"
    )
    return response

@app.route('/llm/infer', methods=['POST'])
def handle_post():
    data = request.json

    if data.get('ai_type').lower() == 'openai':
        required_params = ["model", "system_prompt", "user_prompt", "api_key"]
        missing_params = [param for param in required_params if not data.get(param)]

        if missing_params:
            return jsonify({'error': f'Missing required parameters: {", ".join(missing_params)}'}), 400                

        system_prompt = data['system_prompt'] 
        user_prompt = data['user_prompt']
        model = data['model']
        
        schema_str = data.get('schema')
        openai_client = OpenAI(api_key=data['api_key'])
        
        if schema_str:
            schema = None
            try:
                # Convert the simplified schema string to a valid JSON schema
                print("-------------------")
                print("schema_str = ", schema_str)
                schema = schema_str.replace("~", "\"")  # Replace placeholder with actual quotes
                print("schema = ", schema)
                print("-------------------")

                # Now you can use 'schema' as a proper JSON Schema            
                
            except json.JSONDecodeError as e:
                logging.error(f"JSON decode error: {e}")
                return jsonify({"error": f"Failed to parse schema JSON: {e}"}), 400
            #
            
            response = create_openai_chat_with_tool(openai_client, system_prompt, user_prompt, model, schema, "json_answer", "Generate output using the specified schema")
            
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
            response = openai_client.ChatCompletion.create(
                model=data['model'],
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                response_format={"type": "json_object"}
            )
        
            if response:
                print("-------------------")
                print("response = ", response)
                print("response.choices = ", response.choices)
                print("response.choices[0] = ", response.choices[0])
                print("response.choices[0].message = ", response.choices[0].message)
                print("response.choices[0].message.content = ", response.choices[0].message.content)
                print("-------------------")
                try:
                    completed_answer = response['choices'][0]['message']['content']
                    return jsonify({'completed_answer': completed_answer})
                except (IndexError, KeyError) as e:
                    logging.error(f"Error processing OpenAI response: {e}")
                    return jsonify({'error': 'Error processing OpenAI response'}), 500
            else:
                return jsonify({'error': 'Failed to get response from OpenAI'}), 500
            #
        #
    else:
        return jsonify({'error': f"Unsupported AI type: {data.get('ai_type')}"}), 400
    #
#

if __name__ == '__main__':
    # Example usage
    config = GlobalConfig()
    print("log level = ", GlobalConfig.LOG_LEVEL)
    
    app.run(host='0.0.0.0', port=8501, debug=True)
