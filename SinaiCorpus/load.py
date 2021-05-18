import os
import io
import zipfile


def load_corpus(path = 'Sinai-corpus.zip', filenum = 50):
    corpus_content = ""
    file_cnt = 0
    with zipfile.ZipFile(path) as z:
        print("loading Sinai-corpus ...")
        for filename in z.namelist():
            if not os.path.isdir(filename) and file_cnt <= filenum:
                with z.open(filename) as zfile:
                    with io.TextIOWrapper(zfile, encoding="utf-8") as file:
                        corpus_content += file.read()
                        file_cnt += 1

    print("loaded Sinai-corpus : {} File(s).".format(filenum))
    return corpus_content
