# # with open('morphology.db','r',encoding="utf-8") as db:
# #     lines = [i.strip() for i in db.readlines()]
# #     prefixes = lines[lines.index('###PREFIXES###')+1:lines.index('###SUFFIXES###')]
# #     with open('prefixes.txt','a',encoding="utf-8") as pr:
# #         for i in prefixes:
# #             pr.writelines(i + "\n")
# #     suffixes = lines[lines.index('###SUFFIXES###')+1:lines.index('###STEMS###')]
# #     with open('suffixes.txt','a',encoding="utf-8") as suf:
# #         for i in suffixes:
# #             suf.writelines(i + "\n")
# #     stems = lines[lines.index('###STEMS###')+1:lines.index('###TABLE AB###')]
# #     with open('stems.txt','a',encoding="utf-8") as st:
# #         for i in stems:
# #             st.writelines(i + "\n")
# #     db.close()
# import re
# # Splits lemmas on '_' and '-'
# _STRIP_LEX_RE = re.compile('_|-')

# defines = {}
# _defaultKey = 'pos'
# defaults = {}
# order = None
# compute_feats = frozenset()
# tokenizations = set()
# stem_backoffs = {}
# _withAnalysis = True
# prefix_hash = {}
# suffix_hash = {}
# stem_hash = {}

# prefix_cat_hash = {}
# suffix_cat_hash = {}
# lemma_hash = {}

# prefix_stem_compat = {}
# stem_suffix_compat = {}
# prefix_suffix_compat = {}
# stem_prefix_compat = {}
# max_prefix_size = 0
# max_suffix_size = 0

# def strip_lex(lex):
#     return _STRIP_LEX_RE.split(lex)[0]

# def parse_defaults_line_toks(toks):
#         res = {}

#         for tok in toks:
#             subtoks = tok.split(u':')
#             if len(subtoks) < 2:
#                 raise Exception(
#                     'invalid key value pair {} in DEFAULTS'.format(
#                         repr(tok)))

#             feat = subtoks[0]
#             val = ':'.join(subtoks[1:])

#             if val == '*':
#                 res[feat] = None
#             else:
#                 res[feat] = val

#         return res
# def parse_analysis_line_toks(toks):
#         res = {}

#         for tok in toks:
#             if len(tok) == 0:
#                 continue

#             subtoks = tok.split(u':')
#             if len(subtoks) < 2:
#                 raise Exception(
#                     'invalid key value pair {}'.format(repr(tok)))

#             res[subtoks[0]] = u':'.join(subtoks[1:])

#         return res
# def parse_dbfile(fpath):
#         global defines,_defaultKey,defaults,order,compute_feats,tokenizations,stem_backoffs,_withAnalysis \
#         ,prefix_hash,suffix_hash,stem_hash,prefix_cat_hash,suffix_cat_hash,lemma_hash,prefix_stem_compat,stem_suffix_compat \
#         ,prefix_suffix_compat,stem_prefix_compat,max_prefix_size,max_suffix_size
#         with open(fpath, 'r', encoding='utf-8') as dbfile:
#             # Process DEFINES
#             for line in dbfile:
#                 line = line.strip()

#                 if line == '###DEFINES###':
#                     continue

#                 if line == '###DEFAULTS###':
#                     break

#                 toks = line.split(u' ')

#                 # Check if line has the minimum viable format
#                 if len(toks) < 3 or toks[0] != 'DEFINE':
#                     raise Exception(
#                         'invalid DEFINES line {}'.format(repr(line)))

#                 new_define = toks[1]
#                 val_set = set()

#                 # Parse values for defined keyword
#                 for tok in toks[2:]:
#                     subtoks = tok.split(':')

#                     # If it's a malformed entry, ignore it
#                     if len(subtoks) != 2 and subtoks[0] != toks[1]:
#                         raise Exception(
#                             'invalid key value pair {} in DEFINES'.format(
#                                 repr(tok)))

#                     # If it's an open class, we use None instead of a set
#                     if len(toks) == 3 and subtoks[1] == '*open*':
#                         val_set = None
#                         break

#                     val_set.add(subtoks[1])

#                 defines[new_define] = (
#                     list(val_set) if val_set is not None else None)

#             # Process DEFAULTS
#             for line in dbfile:
#                 line = line.strip()

#                 if line == '###ORDER###':
#                     break

#                 toks = line.split(u' ')

#                 if len(toks) < 2 or toks[0] != 'DEFAULT':
#                     raise Exception(
#                         'invalid DEFAULTS line {}'.format(repr(line)))

#                 parsed_default = parse_defaults_line_toks(toks[1:])

#                 if _defaultKey not in parsed_default:
#                     raise Exception(
#                         'DEFAULTS line {} missing {} value'.format(
#                             repr(line), _defaultKey))

#                 dkey = parsed_default[_defaultKey]
#                 defaults[dkey] = parsed_default

#             # Process ORDER
#             for line in dbfile:
#                 line = line.strip()

#                 if line == '###TOKENIZATIONS###':
#                     compute_feats = frozenset(order)
#                     break

#                 toks = line.split(u' ')

#                 if (order is not None and len(toks) < 2 and toks[0] != 'ORDER'):
#                         raise Exception('invalid ORDER line {}'.format(repr(line)))

#                 if toks[1] not in defines:
#                     raise Exception(
#                         'invalid feature {} in ORDER line.'.format(
#                             repr(toks[1])))

#                 order = toks[1:]

#             # Process TOKENIZATIONS
#             for line in dbfile:
#                 line = line.strip()

#                 if line == '###STEMBACKOFF###':
#                     tokenizations = frozenset(tokenizations)
#                     break

#                 toks = line.split(u' ')

#                 if (order is not None and len(toks) < 2 and
#                         toks[0] != 'TOKENIZATION'):
#                     raise Exception(
#                         'invalid TOKENIZATION line {}'.format(repr(line)))

#                 if toks[1] not in defines:
#                     raise Exception(
#                         'invalid feature {} in TOKENIZATION line.'.format(
#                             repr(toks[1])))

#                 tokenizations.update(toks[1:])

#             # Process STEMBACKOFFS
#             for line in dbfile:
#                 line = line.strip()

#                 if line == '###PREFIXES###':
#                     break

#                 toks = line.split(u' ')

#                 if len(toks) < 3 or toks[0] != 'STEMBACKOFF':
#                     raise Exception(
#                         'invalid STEMBACKOFFS line {}'.format(repr(line)))

#                 stem_backoffs[toks[1]] = toks[2:]

#             # Process PREFIXES
#             for line in dbfile:
#                 line = line
#                 parts = line.split(u'\t')

#                 if len(parts) != 3:
#                     if line.strip() == '###SUFFIXES###':
#                         break
#                     raise Exception(
#                         'invalid PREFIXES line {}'.format(repr(line)))

#                 prefix = parts[0].strip()
#                 category = parts[1]
#                 analysis = parse_analysis_line_toks(
#                     parts[2].strip().split(u' '))

#                 if _withAnalysis:
#                     if prefix not in prefix_hash:
#                         prefix_hash[prefix] = []
#                     prefix_hash[prefix].append((category, analysis))

#                 # if _withGeneration:
#                     # FIXME: Make sure analyses for category are unique?
#                     if category not in prefix_cat_hash:
#                         prefix_cat_hash[category] = []
#                     prefix_cat_hash[category].append(analysis)

#             # Process SUFFIXES
#             for line in dbfile:
#                 line = line
#                 parts = line.split(u'\t')

#                 if len(parts) != 3:
#                     if line.strip() == '###STEMS###':
#                         break
#                     raise Exception(
#                         'invalid SUFFIXES line {}'.format(repr(line)))

#                 suffix = parts[0].strip()
#                 category = parts[1]
#                 analysis = parse_analysis_line_toks(
#                     parts[2].strip().split(u' '))

#                 if _withAnalysis:
#                     if suffix not in suffix_hash:
#                         suffix_hash[suffix] = []
#                     suffix_hash[suffix].append((category, analysis))

#                 # if _withGeneration:
#                     # FIXME: Make sure analyses for category are unique?
#                     if category not in suffix_cat_hash:
#                         suffix_cat_hash[category] = []
#                     suffix_cat_hash[category].append(analysis)

#             # Process STEMS
#             for line in dbfile:
#                 line = line.strip()

#                 if line == '###TABLE AB###':
#                     break

#                 parts = line.split(u'\t')

#                 if len(parts) != 3:
#                     raise Exception(
#                         'invalid STEMS line {}'.format(repr(line)))

#                 stem = parts[0]
#                 category = parts[1]
#                 analysis = parse_analysis_line_toks(parts[2].split(u' '))
#                 analysis['lex'] = strip_lex(analysis['lex'])

#                 if _withAnalysis:
#                     if stem not in stem_hash:
#                         stem_hash[stem] = []
#                     stem_hash[stem].append((category, analysis))

#                 # if _withGeneration:
#                     # FIXME: Make sure analyses for category are unique?
#                     lemma_key = analysis['lex']
#                     analysis['stemcat'] = category
#                     if lemma_key not in lemma_hash:
#                         lemma_hash[lemma_key] = []
#                     lemma_hash[lemma_key].append(analysis)

#             # Process prefix_stem compatibility table
#             for line in dbfile:
#                 line = line.strip()

#                 if line == '###TABLE BC###':
#                     break

#                 toks = line.split()

#                 if len(toks) != 2:
#                     raise Exception(
#                         'invalid TABLE AB line {}'.format(repr(line)))

#                 prefix_cat = toks[0]
#                 stem_cat = toks[1]

#                 if _withAnalysis:
#                     if prefix_cat not in prefix_stem_compat:
#                         prefix_stem_compat[prefix_cat] = set()
#                     prefix_stem_compat[prefix_cat].add(stem_cat)

#                 # if _withGeneration:
#                     if stem_cat not in stem_prefix_compat:
#                         stem_prefix_compat[stem_cat] = set()
#                     stem_prefix_compat[stem_cat].add(prefix_cat)

#             # Process stem_suffix compatibility table
#             for line in dbfile:
#                 line = line.strip()

#                 if line == '###TABLE AC###':
#                     break

#                 toks = line.split()

#                 if len(toks) != 2:
#                     raise Exception(
#                         'invalid TABLE BC line {}'.format(repr(line)))

#                 stem_cat = toks[0]
#                 suffix_cat = toks[1]

#                 if stem_cat not in stem_suffix_compat:
#                     stem_suffix_compat[stem_cat] = set()
#                 stem_suffix_compat[stem_cat].add(suffix_cat)

#             # Process prefix_suffix compatibility table
#             for line in dbfile:
#                 line = line.strip()

#                 toks = line.split()

#                 if len(toks) != 2:
#                     raise Exception(
#                         'invalid TABLE AC line {}'.format(repr(line)))

#                 prefix_cat = toks[0]
#                 suffix_cat = toks[1]

#                 if prefix_cat not in prefix_suffix_compat:
#                     prefix_suffix_compat[prefix_cat] = set()
#                 prefix_suffix_compat[prefix_cat].add(suffix_cat)

#             if _withAnalysis:
#                 for prefix in prefix_hash.keys():
#                     max_prefix_size = max(max_prefix_size,
#                                                len(prefix))
#                 for suffix in suffix_hash.keys():
#                     max_suffix_size = max(max_suffix_size,
#                                                len(suffix))
# parse_dbfile("./morphology.db")
# print(defaults)

from camel_tools.morphology.database import MorphologyDB
from camel_tools.morphology.analyzer import Analyzer

db = MorphologyDB(fpath='./morphology.db')

# Create analyzer with no backoff
analyzer = Analyzer(db)


# Create analyzer with NOAN_PROP backoff
analyzer = Analyzer(db, 'NOAN_PROP')

# or
analyzer = Analyzer(db, backoff='NOAN_PROP')


# To analyze a word, we can use the analyze() method
analyses = analyzer.analyze('شارع')