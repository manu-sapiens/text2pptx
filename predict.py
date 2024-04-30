print("-------- START -----------")

from flask import Flask, request, send_file, jsonify
import json5
from pathlib import Path
import tempfile
from pptx_helper import generate_powerpoint_presentation
from PIL import Image
import base64
import io
from global_config import GlobalConfig

app = Flask(__name__)

def generate_presentation(slides: str, template_name: str = 'Blank') -> bytes:
    output_file_path = Path(tempfile.mkstemp(suffix=".pptx")[1])
    generate_powerpoint_presentation(slides, output_file_path=output_file_path, slides_template=template_name)
    print("-------------------------")
    print("Powerpoint generated using template:", template_name)
    with open(output_file_path, "rb") as f:
        return f.read()

@app.route('/templates', methods=['GET'])
def list_templates():
    templates = GlobalConfig.PPTX_TEMPLATE_FILES
    return jsonify([{name : template['caption']} for name, template in templates.items()])
    #return GlobalConfig.PPTX_TEMPLATE_FILES

@app.route('/generate_presentation', methods=['POST'])
def generate_presentation_endpoint():
    data = request.get_json()  # Use get_json() to parse the incoming JSON payload directly
    
    slides_json = json5.dumps(data)  # Re-encode the data to JSON for internal handling, if necessary
    template_name = data.get('template', 'Blank')  # Default to 'Blank' if no template is provided
    
    print("-------------------------")
    print("Using template:", template_name)
    print("Available templates:", GlobalConfig.PPTX_TEMPLATE_FILES)
    
    # Validate the input JSON and the existence of the template
    try:
        if template_name not in GlobalConfig.PPTX_TEMPLATE_FILES:
            raise ValueError("Template not found: " + template_name)
    except Exception as e:
        print("ERROR:", str(e))
        return {"error": str(e)}, 400  # Return the error with a Bad Request status code

    # Exclude the template key from the data passed to generate the presentation
    if 'template' in data:
        del data['template']

    generated_file = generate_presentation(json5.dumps(data), template_name)
    return send_file(
        io.BytesIO(generated_file),
        mimetype='application/vnd.openxmlformats-officedocument.presentationml.presentation',
        as_attachment=True,
        download_name='output.pptx'
    )


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8501)