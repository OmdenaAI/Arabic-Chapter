with open('morphology.db','r',encoding="utf-8") as db:
    lines = [i.strip() for i in db.readlines()]
    prefixes = lines[lines.index('###PREFIXES###')+1:lines.index('###SUFFIXES###')]
    with open('prefixes.txt','a',encoding="utf-8") as pr:
        for i in prefixes:
            pr.writelines(i + "\n")
    suffixes = lines[lines.index('###SUFFIXES###')+1:lines.index('###STEMS###')]
    with open('suffixes.txt','a',encoding="utf-8") as suf:
        for i in suffixes:
            suf.writelines(i + "\n")
    stems = lines[lines.index('###STEMS###')+1:lines.index('###TABLE AB###')]
    with open('stems.txt','a',encoding="utf-8") as st:
        for i in stems:
            st.writelines(i + "\n")
    db.close()
