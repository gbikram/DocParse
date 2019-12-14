#!flask/bin/python
from flask import Flask
import ole_scan
from flask import render_template

app = Flask(__name__)

@app.route('/')
# Generate Front-end
def index():
    return render_template("index.html")

# @app.route('AnalyzeFile')
#     def analyzeFile():
        
if __name__ == '__main__':
    app.run(host='0.0.0.0')