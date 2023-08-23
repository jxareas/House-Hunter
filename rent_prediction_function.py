# -*- coding: utf-8 -*-
"""
Created on Wed Aug 12 17:09:04 2020

@author: bdaet
"""
import pickle
import numpy as np

#example for debugging
#example = [1,1,625,0,1,1,0,1,0,0,1,0,0,0,1,1,1,0,1,1,0,0,0,0,1,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,1]

def load_models():
    file_name = 'rent_estimator_model.p'
    with open(file_name, 'rb') as pickled:
        data = pickle.load(pickled)
        model = data['model']
    return model  

def predict_rent(x):
    #take natural log of third value on input list (square footage)
    x[2] = np.log(x[2])
    #reshape input
    x = np.array(x).reshape(1,-1)
    
    # load model
    model = load_models()
    prediction = np.round(np.exp(model.predict(x)))
    return prediction
    
#test for debugging
#print(predict_rent(example))

