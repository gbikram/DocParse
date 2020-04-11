# Application for parsing emails and documents

## Usage
Activating venv
source env/bin/activate
python3 -m pip install -r requirements.txt 

## To-Do:

Server Side:
Save email files in unique folder
Add functionality for other documents - PDF, DOC, EML
    EML - DONE
    DOCX - DONE
    PDF - Hash, URLs
    DOC - Get Body URLs
    XLS, PPT - Seems like - need to test
Heroku Dev setup
Save IOCs with file name hash within a NoSQL database
IOC integration with VirusTotal / Other OSINT
Template matching to detect credential harvesters - Scan HTML and match with domain to detect cred harvester (More keyword matches = login form != to website domain = high cred harv confidence)


Client Side
Fix footer use flexbox - https://css-tricks.com/couple-takes-sticky-footer/


Additional Features that can be considered:
Oletools malware deobfuscation - for emotet 

Troubleshooting:
https://medium.com/cleversonder/from-zero-to-hero-with-vue-advanced-components-parcel-dev-tools-fab980a62259
