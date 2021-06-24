# Arabic-Chapter

### Tokenizer class usage
```python
import tokenizer
from tokenizer import tokenization

text= open('test1.txt',encoding = "utf-8").read()

tk=tokenization(text)

#Acessing tokens  

tk.tokens #returns a list of lists of tokens based on sentences

tk.flat_tokens # returns a single list of tokens

#Acessing sentences 

tk.sentences
```
