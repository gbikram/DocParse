#!flask/bin/python
from flask import Flask, request
import ole_scan
from flask import render_template
from flask_cors import CORS, cross_origin
import os

UPLOAD_FOLDER = "./uploadedfiles"

app = Flask(__name__)
CORS(app)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/api/cors', methods = ["GET"])
# Test CORS
def cors_test():
    return "CORS Success"

# Called on upload
@app.route('/api/AnalyzeFile', methods = ["POST"])
# @cross_origin(origin='localhost', headers=['Access-Control-Allow-Origin', '*'])
def analyzeFile():
   if request.method == "POST":
        # Get file from client
        file = request.files['file']

        # Save file locally
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], file.filename) 
        file.save(filepath)    

        # Pass file for oletools processing
        return ole_scan.startScan(filepath)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
