"""
Store  GermanEval data in Exasol database
"""

import glob
from collections import namedtuple
import pandas as pd
import itertools
import re
from ClipToExa import ClipToExa
from nltk.tokenize import word_tokenize
from preprocessing import clean_tweet


# TODO: use to path class and not string
data_path = "./data"
beschwerde_file = data_path + "/Beschwerdeliste.csv"
germeval_file = data_path + "/*.txt"


PROFANITY = "PROFANITY"
OTHER = "OTHER"


class GermanEval:
    def germaneval_beschwerden(self, blist):
        GermanEval = namedtuple(
            "GermanEval",
            [
                "docid",
                "sentence",
                "beschwerde",
                "label_1",
                "label_2",
                "label_3",
                "filename",
            ],
        )
        docid = 0
        lst = []
        for name in glob.glob(germeval_file):
            with open(name) as fp:
                print(f"Reading file: {name}")
                lines = fp.readlines()
                for line in lines:

                    line = line.strip()
                    splits = line.split("\t")

                    # sentence
                    sentence = splits[0]
                    sentence = clean_tweet(sentence)
                    tokens = word_tokenize(sentence, language="german")
                    matched = self.exact_match(blist, tokens)

                    # labels
                    labels = splits[1:]
                    label_3 = ""  # not all files contain 3 labels
                    if len(labels) == 3:
                        label_3 = labels[2]

                    lst.append(
                        GermanEval(
                            docid,
                            sentence,
                            ",".join(matched),
                            labels[0],
                            labels[1],
                            label_3,
                            name,
                        )
                    )

                    docid += 1
        df = pd.DataFrame(lst)
        return df

    def read(self):
        GermanEval = namedtuple(
            "GermanEval",
            ["docid", "sentence", "label_1", "label_2", "label_3", "filename"],
        )
        docid = 0
        lst = []
        for name in glob.glob(germeval_file):
            with open(name) as fp:
                print(f"Reading file: {name}")
                lines = fp.readlines()
                for line in lines:
                    line = line.strip()
                    splits = line.split("\t")
                    sentence = splits[0]
                    labels = splits[1:]
                    label_3 = ""  # not all files contain 3 labels
                    if len(labels) == 3:
                        label_3 = labels[2]

                    lst.append(
                        GermanEval(docid, sentence, labels[0], labels[1], label_3, name)
                    )

                    docid += 1
        df = pd.DataFrame(lst)
        return df

    def readblist(self):
        text = []
        for name in glob.glob(beschwerde_file):
            with open(name) as fp:
                lines = fp.readlines()
                for line in lines:
                    splits = line.split(",")
                    term = splits[1]
                    text.append(term.strip().lower())
        return text

    def exact_match(self, blist, tokens):
        ## regex to perform exact match
        terms = []
        for tok in tokens:
            tok = tok.lower()
            for term in blist:
                if term == tok:
                    terms.append(term)
        # print(terms)
        return terms


    def load_demo(self):
        docs = [{"id":"42","text":"Die htte man frher als Hexe verbrannt."},
                {"id":"43","text":"Die Zeit ist berreif fr dass groe ausmesten in Politik, Justiz u Medien dieses ganze Rot Grn versiffte Parteibuch Pack zum Teufel jagen"},
                {"id":"44","text":"Ein Afrikaner der in China lebt oder geboren ist, ist dann WAS? Africhinese. Das ist lachhaft. Es gibt nur eine Nationale Identitt. Sie hngt von der Abstammung ab. Eine Ratte die im Pferdestall geboren wird, ist auch niemals ein Pferd. Darber sollte wohl Einigkeit bestehen."},
                {"id":"45","text":"Bei den Antifa Terroristen fllt mir nur eins ein, Der Dieb rannte aus dem Kaufhaus und schrie, haltet den Dieb"},
                {"id":"46","text":"Wie dmlich mssen erst die Sesselfurzer sein wenn sie den Unterschied von 17 und 32 Jahren nicht erkennen....?"}]
        return docs

    def profanity(self):
        count = 0
        for name in glob.glob("germeval/*.txt"):
            text = []
            with open(name) as fp:
                print(f" {name}")
                lines = fp.readlines()
                for line in lines:
                    if PROFANITY in line:
                        line = line.strip()
                        splits = line.split("\t")
                        # print(f" line: {name} {splits}")
                        sentence = splits[0]
                        labels = splits[1:]
                        # print(f" labels {labels}")

                        label_task3 = "NA"
                        if len(labels) == 3:
                            label_task3 = labels[2]

                        text.append(sentence)

        print(f"Gereval profanity {len(text)}")
        for i in text:
            print(f"profanity::  {i}")


if __name__ == "__main__":

    germeval = GermanEval()
    blist = germeval.readblist()
    df = germeval.germaneval_beschwerden(blist)
    cx = ClipToExa(tablename="ASR_GERMANEVAL_BESCHWERDEN", dev_mode=False, df=df)
    cx.main()
