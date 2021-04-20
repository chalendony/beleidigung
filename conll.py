"""
create conll formats
"""

import numpy as np
import pandas as pd
import spacy
from spacy.pipeline import EntityRuler
import re 
from collections import namedtuple

# maybe this can be blank??
nlp = spacy.load("de_core_news_sm")
Entity = namedtuple("Entity", "entity_value, start, end, entity_type, ")
entity_types = {"beschwerden": "BESCHWER", "person":"PERSON"}

def beschwerden_matcher():
    name = "Sebastian|XYZ"
    regex = f"{name}"
    docs = ["XYZ Sebastian ist in der Welt und hat gefunden."]

    lst = []
    for adoc in docs:
        matches = re.finditer(regex, adoc, re.MULTILINE)
        for match_number, match in enumerate(matches, start=0):
            lst.append(Entity(match.group(),match.start(),match.end(), entity_types["beschwerden"] ))
            
              
    return lst





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
    lst = exactmatcher()
    print(lst)

