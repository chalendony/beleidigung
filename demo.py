"""
Demostrator to show the entities that are detected within text
"""
from germeval import GermanEval
from conll import beschwerden_matcher
from visual import render


if __name__ == "__main__":
    # read blist
    lst = GermanEval().readblist()

    # read some docs with beschw.
    docs = GermanEval().load_demo()

    # find entities in docs
    annotations = beschwerden_matcher(lst, docs)

    # visually markup entities
    docmap = render(annotations)

    # TODO pass to  html ....
