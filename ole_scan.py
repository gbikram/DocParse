from oletools.olevba import VBA_Parser, TYPE_OLE, TYPE_OpenXML, TYPE_Word2003_XML, TYPE_MHTML
from docx import Document
from docx.opc.constants import RELATIONSHIP_TYPE as RT
import sys

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

filename = sys.argv[1]
if(filename.endswith(".docx")):
    print()
    print("IOCs from Embedded Macro:")
    getVbaIOCs(filename)
    print()
    print("=================================================")
    print()
    print("IOCs from Document Body")
    getDocURLs(filename)
else:
    print("Given file is not a DOCX!")