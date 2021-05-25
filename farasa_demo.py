import requests,json

from requests.models import encode_multipart_formdata

url = 'https://farasa.qcri.org/analyze/'
myobj = {'text': 'ذهب الولد الى المدرسة','task':"lemmatization","API_KEY":"lpcsTkDIDf"}

x = requests.post(url, data = myobj)
with open('./result.txt','w+',encoding='utf-8') as f:
    f.writelines(json.loads(x.text)['text'])