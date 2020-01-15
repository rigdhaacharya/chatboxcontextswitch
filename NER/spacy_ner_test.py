#!/usr/bin/env python
# coding: utf8
"""Example of training spaCy's named entity recognizer, starting off with an
existing model or a blank model.

For more details, see the documentation:
* Training: https://spacy.io/usage/training
* NER: https://spacy.io/usage/linguistic-features#named-entities

Compatible with: spaCy v2.0.0+
"""
from __future__ import unicode_literals, print_function

import plac
import random
from pathlib import Path
import spacy
from spacy.util import minibatch, compounding
import csv



@plac.annotations(
    model=("Model name. Defaults to blank 'en' model.", "option", "m", str),
    output_dir=("Optional output directory", "option", "o", Path),
    n_iter=("Number of training iterations", "option", "n", int))
def main(model=None, output_dir="c:\\temp\\model80", n_iter=100):
    data=GetNer()
    data_train = data[:15987] # use 80% of available data
    testdataLen = len(data)-len(data_train)
    testIndexStart = len(data_train)
    testIndexEnd = testIndexStart+testdataLen
    data_test=data[testIndexStart:testIndexEnd]    
    #data_test=data[:2]

        # test the saved model
    print("Loading from", output_dir)
    nlp2 = spacy.load(output_dir)        
    data_test_pred=[]
    for text, annotations in data_test:
      if(text):
        entities={}
        entities["entities"]=[]
        doc = nlp2(text)
        for ent in doc.ents:
          start=text.find(ent.text)
          end=start+len(ent.text)
          ner=ent.label_
          entities["entities"].append((start, end, ner))
        tupleTa = (text, entities)
        data_test_pred.append(tupleTa)
    
    #now compare the pred vs reality
    correct=0
    total=0
    for i in range(testdataLen):
      pred_text, pred_entity = data_test_pred[i]
      actual_text, actual_entity = data_test[i]
      items_pred = pred_entity.get('entities')
      items_actual = actual_entity.get('entities')
      length = len(items_actual)
      for j in range(length):
        total=total+1        
        if(items_actual[j] in items_pred):
          #if(items_pred[j] == items_actual[j]):
          correct= correct+1
        

    accuracy=correct/total
    print('model accuracy is', accuracy)



def GetNer():
  train_data=[]

  with open("C:\\Users\\v-riach\\Desktop\\581\\structured.txt", errors='ignore') as f:
    reader = csv.reader(f, delimiter="\t")
    for i, line in enumerate(reader):      
      x=line[0].split(';')      
      user=str.strip(x[0])
      intent=str.strip(x[1])
      text=str.strip(x[2])
      origin=str.strip(x[3])
      dest=str.strip(x[4])
      adults=str.strip(x[5])
      budget=str.strip(x[6])
      date=str.strip(x[7])
      entities={}
      entities["entities"]=[]
      if(origin):
        start=text.find(origin)
        end=start+len(origin)
        ner="ORIGIN"
        entities["entities"].append((start, end, ner))
      if(dest):
        start=text.find(dest)
        end=start+len(dest)
        ner="DEST"
        entities["entities"].append((start, end, ner))
      if(adults):
        start=text.find(adults)
        end=start+len(adults)
        ner="ADULTS"
        entities["entities"].append((start, end, ner))
      if(budget):
        start=text.find(budget)
        end=start+len(budget)
        ner="BUDGET"
        entities["entities"].append((start, end, ner))
      if(date):
        start=text.find(date)
        end=start+len(date)
        ner="DATE"
        entities["entities"].append((start, end, ner))
      tupleT = (text, entities)
      train_data.append(tupleT)
  return train_data


if __name__ == '__main__':    
    plac.call(main)

    # Expected output:
    # Entities [('Shaka Khan', 'PERSON')]
    # Tokens [('Who', '', 2), ('is', '', 2), ('Shaka', 'PERSON', 3),
    # ('Khan', 'PERSON', 1), ('?', '', 2)]
    # Entities [('London', 'LOC'), ('Berlin', 'LOC')]
    # Tokens [('I', '', 2), ('like', '', 2), ('London', 'LOC', 3),
    # ('and', '', 2), ('Berlin', 'LOC', 3), ('.', '', 2)]