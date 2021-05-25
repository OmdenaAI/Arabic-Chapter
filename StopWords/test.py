#!/usr/bin/python

import os, sys
from data.ar_stopwords import ar_stopwords
from data.stopwordsallforms import STOPWORDS
from stop_words import remove_stopwords, add_stopword

text = "تعدّ كتابة المقالات الأكاديمية واحدة من أهمّ عناصر النجاح خلال المرحلة الدراسية، الثانوية أو الجامعية على حدّ السواء. ويواجه الكثير من الطلاب الذين يفتقرون إلى موهبة الكتابة، صعوبة في إعداد المقالات الأكاديمية وتجهيزها. لكن، ما لا يعرفه هؤلاء الطلاب، هو أن المقال الأكاديمي، يختلف اختلافًا كبيرًا عن الكتابة الإبداعية، حيث أنّه مبني على قواعد محدّدة إن تعلّمتها والتزمت بها أمكنك كتابة مقال أكاديمي احترافي وناجح تصفح على موقع فرصة"

print("test string:",text,"\n string length:",len(text))

print('Testing ar_stopwords')
lst=[]
for token in text.split():
    if token not in ar_stopwords:    
        lst.append(token)
print('resulting tokens:', lst,'list length:',len(lst))
print("-"*40)

print('Testing stopwordsallforms')
result_list = []
for token in text.split():
    if token not in STOPWORDS.keys():
        result_list.append(token)
print('resulting tokens:', result_list,'list length:',len(result_list))
print("-"*40)

print("Difference between lists =",list(set(lst)- set(result_list)))
print("-"*40)

print('Result from running general remove function')
print(remove_stopwords(text))

##In progress
##add_stopword('فرصة')
