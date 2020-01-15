#Random forest classifier for the frame switch prediction
import numpy as np
from sklearn.preprocessing import LabelEncoder
from sklearn.preprocessing import OneHotEncoder
import pandas as pd
from sklearn import tree
from sklearn.metrics import classification_report, confusion_matrix 
import time
from sklearn.metrics import accuracy_score
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import roc_curve, auc
import matplotlib.pyplot as plt

#load the structured conversatio data
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

num_train=25071
num_pred=6268

index_pred=num_train+num_pred
label_array=np.array(frameswitched)

# integer encode
label_encoder = LabelEncoder()
prevorigin_encoded = label_encoder.fit_transform(prevorigin)
prevdest_encoded = label_encoder.fit_transform(prevdest)
prevdate_encoded = label_encoder.fit_transform(prevdate)
prevadults_encoded = label_encoder.fit_transform(prevadults)
prevbudget_encoded = label_encoder.fit_transform(prevbudget)
previntent_encoded = label_encoder.fit_transform(previntent)


origin_encoded = label_encoder.fit_transform(origin)
dest_encoded = label_encoder.fit_transform(dest)
adults_encoded = label_encoder.fit_transform(adults)
budget_encoded = label_encoder.fit_transform(budget)
date_encoded = label_encoder.fit_transform(date)
intent_encoded=label_encoder.fit_transform(intent)

dat_train1=np.stack([intent_encoded,prevorigin_encoded,prevdest_encoded, prevadults_encoded, 
  prevbudget_encoded,origin_encoded, dest_encoded, adults_encoded, budget_encoded], axis=1)
clf=RandomForestClassifier(n_estimators=100)

start=time.time()
fit=clf.fit(dat_train1[:num_train,:], label_array[:num_train])
end=time.time()
print(f'Time to train Random Forest model ={end-start} s')

y_pred=fit.predict(dat_train1[num_train:index_pred,:]) 
accuracy=accuracy_score(label_array[num_train:index_pred], y_pred)

print(f'Accuracy={accuracy}')
print(confusion_matrix(label_array[num_train:index_pred], y_pred))  
print(classification_report(label_array[num_train:index_pred], y_pred))

#calculate the false position, true position and threshold
fpr2, tpr2, threshold = roc_curve(label_array[num_train:index_pred], y_pred)
roc_auc2 = auc(fpr2, tpr2)


# plot the roc and auc curves
plt.figure()
plt.title('Receiver Operating Characteristic')
plt.plot(fpr2, tpr2, label = 'MLP AUC = %0.2f' % roc_auc2)
plt.legend(loc = 'lower right')
plt.plot([0, 1], [0, 1],'r--')
plt.xlim([0, 1])
plt.ylim([0, 1])
plt.ylabel('True Positive Rate')
plt.xlabel('False Positive Rate')
plt.show()