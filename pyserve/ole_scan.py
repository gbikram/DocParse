from oletools.olevba import VBA_Parser, TYPE_OLE, TYPE_OpenXML, TYPE_Word2003_XML, TYPE_MHTML
from docx import Document
from docx.opc.constants import RELATIONSHIP_TYPE as RT
import sys
import datetime
import json
import eml_parser
import mailparser
from phishml import test_pretrained_model as phishml

UPLOAD_FOLDER = "./uploadedfiles"

# Uses olevba to analyze macros and get all IOCs from a Macro - DOC+DOCX
def getVbaIOCs(pathToFile):
    vbaparser = VBA_Parser(pathToFile)
    
    if (vbaparser.detect_vba_macros()) is False:
        return None

    results = vbaparser.analyze_macros()
    json_macros = []
    for kw_type, keyword, description in results:
        macro_data = {}
        macro_data['type'] = kw_type
        macro_data['keyword'] = keyword
        macro_data['description'] = description
        json_macros.append(macro_data)
    vbaparser.close()
    
    return json_macros

# Get URLs from Docx - constraint - only accepts docx
def getDocxURLs(pathToFile):
    document = Document(pathToFile)
    rels = document.part.rels
    urls = []
    for rel in rels:
        if rels[rel].reltype == RT.HYPERLINK:      
            urls.append(rels[rel]._target)
    return urls

def jsonSerial(obj):
    if isinstance(obj, datetime.datetime):
        serial = obj.isoformat()
        return serial

# Get IOCs from email
def getEmailIOCs(pathToFile):
    json_out = {}

    mailParser = mailparser.parse_from_file(pathToFile)

    with open(pathToFile, 'rb') as emailFile:
        rawEmail = emailFile.read()
    ep = eml_parser.EmlParser()
    parsedEmail = ep.decode_email_bytes(rawEmail)
    del parsedEmail['body']
    # print(json.dumps(parsedEmail, default=jsonSerial))

    if 'attachment' in parsedEmail:
        attachments = []
        mailParser.write_attachments(UPLOAD_FOLDER)

        # For each attachment in output, check attachment extension & scan
        for attachment in parsedEmail['attachment']:
            attachmentData = {}
            attachmentData['file_name'] = attachment['filename']
            attachmentData['hash'] = {
                'md5': attachment['hash']['md5'],
                'sha256': attachment['hash']['sha256']
            }            
            
            # Docx  or DOC file
            if(attachment['filename'].endswith(".docx") or attachment['filename'].endswith(".doc") ):
                if(attachment['filename'].endswith(".docx")):
                    attachmentData['body_urls'] = getDocxURLs(UPLOAD_FOLDER + '/' + attachment['filename'])
                attachmentData['macros'] = getVbaIOCs(UPLOAD_FOLDER + '/' + attachment['filename'])
            
            # Email File
            elif(attachment['filename'].endswith(".eml")):
                attachmentData['file_name']['email_iocs'] = getEmailIOCs(pathToFile)        
            
            attachments.append(attachmentData)
        
        json_out['attachments'] = attachments
    json_out['headers'] = parsedEmail['header']['header']
    json_out['resolution'] = "benign"
    
    # Parse Raw Email
    mail = mailparser.parse_from_file(pathToFile)
    
    # Get URLs from raw email
    bodyUrls = ep.get_uri_ondata(mail.body)
    
    # Convert body urls to dict
    bodyUrlsDict = []
    urlCounter = 0 
    for bodyUrl in bodyUrls:
        bodyUrlData = {}
        bodyUrlData['url'] = bodyUrl

        urlCounter += 1

        print(bodyUrl)

        if(json_out['resolution'] == "benign"):
            if(phishml.runPhishCheck(bodyUrl)):
                json_out['resolution'] = "phishing"
    
        if(urlCounter == 10 or "unsubscribe" in bodyUrl):
            json_out['resolution'] = "spam"
        bodyUrlsDict.append(bodyUrlData)
    
    json_out['body_urls'] = bodyUrlsDict

    return json_out

def startScan(pathToFile):
    # Check if DOCX file since this supports only DOCX for now. Probably need a switch case for various formats

    filename = pathToFile.split("/")[2]
    results_json = {}
    results_json[filename] = {}

    # DOCX File or DOC File
    if(filename.endswith(".docx") or filename.endswith(".doc")):
        
        # If DOCX - get all URLs from body. 
        # Need to add support for DOC
        if(filename.endswith(".docx")):
            results_json[filename]['file_type'] = "docx"
            results_json[filename]['body_iocs'] = getDocxURLs(pathToFile)
        elif(filename.endswith("doc")):
            results_json[filename]['file_type'] = "doc"

        results_json[filename]['macro_iocs'] = getVbaIOCs(pathToFile)  

    # Email File
    elif(filename.endswith(".eml")):
        results_json[filename]['file_type'] = "eml"
        results_json[filename]['email_data'] = getEmailIOCs(pathToFile)
    
    else:
        results_json['error'] = 'invalid file'
    return results_json

# Only for running the script directly like cli
if __name__ == "__main__":
    # execute only if run as a script
    pathToFile = sys.argv[1]
    startScan(pathToFile)
