# Application for parsing emails and documents

## Phishing Detection Sources:
https://checkphish.ai/checkphish-api - To-Do
KDNuggets Pre-trained ML model

## Malware Detection Sources:
* oletools
* peepdf - To-Do

## Usage
Activating venv
source env/bin/activate
python3 -m pip install -r requirements.txt 

## To-Do:
Additional Sources - Checkphish.ai, VirusTotal, peepdf, spamassasin

### Server Side:
* Save email files in unique folder
* Add functionality for other documents - PDF, DOC, EML
    * EML - DONE
    * DOCX - DONE
    * PDF - Hash, URLs
    * DOC - Get Body URLs
    * XLS, PPT - Seems like - need to test
* Save IOCs with file name hash within a NoSQL database
* IOC integration with VirusTotal / Other OSINT
* Template matching to detect credential harvesters - Scan HTML and match with domain to detect cred harvester (More keyword matches = login form != to website domain = high cred harv confidence)


### Client Side
* Fix footer use flexbox - https://css-tricks.com/couple-takes-sticky-footer/


### Additional Features that can be considered:
* Oletools malware deobfuscation

### Troubleshooting:
* https://medium.com/cleversonder/from-zero-to-hero-with-vue-advanced-components-parcel-dev-tools-fab980a62259
* https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/
* https://docs.python.org/3/library/venv.html


#### Activate virtual env
* source env/bin/activate
* python -m pip install -r requirements.txt
* python app.py

#### Run Client
* sudo docker build -t docparse-vue .
* sudo docker run -it -p 127.0.0.1:80:8080 --rm --name docparse-vue docparse-vue

#### Run Server
* sudo docker build --tag flask-docparse .
* sudo docker run --name flask-docparse -p 5000:5000 flask-docparse

### Build Docker Compose:
docker-compose up --build