from oletools.olevba import VBA_Parser, TYPE_OLE, TYPE_OpenXML, TYPE_Word2003_XML, TYPE_MHTML
from docx import Document
from docx.opc.constants import RELATIONSHIP_TYPE as RT
import sys
import datetime
import json
import eml_parser
import mailparser

# Uses olevba to analyze macros and get all IOCs from a Macro
def getVbaIOCs(filename):
    vbaparser = VBA_Parser(filename)
    results = vbaparser.analyze_macros()
    if(results != None):
        for kw_type, keyword, description in results:
            print('type=%s - keyword=%s - description=%s' % (kw_type, keyword, description))
    vbaparser.close()

# Get URLs from Docx - constraint - only accepts docx
def getDocURLs(filename):
    document = Document(filename)
    rels = document.part.rels
    links = []
    for rel in rels:
        if rels[rel].reltype == RT.HYPERLINK:      
            print(rels[rel]._target)

def jsonSerial(obj):
    if isinstance(obj, datetime.datetime):
        serial = obj.isoformat()
        return serial

# Get IOCs from email
def getEmailIOCs(filename):
    with open(filename, 'rb') as emailFile:
        rawEmail = emailFile.read()
    parsedEmail = eml_parser.eml_parser.decode_email_b(rawEmail, include_attachment_data=True)
    output = json.dumps(parsedEmail, default=jsonSerial)
    outFile =  open("eml_scan_results.json", "w+")
    outFile.write(output)
    print("Output File Generated\n")
    mail = mailparser.parse_from_file(filename)
    print(eml_parser.eml_parser.get_uri_ondata(mail.body))

def startScan(filename):
    # Check if DOCX file since this supports only DOCX for now. Probably need a switch case for various formats
    if(filename.endswith(".docx")):
        print()
        print("IOCs from Embedded Macro:")
        getVbaIOCs(filename)
        print()
        print("=================================================")
        print()
        print("IOCs from Document Body")
        getDocURLs(filename)
    elif(filename.endswith(".eml")):
        print()
        print("IOCs from " + filename)
        getEmailIOCs(filename)
    else:
        print("Invalid File Type")

if __name__ == "__main__":
    # execute only if run as a script
    filename = sys.argv[1]
    startScan(filename)