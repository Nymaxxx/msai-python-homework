#!/usr/bin/env python
# coding: utf-8

# In[74]:


import numpy as np
from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.gaussian_process import GaussianProcessClassifier
from sklearn.metrics import accuracy_score


# In[79]:


class Facade:
    def __init__(self, classifiers) -> None:
        self.classifiers = classifiers

    def fit(self, X, y):
        for model in self.classifiers:
            model.fit(X, y)

    def predict(self, X):
        preds = []

        for model in self.classifiers:
            preds.append(model.predict(X))

        pred = np.floor(np.stack(preds).sum(axis=0) / len(self.classifiers))

        return pred


# In[81]:


if __name__ == "__main__":
    data = load_iris(return_X_y = True)
    
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, shuffle=True)

    classifiers = [LogisticRegression(), GaussianProcessClassifier()]

    ensemble = Facade(classifiers)
    ensemble.fit(X_train, y_train)
    predict = ensemble.predict(X_test)
    
    acc = accuracy_score(y_test, predict)

    print(acc)


# In[ ]:


# 0.9666666666666667

