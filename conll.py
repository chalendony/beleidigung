"""
create conll formats
"""

import numpy as np
import pandas as pd
import spacy
from spacy.pipeline import EntityRuler
import re 

from germeval import GermanEval
from constants import Entity

nlp = spacy.load("de_core_news_sm")

# TODO: move to constants
entity_types = {"beschwerden": "BESCHWER", "person":"PERSON"}

def beschwerden_matcher(blist, docs):
    rexpression = "|".join(blist)
    regex = f"{rexpression}"

    doc_lst = []
    for adoc in docs:
        entity_lst = []
        docid = adoc["id"]
        text = adoc["text"]
        matches = re.finditer(regex, text.lower(), re.MULTILINE)
        for match_number, match in enumerate(matches, start=0):
            entity_lst.append(Entity(docid, match.group(),match.start(),match.end(), entity_types["beschwerden"] ))
        doc_lst.append([docid, text, entity_lst])        
              
    return doc_lst





def conll(text):

    text = "XYZ Sebastian ist in der Welt und hat gefunden."
    # give the span
    entities = [("BEL", 0, 3), ("PPP", 4, 13)]
    doc = nlp(text)

    ents = []
    for ee in entities:
        ents.append(doc.char_span(ee[1], ee[2], ee[0]))
    doc.ents = ents
    for e in doc:
        # TODO: combine the last two columns in an appropriate format with hyphen
        print(e.text, e.ent_iob_, e.ent_type_)


if __name__ == "__main__":
    lst = GermanEval().readblist()
    docs = ""
    entities = beschwerden_matcher(lst, docs)
    print(entities)

