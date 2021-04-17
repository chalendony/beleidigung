import glob
import collections
import pandas as pd
# TODO class reader

import re

Germeval = collections.namedtuple('Germeval', 'sentence label_task1 label_task2  label_task3 filename')
target = ['OFFENSE', 'INSULT', 'EXPLICIT', 'ABUSE', 'OTHER', 'PROFANITY', 'IMPLICIT']
# TODO create regex from target
#reg_target = "'OFFENSE | INSULT | EXPLICIT | ABUSE | OTHER | PROFANITY | IMPLICIT'"
delimeter = 'OFFENSE|OTHER'

def read():
    #tuple

    count = 0
    for name in glob.glob('germeval/EX*.txt'):
        lst = []
        print(name)
        with open(name) as fp:
           
            lines = fp.readlines()
            for line in lines:
                line = line.strip()
                splits = line.split('\t')
                print(f" {splits}")
                sentence = splits[0]
                labels = splits[1:-1]
                #print(f" {labels}")
               
                label_task3 = "NA"
                if len(labels) == 3:
                    label_task3 = labels[2]

                lst.append(Germeval(sentence=sentence, label_task1=labels[0], label_task2=labels[1], label_task3=label_task3, 
                    filename=name))
           
    df = pd.DataFrame(lst)
    print(f"shape {df.shape}")

if __name__ == "__main__":
    read()

    