from flask_cors import CORS, cross_origin #Add cross region support
import os
from flask import Flask, request, jsonify, send_from_directory, render_template, make_response
from werkzeug.utils import secure_filename
from werkzeug.middleware.proxy_fix import ProxyFix
import subprocess
from subprocess import Popen, PIPE, STDOUT
from celery import Celery
from celery.utils.log import get_task_logger
import logging
from logging.config import dictConfig
import pexpect
import re
import threading
import time
dictConfig({
    'version': 1,
    'formatters': {'default': {'format': '[%(asctime)s] %(levelname)s in %(module)s: %(message)s',}},
    'handlers': {'wsgi': {'class': 'logging.StreamHandler', 'formatter': 'default',}},
    'root': {'level': 'INFO', 'handlers': ['wsgi']}
})

def configure_logging():
    logging.basicConfig(filename='app.log', level=logging.INFO, format='[%(asctime)s] %(levelname)s in %(module)s: %(message)s')

# Call the logging configuration function before running the Flask app
configure_logging()


app = Flask(__name__)
app.wsgi_app = ProxyFix(app.wsgi_app, x_for=1, x_proto=1, x_host=1, x_port=1, x_prefix=1)

app.config['MAX_CONTENT_LENGTH'] = 500 * 1024 * 1024  # Limit of 16 MB, adjust as needed
app.config['CELERY_BROKER_URL'] = 'redis://localhost:6379/0'
app.config['CELERY_RESULT_BACKEND'] = 'redis://localhost:6379/0'
def make_celery(app):
    celery = Celery(app.name, broker=app.config['CELERY_BROKER_URL'])
    celery.conf.update(app.config)
    return celery
celery = make_celery(app)
CORS(app)

upload_folder = '/home/lab212/upload'  
app.config['UPLOAD_FOLDER'] = upload_folder
os.makedirs(upload_folder, exist_ok=True)  

@app.route('/home/lab212/upload/<path:subpath>', methods=['GET'])
def get_file_or_folder(subpath):
    full_path = os.path.join(app.config['UPLOAD_FOLDER'], subpath)
    
    if os.path.isdir(full_path):
        # It's a directory, list contents
        contents = []
        for item in os.listdir(full_path):
            item_full_path = os.path.join(full_path, item)
            if os.path.isdir(item_full_path):
                contents.append({'name': item, 'type': 'folder', 'url': f'/home/lab212/upload/{subpath}/{item}'})
            else:
                contents.append({'name': item, 'type': 'file', 'url': f'/home/lab212/upload/{subpath}/{item}'})
        
        return jsonify(contents)
    elif os.path.isfile(full_path):
        # It's a file, send the file
        return send_from_directory(os.path.dirname(full_path), os.path.basename(full_path))
    else:
        return jsonify({"error": "Item does not exist"}), 404


@app.route('/home/lab212/upload', methods=['POST', 'GET'])
def handle_request():
    if request.method == 'POST':
        if 'file' in request.files:
            file = request.files['file']
            filename = secure_filename(file.filename)
            upload_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(upload_path)
            print(f'Received file: {filename}')
            return jsonify({"message": f"File {filename} uploaded successfully."}), 200
        else:
            return jsonify({"error": "No file part"}), 400

    elif request.method == 'GET':
        files = os.listdir(app.config['UPLOAD_FOLDER'])
        return jsonify(files)

    return render_template('index.htm')

@app.route('/upload', methods=['POST'])
def handle_upload():
    root_folder_name = request.form['rootFolderName']  # Get the root folder name from the form data
    #root_folder_path = os.path.join(upload_folder, root_folder_name)
    #os.makedirs(root_folder_path, exist_ok=True)

    files = request.files.getlist('files')
    if not files:
        return jsonify({"error": "No files were uploaded"}), 400

    for file in files:
        filename = file.filename  # Getting the path from the frontend
        safe_path = os.path.join(upload_folder, filename)  # Save inside the new root folder
        directory = os.path.dirname(safe_path)
        os.makedirs(directory, exist_ok=True)
        file.save(safe_path)
        #print(f'Received file: {safe_path}')
    print(f"Folder '{root_folder_name}' and its files uploaded successfully")
    return jsonify({"message": f"Folder '{root_folder_name}' and its files uploaded successfully"}), 200

logger = get_task_logger(__name__)
@app.route('/run_deep', methods=['POST'])
def run_deep():
    logger.info("Starting 2D quantify & visualize")
    try:
        commands = [
            '/home/lab212/anaconda3/bin/activate py3_torch && cd /home/lab212/www/mmdet/demo && python contact_test_panoptic_sw_vis.py'
        ]
        for cmd in commands:
            subprocess.run(cmd, shell=True, check=True)
        
        return jsonify({'message': 'Process completed successfully', 'status': 'success'}), 200
    except subprocess.CalledProcessError as e:
        return jsonify({'message': str(e), 'status': 'error'}), 500

@app.route('/get_deep', methods=['GET'])
def get_deep():
    files = os.listdir('/home/lab212/www/mmdet/results')
    return jsonify(files)

@app.route('/get_deep/<filename>', methods=['GET'])
def download_file(filename):
    return send_from_directory('/home/lab212/www/mmdet/results', filename)

# Global variable to store the link
reconstruction_result = None
logger = get_task_logger(__name__)
@app.route('/run_test', methods=['POST'])
def run_test():
    global reconstruction_result
    logger.info("Starting 3D reconstruction task")
    directory = "/home/lab212/pytorch_connectomics/3Dreconstruction"


    try:
        child = pexpect.spawn('bash', timeout=600)
        child.sendline('conda activate py3_torch')
        child.sendline(f'cd {directory}')
        child.sendline('python -i test.py') 
        time.sleep(3)
        logger.info(f"Task completed successfully!")
        return jsonify({"message": "Reconstruction started"}), 200  # Include link in response
    except Exception as e:
        logger.error(f"Task failed with error: {str(e)}", exc_info=True)
        return jsonify({"error": str(e)}), 500


@app.route('/get_result', methods=['GET'])
def get_result():
    link_file_path = os.path.join("/home/lab212/pytorch_connectomics/3Dreconstruction", 'link.txt')
    if os.path.exists(link_file_path):
        with open(link_file_path, 'r') as file:
            reconstruction_result = file.read().strip()
            logger.info(f"Generated link: {reconstruction_result}")
    else:
        logger.error("link.txt file not found.")
        reconstruction_result = None
    if reconstruction_result:
        return jsonify({"link": reconstruction_result}), 200
    else:
        return jsonify({"error": "Result not available yet"}), 202

# Directory where CSV files are stored
CSV_FILES_DIR = '/home/lab212/data/mitoeroutput'

@app.route('/api/csv-files')
def list_csv_files():
    files = [f for f in os.listdir(CSV_FILES_DIR) if f.endswith('.csv')]
    return jsonify(files)

@app.route('/api/download-csv')
def download_csv():
    file_name = request.args.get('file')
    return send_from_directory(CSV_FILES_DIR, file_name, as_attachment=True)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, debug=True)
