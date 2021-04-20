import spacy
from spacy import displacy
from constants import Entity, entity_types, HTML_TEMPLATE,  MARK_CLOSE, MARK_OPEN
from string import Template
from operator import attrgetter

nlp = spacy.load("de_core_news_sm")


def render_css(annotations):
    """
    Use stlye sheet to create entire html page of annotated documents
    """
    docmap = []
    result = ""
    for ann in annotations:
        docid = ann[0]
        result = result + f"<p>DOK {docid}: "
        text = ann[1].lower()
        print(text)
        entity = ann[2]
        entity = sorted(entity, key=attrgetter('end'))
        # goes wonkey when multiple entities in single file, so using string replacement instead of positional replacement
        for e in entity:
            # get string
            entity_type = getattr(e, "entity_type")
            entity_value = getattr(e, "entity_value")
            start = getattr(e, "start")
            end = getattr(e, "end")
            target = text[start:end]
            text = text.replace(target, f"{MARK_OPEN.substitute(ner_type=entity_type, ner_value=entity_value)}  {MARK_CLOSE}", 1)
            # insert mark around entity within 
        result = result + text
    result = HTML_TEMPLATE.substitute(mark=result)        
    with open("demo.html", "w") as f:   
        f.write(result)
    print("See file: demo.html")
    return result



def render_displacy(annotations):
    """
    Use spacy to return html snippet of annotated documents
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
            ents.append(doc.char_span(start, end, entity_value))
        doc.ents = ents
        colors = {"BESCHWER": "#E8DAEF" }
        options = {"ents": list(set(distinct_entities)),"colors": colors,  "template": TEMPLATE_ENT}
        render = displacy.render(docs=doc, style="ent", options=options)
        docmap.append((docid, render))
    html(docmap)    
    return docmap

