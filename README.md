---------
Intro
---------
This repo contains classifiers to check if a context switch has occured during
a chatbox conversations. As humans we understand if our counterpart changes context from talking about Mexico to their trip in Bali. For computers, it is a tougher task and to switch back and forth between contexts. 


------------
Code details
------------
Source code to replicate the results of this project are provided in the zip file.
The list below explains the included python files and their purpose.
1. preprocess.py - Implements the Contraction and Stop word removal as well
as the lemmatization
2. frameSwitch Ada.py - Implements the Ada booster classifier
3. frameSwitch CV.py - Implements the Grid Search with Cross Validation for
finding the best hyper parameters for the artificial neural network model
4. frameSwitch DecTree.py - Implements the Decision Tree classifier with Fea-
ture Selection by wrapper method
5. frameSwitch NaiveBayes.py - Implements the Naive Bayes classifier with
Feature selection by wrapper method
Smarter Chatbots with Memory 15
6. frameSwitch NN.py - Implements the artificial neural network classifier
7. frameSwitch RandForest.py - Implements the Random Forest classifier
8. frameSwitch SVC.py - Implements the Support Vector Machine with poly-
nomial kernel and feature selection by wrapper method
9. NER
ner compare.py - Small file to compare Entity Extraction using prebuilt
NLTK and Spacy models
10. NER
spacy ner train.py - Script to train the custom Spacy NER model
11. NER
spacy ner test.py - Script to test the trained custom Spacy NER model
In addition to the included the python files, the zip file also includes the csproj
and .cs files associated with the C# program for data extraction and pre-
processing. The C# program includes the following:
1. BingSpellcheck.Spellcheck - Method to correct the spellings of the frame
dataset using the Bing Spell check API
2. SpellCheckSchema.cs - Object representation of the Bing Spell Check API
result
3. DocumentSchema.cs - Object representation of the Frames dataset JSON
4. Program.MakeStructuredData - Program to generate the CSV file used for
classification using oversampling for Class 1
5. Program.CreateNERModel - Program to generate the CSV file used for
training and testing the Named Entity Recognition model
Additionally, the zip file also contains the data in JSON and CSV formats.
1. frames.json - Original data [4] downloaded from Maluuba used by the C#
program
2. structured.text - CSV file used for Named Entity Recognition training and
testing
3. structured conv.text - CSV file used for training and testing the classifiers