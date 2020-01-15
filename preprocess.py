#Helper method for pre-processing
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.corpus import stopwords
import glob
import nltk
from pycontractions import Contractions
import spacy

#method to remove contraction
def removeconcat(line, cont):
         return list(cont.expand_texts([line]))

#Note this method must be run after the SpellCheck method provided in the C# program
stopWords = set(stopwords.words())
path = 'C:\\Temp\\conversations\\*.json'   
cont = Contractions(api_key="glove-twitter-100")
cont.load_models()
files=glob.glob(path)   
nlp = spacy.load('en')
for file in files:     
    f=open(file, 'r')  
    lines=f.readlines()
    alllines=removeconcat(line, cont)
    for line in lines:
        doc=nlp(line)
        for ent in doc.ents:
            print(ent, ent.lemma_, ent.label_)       
    f.close()
 