#Helper method to find the best hyperparameters for the 
#artificial neural network using Grid Search with Cross Validation method
import numpy as np
from sklearn.preprocessing import LabelEncoder
from sklearn.preprocessing import OneHotEncoder
import pandas as pd
from sklearn import tree
from sklearn.metrics import classification_report, confusion_matrix 
import time
from sklearn.metrics import accuracy_score
from sklearn.neural_network import MLPClassifier
from sklearn.model_selection import GridSearchCV
from sklearn.metrics import roc_curve, auc


df=pd.read_csv("C:\\Temp\\conversations\\structured_conv.txt", delimiter=';')
user=df["User"]
intent=df["Intent"]
prevorigin=df["PrevOrigin"]
prevdest=df["PrevDestination"]
prevdate=df["PrevDate"]
prevadults=df["PrevAdults"]
prevbudget=df["PrevBudget"]
previntent=df["PrevIntent"]
origin=df["Origin"]
dest=df["Destination"]
adults=df["Adults"]
budget=df["Budget"]
date=df["Date"]
frameswitched=df["FrameSwitched"]

num_train=30000
num_pred=5132

totalzero=0
for x in range(num_train+1):
  if(frameswitched[x]==0):
    totalzero=totalzero+1

index_pred=num_train+num_pred
label_train=frameswitched[:num_train]
label_train_array=np.array(label_train)
label_test=frameswitched[num_train:index_pred]
label_test_array=np.array(label_test)
# integer encode
label_encoder = LabelEncoder()
prevorigin_encoded = label_encoder.fit_transform(prevorigin[:num_train])
prevdest_encoded = label_encoder.fit_transform(prevdest[:num_train])
prevdate_encoded = label_encoder.fit_transform(prevdate[:num_train])
prevadults_encoded = label_encoder.fit_transform(prevadults[:num_train])
prevbudget_encoded = label_encoder.fit_transform(prevbudget[:num_train])
previntent_encoded = label_encoder.fit_transform(previntent[:num_train])


origin_encoded = label_encoder.fit_transform(origin[:num_train])
dest_encoded = label_encoder.fit_transform(dest[:num_train])
adults_encoded = label_encoder.fit_transform(adults[:num_train])
budget_encoded = label_encoder.fit_transform(budget[:num_train])
date_encoded = label_encoder.fit_transform(date[:num_train])
intent_encoded=label_encoder.fit_transform(intent[:num_train])

dat_train1=np.stack([intent_encoded,prevorigin_encoded,prevdest_encoded,prevdate_encoded, prevadults_encoded, 
  prevbudget_encoded,origin_encoded, dest_encoded, adults_encoded, budget_encoded, date_encoded], axis=1)

parameters= {'activation':( 'tanh', 'relu', 'logistic'),
'hidden_layer_sizes':[ (5,5), (10,10), (5,5,5), (10,10,10)],'solver':["sgd", 'lbfgs', 'adam']
}
clfsearch = GridSearchCV(estimator=MLPClassifier(), param_grid=parameters, scoring='accuracy', n_jobs=-1)
#find the best hyperparameters
clfsearch.fit(dat_train1, label_train_array)
print ('best cv', clfsearch.cv_results_)
print ('Best score for data', clfsearch.best_score_)
print ('Best model', clfsearch.best_estimator_)
