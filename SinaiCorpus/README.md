# Sinai Corpus
*Sinai Corpus* is a clean **Arabic language tagged corpus** made up of texts collected from  various arabic websites with more than 14m+ words and 300k+ tagged sentences.

## Corpus format
All tagged sentences follow the format below:
> ka*`lika:ADV &nbsp;&nbsp; yuso>al:IV3MS+/VERB_IMPERFECT &nbsp;&nbsp; Ean:PREP &nbsp;&nbsp; maEonaY:NOUN &nbsp;&nbsp; AlfiEol:DET+/NOUN 

Equivalent to (POS separated by colon `:`)
> كَذٰلِكَ يُسْأَل عَن مَعْنَى الفِعْل


### Basic information
&nbsp;| Frequency 
--- | --- 
Words | 14,904,000 
Sentences | 348,800 
Web pages | 362

### Notes
- *Sinai Corpus* is analyzed, and processed by [Arabycia](https://github.com/mohabmes/Arabycia).
- See [sample.txt](https://github.com/mohabmes/Sinai-corpus/blob/master/src/sample.txt) for more examples (corpus format).
- Use [load.py](https://github.com/mohabmes/Sinai-corpus/blob/master/load.py) to load all corpus content.

# License
[MIT License](https://github.com/mohabmes/Sinai-corpus/blob/master/LICENSE) Copyright (c) 2020 mohabmes
