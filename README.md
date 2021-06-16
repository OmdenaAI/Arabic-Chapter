# Arabic-Chapter

### Tokenizer class usage
```python
import tokenizer
from tokenizer import tokenization

text= open('test1.txt',encoding = "utf-8").read()

tk=tokenization(text)

#Acessing tokens 

tk.tokens


#Acessing sentences 

tk.sentences
```
