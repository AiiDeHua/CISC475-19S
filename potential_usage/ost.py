# coding = utf-8
import bibtexparser as bp
from bibtexparser.bparser import BibTexParser
from bibtexparser.customization import convert_to_unicode
import os, shutil

work_dir = 'bib/'
for parent, dirnames, filenames in os.walk(work_dir,  followlinks=True):
    for filename in filenames:
        with open(work_dir+filename) as bibfile:
            parser = BibTexParser()
            parser.customization = convert_to_unicode
            bibdata = bp.load(bibfile, parser = parser)
            print(bibdata.entries[0]['abstract'])
