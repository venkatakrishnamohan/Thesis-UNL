import numpy as np
import pandas as pd
import gensim
import os
from gensim.models.keyedvectors import KeyedVectors
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.naive_bayes import MultinomialNB
from sklearn.model_selection import cross_val_score
import sklearn.preprocessing as sk
from sklearn.preprocessing import scale
from sklearn import svm 
from sklearn.ensemble import BaggingClassifier
from sklearn import model_selection
from sklearn.ensemble import ExtraTreesClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.ensemble import AdaBoostClassifier
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.ensemble import VotingClassifier
from xgboost import XGBClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.model_selection import GridSearchCV
df = pd.read_csv('classification_data.csv')
df['categorical_id'] = ''
df.categorical_id = pd.Categorical(df.Category)
df.categorical_id = df.categorical_id.cat.codes
features_scaled = np.load('classification_features.npy')
labels = df.categorical_id

ex_trees = GradientBoostingClassifier(ExtraTreesClassifier(n_estimators=100,max_features=7),n_estimators=100, random_state=2018)
knn = GradientBoostingClassifier(KNeighborsClassifier(n_neighbors=5),n_estimators=100, random_state=2018)
lr = GradientBoostingClassifier(LogisticRegression(C=2.0,random_state=0),n_estimators=100, random_state=2018)
eclf = VotingClassifier(estimators=[('lr', lr), ('trees', ex_trees), ('knn', knn)], voting='hard')

models = [ex_trees, knn, lr, eclf]
CV=10
cv_df = pd.DataFrame(index=range(CV * len(models)))
entries = []
for model in models:
  model_name = model.__class__.__name__
  accuracies = cross_val_score(model, features_scaled, labels, scoring='accuracy', cv=CV)
  for fold_idx, accuracy in enumerate(accuracies):
    entries.append((model_name, fold_idx, accuracy))
cv_df = pd.DataFrame(entries, columns=['model_name', 'fold_idx', 'accuracy'])

cv_df.groupby('model_name').accuracy.mean()