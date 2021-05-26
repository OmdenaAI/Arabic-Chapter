#!/usr/bin/python


import os, sys
from data.ar_stopwords import ar_stopwords
from data.stopwordsallforms import STOPWORDS
from stop_words import remove_stopwords, add_stopword

text = u"تعدّ كتابة المقالات الأكاديمية واحدة من أهمّ عناصر النجاح خلال المرحلة الدراسية، الثانوية أو الجامعية على حدّ السواء. ويواجه الكثير من الطلاب الذين يفتقرون إلى موهبة الكتابة، صعوبة في إعداد المقالات الأكاديمية وتجهيزها. لكن، ما لا يعرفه هؤلاء الطلاب، هو أن المقال الأكاديمي، يختلف اختلافًا كبيرًا عن الكتابة الإبداعية، حيث أنّه مبني على قواعد محدّدة إن تعلّمتها والتزمت بها أمكنك كتابة مقال أكاديمي احترافي وناجح تصفح على موقع فرصة"


print("test string:",text,"\n string length:",len(text))
print()
print()


print('Testing ar_stopwords')
lst=[]
for token in text.split():
    if token not in ar_stopwords:    
        lst.append(token)
print('resulting tokens:', lst,'list length:',len(lst))
print("-"*40)
print()
print()



print('Testing stopwordsallforms')
result_list = []
for token in text.split():
    if token not in STOPWORDS.keys():
        result_list.append(token)
print('resulting tokens:', result_list,'list length:',len(result_list))
print("-"*40)
print()
print()


print("Difference between lists =",list(set(lst)- set(result_list)))
print("-"*40)
print()
print()


print('Result from running general remove function')
print(remove_stopwords(text, sw_src = "stopwords"))
print(len(remove_stopwords(text, sw_src = "ar_stopwords")))
print("-"*40)
print()
print()

print("testing adding new stopword")
new_stopword = 'فرصة'
print(new_stopword in STOPWORDS)    #False
print(new_stopword in ar_stopwords) #False

add_stopword(new_stopword)
print(new_stopword in STOPWORDS)     #True
print(new_stopword in ar_stopwords)  #False

add_stopword(new_stopword, to = "ar_stopwords")
print(new_stopword in STOPWORDS)     #True
print(new_stopword in ar_stopwords)  #True
