#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun May 23 19:03:10 2021

@author: ehab
"""
from nltk.metrics import *

import qalsadi.lemmatizer


#this function is to get output lemmatizer 
def input_data(filename):
    #open the file
    file=open(filename)
    text=file.read()
    
    lemmer=qalsadi.lemmatizer.Lemmatizer()
    lemmas=lemmer.lemmatize_text(text)
    return lemmas
        

#calculate the accuracy
def test_acc(test_file,lemmas):
    #file=open(test_file)
    test=[]
    with open(test_file,'r') as file:
        test=[current_place.rstrip() for current_place in file.readlines()]
        
    reference=lemmas  
    
    a=accuracy(reference,test)
    return(a*100)

  ########------test--------------##  
#filename= "/home/ehab/Desktop/data.txt"
#test_file="/home/ehab/Desktop/test_data.txt"
#lemmas=input_data(filename)
#print(lemmas)
#print(test_acc(test_file,lemmas))

