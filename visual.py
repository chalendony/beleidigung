# read the data
# use spacy to display annotations
import spacy
from spacy import displacy
from constants import Entity

nlp = spacy.load("de_core_news_sm")

# override for spacy html templates
TEMPLATE_ENT = """
<mark data-entity="{label}">{text}</mark>
"""

def render(annotations):
    
    docmap = []
    for ann in annotations:
        docid = ann[0]
        text = ann[1].lower()
        print(text)
        entity = ann[2]
        doc = nlp(text)
        ents = []
        distinct_entities = []
        for e in entity:
            start = getattr(e, "start")
            end = getattr(e, "end")
            entity_value = getattr(e, "entity_value")
            distinct_entities.append(entity_value)
            print(f"*************{entity_value}, {start}, {end}")
            ents.append(doc.char_span(start, end, entity_value))
        print(ents)
        doc.ents = ents
        options = {"ents": list(set(distinct_entities)), "template": TEMPLATE_ENT}
        render = displacy.render(docs=doc, style="ent", options=options)
        docmap.append((docid, render))
    return docmap



def display():

    text = "XYZ Sebastian ist in der Welt und hat gefunden."
    # give the span
    entities = [("BEL", 0, 3), ("PPP", 4, 13)]
    doc = nlp(text)

    ents = []
    for ee in entities:
        ents.append(doc.char_span(ee[1], ee[2], ee[0]))

    doc.ents = ents
    colors = {"BEL": "#E8DAEF", "PPP": "#F02A8F"}
    entities = ["BEL", "PPP"]

    options = {"ents": entities, "colors": colors, "template": TPL_ENT}
    render = displacy.render(docs=doc, style="ent", options=options)
    print(render)


if __name__ == "__main__":
    display()
