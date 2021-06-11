#!/usr/bin/python


import os, sys
#from data.ar_stopwords import ar_stopwords
#from data.stopwordsallforms import STOPWORDS
from stop_words import stopwords

text = u"تعدّ كتابة المقالات الأكاديمية واحدة من أهمّ عناصر النجاح خلال المرحلة الدراسية، الثانوية أو الجامعية على حدّ السواء. ويواجه الكثير من الطلاب الذين يفتقرون إلى موهبة الكتابة، صعوبة في إعداد المقالات الأكاديمية وتجهيزها. لكن، ما لا يعرفه هؤلاء الطلاب، هو أن المقال الأكاديمي، يختلف اختلافًا كبيرًا عن الكتابة الإبداعية، حيث أنّه مبني على قواعد محدّدة إن تعلّمتها والتزمت بها أمكنك كتابة مقال أكاديمي احترافي وناجح تصفح على موقع فرصة"


print("test string:\n",text,"\n string length:",len(text))
print("-"*40)
print()
print()


#print('Testing short-source')
#lst=[]
#for token in text.split():
#    if token not in ar_stopwords:
#        lst.append(token)
#print('resulting tokens:', lst,'list length:',len(lst))
#print("-"*40)
#print()
#print()
#
#
#
#print('Testing long-source')
#result_list = []
#for token in text.split():
#    if token not in STOPWORDS.keys():
#        result_list.append(token)
#print('resulting tokens:', result_list,'list length:',len(result_list))
#print("-"*40)
#print()
#print()
#
#
#print("Difference between lists =",list(set(lst)- set(result_list)))
#print("-"*40)
#print()
#print()


print('Result from running remove function with long stopword source')
print(stopwords.remove_stopwords(text, sw_src = "stopwords_long"))
print('resulting tokens count', len(stopwords.remove_stopwords(text, sw_src = "stopwords_long")))
print("-"*40)
print()
print()

print('Result from running remove function with short stopword source')
print(stopwords.remove_stopwords(text, sw_src = "stopwords_short"))
print('resulting tokens count', len(stopwords.remove_stopwords(text, sw_src = "stopwords_short")))
print("-"*40)
print()
print()

print("testing adding new stopword")
new_stopword = 'فرصة'
print('Is Stopword in long source?:',stopwords.is_stop_word(new_stopword,sw_src = 'stopwords_long'))   #False
print('Is Stopword in short source?:',stopwords.is_stop_word(new_stopword,sw_src = 'stopwords_short'))   #False

print("-"*40)
print()
print()

print('Adding Stopword to long source')
stopwords.add_stopword(new_stopword,to='stopwords_long')
print('Is Stopword in long source?:',stopwords.is_stop_word(new_stopword,sw_src = 'stopwords_long'))   #True
print('Is Stopword in short source?:',stopwords.is_stop_word(new_stopword,sw_src = 'stopwords_short'))  #False

print("-"*40)
print()
print()

print('Adding Stopword to short source')
stopwords.add_stopword(new_stopword,to='stopwords_short')
print('Is Stopword in long source?:',stopwords.is_stop_word(new_stopword,sw_src = 'stopwords_long')) #True
print('Is Stopword in short source?:',stopwords.is_stop_word(new_stopword,sw_src = 'stopwords_short')) #True
