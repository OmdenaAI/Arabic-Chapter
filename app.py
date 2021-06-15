from flask.templating import render_template
from flask import Flask,render_template,request

app  = Flask(__name__)

@app.route('/',methods=['GET','POST'])
def home():
        wordlist  = []
        if request.method == 'POST':
                for word in request.form['inp'].split():
                        temp = normalize(word.strip())
                        if len(temp) < 3:
                                wordlist.append(word)
                        else:
                                wordlist.append(temp)
                return render_template('index.html',words = wordlist)
        else:
                return render_template('index.html')


def normalize(word):
        #Remove honorific sign
        word = word.replace('"','')
        word =  word.replace("(", "")
        word =  word.replace(")", "")
        word = word.replace('؟','')
        word = word.replace('!','')
        word = word.replace('.','')
        word = word.replace("\u0610", "") #ARABIC SIGN SALLALLAHOU ALAYHE WA SALLAM
        word =  word.replace("\u0611", "")#ARABIC SIGN ALAYHE ASSALLAM
        word =  word.replace("\u0612", "")#ARABIC SIGN RAHMATULLAH ALAYHE
        word =  word.replace("\u0613", "")#ARABIC SIGN RADI ALLAHOU ANHU
        word =  word.replace("\u0614", "")#ARABIC SIGN TAKHALLUS
        #Remove koranic anotation
        word =  word.replace("\u0615", "")#ARABIC SMALL HIGH TAH
        word =  word.replace("\u0616", "")#ARABIC SMALL HIGH LIGATURE ALEF WITH LAM WITH YEH
        word =  word.replace("\u0617", "")#ARABIC SMALL HIGH ZAIN
        word =  word.replace("\u0618", "")#ARABIC SMALL FATHA
        word =  word.replace("\u0619", "")#ARABIC SMALL DAMMA
        word =  word.replace("\u061A", "")#ARABIC SMALL KASRA
        word =  word.replace("\u06D6", "")#ARABIC SMALL HIGH LIGATURE SAD WITH LAM WITH ALEF MAKSURA
        word =  word.replace("\u06D7", "")#ARABIC SMALL HIGH LIGATURE QAF WITH LAM WITH ALEF MAKSURA
        word =  word.replace("\u06D8", "")#ARABIC SMALL HIGH MEEM INITIAL FORM
        word =  word.replace("\u06D9", "")#ARABIC SMALL HIGH LAM ALEF
        word =  word.replace("\u06DA", "")#ARABIC SMALL HIGH JEEM
        word =  word.replace("\u06DB", "")#ARABIC SMALL HIGH THREE DOTS
        word =  word.replace("\u06DC", "")#ARABIC SMALL HIGH SEEN
        word =  word.replace("\u06DD", "")#ARABIC END OF AYAH
        word =  word.replace("\u06DE", "")#ARABIC START OF RUB EL HIZB
        word =  word.replace("\u06DF", "")#ARABIC SMALL HIGH ROUNDED ZERO
        word =  word.replace("\u06E0", "")#ARABIC SMALL HIGH UPRIGHT RECTANGULAR ZERO
        word =  word.replace("\u06E1", "")#ARABIC SMALL HIGH DOTLESS HEAD OF KHAH
        word =  word.replace("\u06E2", "")#ARABIC SMALL HIGH MEEM ISOLATED FORM
        word =  word.replace("\u06E3", "")#ARABIC SMALL LOW SEEN
        word =  word.replace("\u06E4", "")#ARABIC SMALL HIGH MADDA
        word =  word.replace("\u06E5", "")#ARABIC SMALL WAW
        word =  word.replace("\u06E6", "")#ARABIC SMALL YEH
        word =  word.replace("\u06E7", "")#ARABIC SMALL HIGH YEH
        word =  word.replace("\u06E8", "")#ARABIC SMALL HIGH NOON
        word =  word.replace("\u06E9", "")#ARABIC PLACE OF SAJDAH
        word =  word.replace("\u06EA", "")#ARABIC EMPTY CENTRE LOW STOP
        word =  word.replace("\u06EB", "")#ARABIC EMPTY CENTRE HIGH STOP
        word =  word.replace("\u06EC", "")#ARABIC ROUNDED HIGH STOP WITH FILLED CENTRE
        word =  word.replace("\u06ED", "")#ARABIC SMALL LOW MEEM
        #Remove tatweel
        word =  word.replace("\u0640", "")
        #Remove tashkeel
        word =  word.replace("\u064B", "")#ARABIC FATHATAN
        word =  word.replace("\u064C", "")#ARABIC DAMMATAN
        word =  word.replace("\u064D", "")#ARABIC KASRATAN
        word =  word.replace("\u064E", "")#ARABIC FATHA
        word =  word.replace("\u064F", "")#ARABIC DAMMA
        word =  word.replace("\u0650", "")#ARABIC KASRA
        word =  word.replace("\u0651", "")#ARABIC SHADDA
        word =  word.replace("\u0652", "")#ARABIC SUKUN
        word =  word.replace("\u0653", "")#ARABIC MADDAH ABOVE
        word =  word.replace("\u0654", "")#ARABIC HAMZA ABOVE
        word =  word.replace("\u0655", "")#ARABIC HAMZA BELOW
        word =  word.replace("\u0656", "")#ARABIC SUBSCRIPT ALEF
        word =  word.replace("\u0657", "")#ARABIC INVERTED DAMMA
        word =  word.replace("\u0658", "")#ARABIC MARK NOON GHUNNA
        word =  word.replace("\u0659", "")#ARABIC ZWARAKAY
        word =  word.replace("\u065A", "")#ARABIC VOWEL SIGN SMALL V ABOVE
        word =  word.replace("\u065B", "")#ARABIC VOWEL SIGN INVERTED SMALL V ABOVE
        word =  word.replace("\u065C", "")#ARABIC VOWEL SIGN DOT BELOW
        word =  word.replace("\u065D", "")#ARABIC REVERSED DAMMA
        word =  word.replace("\u065E", "")#ARABIC FATHA WITH TWO DOTS
        word =  word.replace("\u065F", "")#ARABIC WAVY HAMZA BELOW
        word =  word.replace("\u0670", "")#ARABIC LETTER SUPERSCRIPT ALEF
        word =  word.replace("ى", "ي")
        word =  word.replace("ؤ", "ء")
        word =  word.replace("ئ", "ء")
        word =  word.replace("ة", "ه")
        word =  word.replace("گ", "ك")
        word = word.replace('ال','')
        return  word
if __name__ == '__main__':
    app.run('0.0.0.0')
