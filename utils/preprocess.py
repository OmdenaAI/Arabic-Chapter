import re
from tqdm import tqdm

# def tokenizer(
#     texts:list,
#     punctuations = """'!"#$%&'()*+,«».؛،/:؟?@[\]^_`{|}~""",
#     stop_words=['and', 'a', 'is', 'the', 'in', 'be', 'will']
#     )->list:

#     list_ = []
#     maxlen = 0
#     for i in range(len(texts)):
#         maxlen = len(texts[i]) if len(texts[i]) > maxlen else maxlen
#         for x in texts[i]: 
#             if x not in punctuations: 
#                 texts[i] = texts[i].replace(x, " ")
#             # if x == 'و':
#             #     texts[i] = texts[i].replace(x, " و ")

#         texts[i] = re.sub(r'\w*\d\w*', '', texts[i])

#         texts[i] = re.sub(r'[0-9]+', '', texts[i])

#         texts[i] = re.sub(r'\s+', ' ', texts[i]).strip()

#         texts[i] = texts[i].split(' ')

#         texts[i] = [x for x in texts[i] if x!='']

#         texts[i] = [x for x in texts[i] if x not in stop_words]
#         list_.append(texts[i])

#     return list_, maxlen

def tokenizer(
    texts:list,
    punctuations=[],
    stop_words=[],
    )->list:

    list_ = []
    maxlen = 0
    vocab = 0
    for i in tqdm(range(len(texts)), total=len(texts)):
        texts[i] = texts[i].lower()
        for x in texts[i]:
           if x in punctuations:
               texts[i] = texts[i].replace(x, " ")

        texts[i] = re.sub(r'<.*?>', '', texts[i])
        texts[i] = re.sub(r'\w*\d\w*', '', texts[i])
        texts[i] = re.sub(r'[0-9]+', '', texts[i])
        texts[i] = re.sub(r'\s+', ' ', texts[i]).strip()

        texts[i] = texts[i].split(' ')
        texts[i] = [x for x in texts[i] if x!='']
        texts[i] = [x for x in texts[i] if x not in punctuations]
        texts[i] = [x for x in texts[i] if x not in stop_words]
        list_.append(texts[i])

        maxlen = len(texts[i]) if len(texts[i]) > maxlen else maxlen
        for i in texts[i]:
            vocab += 1
                
    return list_, maxlen, vocab