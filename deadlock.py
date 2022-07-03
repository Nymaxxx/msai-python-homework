#!/usr/bin/env python
# coding: utf-8

# In[5]:


# lets deadlock thread by waiting on itself
from threading import Thread, Lock
 
def task(lock):
    with lock:
        with lock:
            pass

lock = Lock()

thread = Thread(target = task, args = (lock, ))
thread.start()
thread.join()


# In[ ]:




