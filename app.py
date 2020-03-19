#!flask/bin/python
from flask import Flask, request
import ole_scan
from flask import render_template
import requests
import os

UPLOAD_FOLDER = "./uploadedfiles"

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/')
# Generate Front-end
def index():
    return render_template("index.html")

@app.route('/AnalyzeFile', methods = ["POST"])
def analyzeFile():
   if request.method == "POST":
        print("POST DETECT")
        # Get file from client
        file = request.files['file']
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], file.filename) 
        file.save(filepath)    
        print("FILE RETRIEVED")
        # Pass file for processing
        ole_scan.startScan(filepath)
        return "File Uploaded"

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
