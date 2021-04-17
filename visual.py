
# read the data
# use spacy to display annotations
import spacy
from spacy import displacy

# maybe this can be blank??
nlp = spacy.load('de_core_news_sm')

# override for html templates
TPL_ENTS = """
<div class="entities">{content}</div>
"""

TPL_ENT = """
<mark data-entity="{label}">{text}</mark>
"""

def display():

    text = "XYZ Sebastian ist in der Welt und hat gefunden."
    # give the span
    entities = [("BEL", 0, 3),("PPP", 4, 13)]   
    doc = nlp(text)

    ents = []
    for ee in entities:
        ents.append(doc.char_span(ee[1], ee[2], ee[0]))

    doc.ents = ents
    colors = {"BEL":"#E8DAEF", "PPP":"#F02A8F"}
    entities  = ["BEL", "PPP"]

    options = {"ents": entities, "colors":colors, "template":TPL_ENT}  
    render = displacy.render(docs=doc, style="ent", options=options)
    print(render)



if __name__ == "__main__":
    display()