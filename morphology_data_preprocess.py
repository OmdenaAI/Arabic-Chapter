# with open('morphology.db','r',encoding="utf-8") as db:
#     lines = [i.strip() for i in db.readlines()]
#     prefixes = lines[lines.index('###PREFIXES###')+1:lines.index('###SUFFIXES###')]
#     with open('prefixes.txt','a',encoding="utf-8") as pr:
#         for i in prefixes:
#             pr.writelines(i + "\n")
#     suffixes = lines[lines.index('###SUFFIXES###')+1:lines.index('###STEMS###')]
#     with open('suffixes.txt','a',encoding="utf-8") as suf:
#         for i in suffixes:
#             suf.writelines(i + "\n")
#     stems = lines[lines.index('###STEMS###')+1:lines.index('###TABLE AB###')]
#     with open('stems.txt','a',encoding="utf-8") as st:
#         for i in stems:
#             st.writelines(i + "\n")
#     db.close()
import sqlite3

con = sqlite3.connect('./morphology.db')

# creating cursor
cur = con.cursor()

# reading all table names
table_list = [a for a in cur.execute("SELECT name FROM sqlite_master WHERE type = 'table'")]
# here is you table list
print(table_list)

# Be sure to close the connection
con.close()