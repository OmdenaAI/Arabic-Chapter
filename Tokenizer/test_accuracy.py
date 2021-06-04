#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jun  2 09:32:33 2021

@author: ehab
"""
import numpy as np
import json
from nltk.metrics import *
import tokenizer
from tokenizer import tokenization




def input_data(filename):
    #open the file
    file=open(filename)
    text=file.read()
    tokenizer=tokenization(text)
    snt=tokenizer.sentences
    tok=tokenizer.tokens
    
    return tok



def test_acc(test_file_tok,tok):
    
    test2=[]
  
        
    with open(test_file_tok,'r') as file:
        test2=[current_place.rstrip() for current_place in file.readlines()]
   
    list(test2)
        
    
    reference2=tok  
    
    
    print(len(reference2[0]))
    print(len(test2[0]))
    print(reference2)
    print(test2)
    
   # a=accuracy(reference1,test1)
    b=accuracy(reference2,test2)
   
    return((b)*100)




 ########------test--------------##
  """
filename= "/home/ehab/Desktop/data.txt" 


test_file_tok="/home/ehab/Desktop/test_data_tok_o.txt"
tok=input_data(filename)
#print("sentence: " ,snt)
print("tokens: ",tok)
print(test_acc(test_file_tok,tok))"""