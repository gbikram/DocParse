from oletools.olevba import VBA_Parser, TYPE_OLE, TYPE_OpenXML, TYPE_Word2003_XML, TYPE_MHTML
from docx import Document
from docx.opc.constants import RELATIONSHIP_TYPE as RT

# Uses olevba to analyze macros and get all IOCs from a Macro
def getVbaIOCs(filename):
    vbaparser = VBA_Parser(filename)
    results = vbaparser.analyze_macros()
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

getVbaIOCs("Malicious Samples/__00FYI SHIPPING DOC.doc")
print("=================================================")
getDocURLs("Malicious Samples/addresses.docx")