from camel_tools.morphology.database import MorphologyDB
from camel_tools.morphology.analyzer import Analyzer
db = MorphologyDB.builtin_db()
analyzer = Analyzer(db)
data = ""
# To analyze a word, we can use the analyze() method
with open('out.txt','w',encoding="utf-8") as f:
    out = set()
    with open('data.txt','r',encoding="utf-8") as op:
        data  = op.read()
    for i in data.split(' '):
        analyses = analyzer.analyze(i)
        if len(analyses) > 0:
            f.write(analyses[0]['lex'] + '\n')
