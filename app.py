print("-------- START -----------")

from flask import Flask, request, send_file, jsonify
import json5
from pathlib import Path
import tempfile
from pptx_helper import generate_powerpoint_presentation
from global_config import GlobalConfig
import io

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

@app.route('/templates', methods=['GET'])
def list_templates():
    config = GlobalConfig()
    templates = config.PPTX_TEMPLATE_FILES
    return jsonify([{name: template['caption']} for name, template in templates.items()])

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
        print("ERROR:", str(e))
        # send back a error.txt plain text file containing the error message
        # and a status of 400
        error_txt = "MANU WAS THERE, error = " + str(e)
        generated_file = error_txt.encode('utf-8')
        return send_file(
            io.BytesIO(generated_file),
            mimetype='', # just plain text file
            as_attachment=True,
            download_name="error.txt"), 400

if __name__ == '__main__':
    # Example usage
    config = GlobalConfig()
    templates = config.PPTX_TEMPLATE_FILES
    print("log level = ", GlobalConfig.LOG_LEVEL)
    print("templates = ", templates)
    
    app.run(host='0.0.0.0', port=8501)
