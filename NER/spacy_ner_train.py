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


# training data
TRAIN_DATA = [
    ('Book me a flight to Miami from Capricia for 5 people in Jan for $1700', {
        'entities': [(20, 25, 'LOC'), (56,59, 'DATE')]
    }),
    ('Flight to Seattle for Dec 2', {
        'entities': [(10, 17, 'LOC'), (22, 27, 'DATE')]
    }),
    ('Flight to Miami for Dec 3', {'entities':[(10,15, 'LOC'), (20,25, 'DATE')]})
]

TEST_DATA = [
    ('Book me a flight to Denver')
]


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

    """Load the model, set up the pipeline and train the entity recognizer."""
    if model is not None:
        nlp = spacy.load(model)  # load existing spaCy model
        print("Loaded model '%s'" % model)
    else:
        nlp = spacy.blank('en')  # create blank Language class
        print("Created blank 'en' model")

    # create the built-in pipeline components and add them to the pipeline
    # nlp.create_pipe works for built-ins that are registered with spaCy
    if 'ner' not in nlp.pipe_names:
        ner = nlp.create_pipe('ner')
        nlp.add_pipe(ner, last=True)
    # otherwise, get it so we can add labels
    else:
        ner = nlp.get_pipe('ner')

    # add labels
    for _, annotations in data_train:
        for ent in annotations.get('entities'):
            ner.add_label(ent[2])

    # get names of other pipes to disable them during training
    other_pipes = [pipe for pipe in nlp.pipe_names if pipe != 'ner']
    with nlp.disable_pipes(*other_pipes):  # only train NER
        optimizer = nlp.begin_training()
        for itn in range(n_iter):
            random.shuffle(data_train)
            losses = {}
            # batch up the examples using spaCy's minibatch
            batches = minibatch(data_train, size=compounding(4., 32., 1.001))
            for batch in batches:
                texts, annotations = zip(*batch)
                nlp.update(
                    texts,  # batch of texts
                    annotations,  # batch of annotations
                    drop=0,  # dropout - make it harder to memorise data
                    sgd=optimizer,  # callable to update weights
                    losses=losses)
            print('Losses', losses)

    # test the trained model
    #for text in data_test:
        #doc = nlp(text[0])
        #print('Entities', [(ent.text, ent.label_) for ent in doc.ents])
        #print('Tokens', [(t.text, t.ent_type_, t.ent_iob) for t in doc])

    # # save model to output directory
    if output_dir is not None:
        output_dir = Path(output_dir)
        if not output_dir.exists():
            output_dir.mkdir()
        nlp.to_disk(output_dir)
        print("Saved model to", output_dir)

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
              #print('Entities', [(ent.text, ent.label_) for ent in doc.ents])
              tupleTa = (text, entities)
              data_test_pred.append(tupleTa)
              #print('Tokens', [(t.text, t.ent_type_, t.ent_iob) for t in doc])
    
    #now compare the pred vs reality
    correct=0
    total=0
    for i in range(testdataLen):
      pred_text, pred_entity = data_test_pred[i]
      actual_text, actual_entity = data_test[i]
      items_pred = pred_entity.get('entities')
      items_actual = actual_entity.get('entities')
      # for index, item in enumerate(pred_entity):
      #   total=total+1
      #   if(actual_entity[index] == item):
      #     correct=correct+1

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