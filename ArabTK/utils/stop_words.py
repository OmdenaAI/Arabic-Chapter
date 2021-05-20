import joblib
import glob
import arabicstopwords.arabicstopwords as stp


def generate():
    words = set()
    for files in glob.glob("data\Stop_words\*.txt"):
        file = open(files, 'r', encoding='utf8')
        for i in file:
            words.add(i)
        file.close()

    joblib.dump(words, "data\Stop_words\stopWords.pkl")


def remove_stop_words(text):
    generate()
    Swords = joblib.load("data\Stop_words\stopWords.pkl")
    words = [x for x in text if x not in Swords]
    words = [x for x in words if not stp.is_stop(x)]
    return words
