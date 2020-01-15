from nltk import word_tokenize, pos_tag, ne_chunk
import spacy

sentence="Book me a flight to Miami from Seattle for Jan 7 for 8 people for $500"
ne_tree = ne_chunk(pos_tag(word_tokenize(sentence)))
print('Named Entity Extraction with Default NLTK model')
print(ne_tree)
nlp = spacy.load('en')
doc = nlp(sentence)
print('Named Entity Extraction with EN Spacy model')
for ent in doc.ents:
    print(ent.text, ent.label_)