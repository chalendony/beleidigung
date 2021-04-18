import glob
import collections
import pandas as pd
import itertools

import re

Germeval = collections.namedtuple('Germeval', 'sentence label_task1 label_task2  label_task3 filename')
PROFANITY = "PROFANITY"
OTHER = "OTHER"

def readblist():
    text = []
    for name in glob.glob('Beschwerdeliste.csv'):
        with open(name) as fp:
            lines = fp.readlines()
            for line in lines:
                splits = line.split(",")
                term = splits[1]
                text.append(term.strip().lower())
    return text

def exact_match(targetlst):
    text = []
    terms = []
    for name in glob.glob('germeval/*.txt'):

        with open(name) as fp:
            print(f" {name}")
            lines = fp.readlines()
            for line in lines:
                line = line.strip()
                splits = line.split('\t')
                sentence = splits[0]
        #   """       tmp = [(t,line) for t in targetlst if t in line.lower()]
        #         if  tmp: 
                   
        #             text.append(list(itertools.chain(*tmp))) # flatten the list """
                
                
                for term in targetlst:
                    if term in sentence.lower():
                        text.append(sentence) 
                        terms.append(term)

    print(f"Count B-list {len(text)}") 
    print(f"Unique terms {len(set(terms))}")   
    # for i in text:
    #     print(f"beschwerde::  {i}")


def profanity():
    #tuple

    count = 0
    for name in glob.glob('germeval/*.txt'):
        text = []
        with open(name) as fp:
            print(f" {name}")
            lines = fp.readlines()
            for line in lines:
                if PROFANITY in line:
                    line = line.strip()
                    splits = line.split('\t')
                    #print(f" line: {name} {splits}")
                    sentence = splits[0]
                    labels = splits[1:]
                    #print(f" labels {labels}")
                
                    label_task3 = "NA"
                    if len(labels) == 3:
                        label_task3 = labels[2]

                    
                    text.append(sentence)
           
    print(f"Gereval profanity {len(text)}")       
    for i in text:
        print(f"profanity::  {i}")


def read():
    #tuple

    count = 0
    for name in glob.glob('germeval/*.txt'):
        lst = []
       
        with open(name) as fp:
            print(f" {name}")
            lines = fp.readlines()
            for line in lines:
                line = line.strip()
                splits = line.split('\t')
                #print(f" line: {name} {splits}")
                sentence = splits[0]
                labels = splits[1:]
                #print(f" labels {labels}")
               
                label_task3 = "NA"
                if len(labels) == 3:
                    label_task3 = labels[2]

                lst.append(Germeval(sentence=sentence, label_task1=labels[0], label_task2=labels[1], label_task3=label_task3, 
                    filename=name))

    df = pd.DataFrame(lst)
    print(f"shape {df.shape}")
    print(f"shape {df.head}")


if __name__ == "__main__":
   #profanity()
   targets = readblist()
   exact_match(targets)


    