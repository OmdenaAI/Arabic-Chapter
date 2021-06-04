#!/usr/bin/python


import os, sys
from data.ar_stopwords import ar_stopwords
from data.stopwordsallforms import STOPWORDS
from stop_words import stopwords

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
print(stopwords.remove_stopwords(text, sw_src = "stopwords_long"))
print(len(stopwords.remove_stopwords(text, sw_src = "stopwords_short")))
print("-"*40)
print()
print()

print("testing adding new stopword")
new_stopword = 'فرصة'
print(stopwords.is_stop_word(new_stopword,sw_src = 'stopwords_long'))   #False
print(stopwords.is_stop_word(new_stopword,sw_src = 'stopwords_long'))   #False

stopwords.add_stopword(new_stopword,to='stopwords_long')
print(stopwords.is_stop_word(new_stopword,sw_src = 'stopwords_long'))   #True
print(stopwords.is_stop_word(new_stopword,sw_src = 'stopwords_short'))  #False


stopwords.add_stopword(new_stopword,to='stopwords_short')
print(stopwords.is_stop_word(new_stopword,sw_src = 'stopwords_long')) #True
print(stopwords.is_stop_word(new_stopword,sw_src = 'stopwords_short')) #True
