# -*- encoding: utf-8 -*-

## important http://www.crosscite.org/cn/

## doi extraction
from PyPDF2 import PdfFileReader
import re
import sys

## doi lookup

import requests
import json

## doi regex
doi_re = re.compile(r"""\b(10[.][0-9]{4,}(?:[.][0-9]+)*/(?:(?!["&\'])\S)+)\b""")

class DoiNotFound(Exception):
    pass
class RefNotFound(Exception):
    pass

class CrossRefClient(object):
    
    def __init__(self, accept='application/vnd.citationstyles.csl+json', timeout=3):
        self.headers = {'accept': accept}
        self.timeout = timeout
 
    
    def query(self, doi, q={}):
        if doi.startswith("http://"):
            url = doi
        else:
            url = "http://dx.doi.org/" + doi
        
        r = requests.get(url, headers = self.headers)
        return r
    
    def doi2json(self, doi):
        self.headers['accept'] = 'application/vnd.citationstyles.csl+json'
        return self.query(doi).json()

 
def getDoi(pdf_file):
     input_ = PdfFileReader(open(pdf_file, "rb"))
     doc_info = input_.getDocumentInfo()
     
     doi = None
     try:
         doi = doc_info['/doi']
     except KeyError:
         try:
             text = input_.getPage(0).extractText()
             doi = doi_re.findall(text)[0]
         except:
             raise DoiNotFound
     return doi

def getRef(doi):
    try:
        s = CrossRefClient()
        return s.doi2json(doi)
    except:
        raise RefNotFound
