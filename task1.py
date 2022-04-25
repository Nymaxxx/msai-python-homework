#!/usr/bin/env python
# coding: utf-8

# In[18]:


import numpy as np
from sklearn.utils import shuffle
from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error


# In[19]:


class Builder:
    def __init__(self, X_train, y_train):
        self.X_train = X_train
        self.y_train = y_train

    def get_subsample(self, df_share):
        X = self.X_train.copy()
        y = self.y_train.copy()
        
        X, y = shuffle(X, y, random_state=0)
        ids = int(df_share / 100 * len(y))
        
        return X[:ids], y[:ids]


# In[20]:


if __name__ == "__main__":
    X, y = load_iris(return_X_y = True)
    X, y = shuffle(X, y, random_state=0)
    X_train, X_test, y_train, y_test = train_test_split(X, y, train_size=0.8, random_state=0)
    
    pattern_item = Builder(X_train, y_train)
    k = 1
    for df_share in range(10, 101, 10):
        
        curr_X_train, curr_y_train = pattern_item.get_subsample(df_share)
        
        lr = LinearRegression()
        
        lr.fit(curr_X_train, curr_y_train)
        pred = lr.predict(X_test)
        error = mean_squared_error(y_test, pred)
    
        print("Test {}: data = {}%, error = {}".format(k, df_share, error))
        k += 1


# In[21]:


"""
Test 1: data = 10%, error = 0.09866491792492346
Test 2: data = 20%, error = 0.07655448613230681
Test 3: data = 30%, error = 0.06584706557008055
Test 4: data = 40%, error = 0.062156099864419896
Test 5: data = 50%, error = 0.05347078060455472
Test 6: data = 60%, error = 0.05147830656465323
Test 7: data = 70%, error = 0.056680550084404466
Test 8: data = 80%, error = 0.05430192308265776
Test 9: data = 90%, error = 0.053441678026735946
Test 10: data = 100%, error = 0.05513105809164024
"""


# In[ ]:




