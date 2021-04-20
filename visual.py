# read the data
# use spacy to display annotations
import spacy
from spacy import displacy
from constants import Entity, HTML_TEMPLATE, entity_types, MARK
from string import Template
nlp = spacy.load("de_core_news_sm")


def render_css(annotations):
    MARK_OPEN = Template("""
    <mark data-entity="$ner_type">
    $ner_value
    """  )
    
    MARK_CLOSE = " </mark>"

    docmap = []
    result = ""
    for ann in annotations:
        docid = ann[0]
        result = result + f"<p>{docid}</p>"
        text = ann[1].lower()
        print(text)
        entity = ann[2]
        ents = []
        for e in entity:
            entity_type = getattr(e, "entity_type")
            entity_value = getattr(e, "entity_value")
            start = getattr(e, "start")
            end = getattr(e, "end")
            # insert mark around entity within string
            result = result + f"{text[0:start]} {MARK_OPEN.substitute(ner_type=entity_type, ner_value=entity_value)}  {entity_value} {MARK_CLOSE} {text[end:-1]} <br>"

    result = HTML_TEMPLATE.substitute(mark=result)        
    with open("demo.html", "w") as f:   
        f.write(result)
    print("See file: demo.html")

def html_css(annotations):
    mark = ""
    for d in docmap:
        docid = d[0]
        text = d[1]
        mark = mark + f"<p>{docid}</p><br><br>"

        entity_lst = d[2]
        for e in entity_lst:
            ner_type = e[0]
            ner_value = e[1]
            mark = mark +  MARK.substitute(ner_type=ner_type, ner_value=ner_value) + f"<br>"
    result = HTML_TEMPLATE.substitute(mark=mark)
    with open("demo.html", "w") as f:   
        f.write(result)
    print("See file: demo.html")


def render_displacy(annotations):

    # override for spacy html templates for rendering entity
    TEMPLATE_ENT = """
<mark data-entity="{label}">{text}</mark>
"""


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
    html(docmap)    
    return docmap



def display_tmp():

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
    display_tmp()
