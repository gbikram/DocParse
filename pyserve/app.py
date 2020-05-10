#!flask/bin/python
from flask import Flask, request
import ole_scan
from flask import render_template
from flask_cors import CORS
import os

UPLOAD_FOLDER = "./uploadedfiles"

app = Flask(__name__)
CORS(app)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# @app.route('/')
# # Generate Front-end
# def index():
#     return render_template("index.html")

# Called on upload
@app.route('/AnalyzeFile', methods = ["POST"])
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
    app.run(host='0.0.0.0', port=5555, debug=True)
