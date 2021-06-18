from flask.templating import render_template
from flask import Flask,render_template,request
import re
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
        word = re.sub("^[\u0610]+$", "",word) #ARABIC SIGN SALLALLAHOU ALAYHE WA SALLAM
        word =  re.sub("^[\u0611]+$", "",word)#ARABIC SIGN ALAYHE ASSALLAM
        word =  re.sub("^[\u0612]+$", "",word)#ARABIC SIGN RAHMATULLAH ALAYHE
        word =  re.sub("^[\u0613]+$", "",word)#ARABIC SIGN RADI ALLAHOU ANHU
        word =  re.sub("^[\u0614]+$", "",word)#ARABIC SIGN TAKHALLUS
        #Remove koranic anotation
        word =  re.sub("^[\u0615]+$", "",word)#ARABIC SMALL HIGH TAH
        word =  re.sub("^[\u0616]+$", "",word)#ARABIC SMALL HIGH LIGATURE ALEF WITH LAM WITH YEH
        word =  re.sub("^[\u0617]+$", "",word)#ARABIC SMALL HIGH ZAIN
        word =  re.sub("^[\u0618]+$", "",word)#ARABIC SMALL FATHA
        word =  re.sub("^[\u0619]+$", "",word)#ARABIC SMALL DAMMA
        word =  re.sub("^[\u061A]+$", "",word)#ARABIC SMALL KASRA
        word =  re.sub("^[\u06D6]+$", "",word)#ARABIC SMALL HIGH LIGATURE SAD WITH LAM WITH ALEF MAKSURA
        word =  re.sub("^[\u06D7]+$", "",word)#ARABIC SMALL HIGH LIGATURE QAF WITH LAM WITH ALEF MAKSURA
        word =  re.sub("^[\u06D8]+$", "",word)#ARABIC SMALL HIGH MEEM INITIAL FORM
        word =  re.sub("^[\u06D9]+$", "",word)#ARABIC SMALL HIGH LAM ALEF
        word =  re.sub("^[\u06DA]+$", "",word)#ARABIC SMALL HIGH JEEM
        word =  re.sub("^[\u06DB]+$", "",word)#ARABIC SMALL HIGH THREE DOTS
        word =  re.sub("^[\u06DC]+$", "",word)#ARABIC SMALL HIGH SEEN
        word =  re.sub("^[\u06DD]+$", "",word)#ARABIC END OF AYAH
        word =  re.sub("^[\u06DE]+$", "",word)#ARABIC START OF RUB EL HIZB
        word =  re.sub("^[\u06DF]+$", "",word)#ARABIC SMALL HIGH ROUNDED ZERO
        word =  re.sub("^[\u06E0]+$", "",word)#ARABIC SMALL HIGH UPRIGHT RECTANGULAR ZERO
        word =  re.sub("^[\u06E1]+$", "",word)#ARABIC SMALL HIGH DOTLESS HEAD OF KHAH
        word =  re.sub("^[\u06E2]+$", "",word)#ARABIC SMALL HIGH MEEM ISOLATED FORM
        word =  re.sub("^[\u06E3]+$", "",word)#ARABIC SMALL LOW SEEN
        word =  re.sub("^[\u06E4]+$", "",word)#ARABIC SMALL HIGH MADDA
        word =  re.sub("^[\u06E5]+$", "",word)#ARABIC SMALL WAW
        word =  re.sub("^[\u06E6]+$", "",word)#ARABIC SMALL YEH
        word =  re.sub("^[\u06E7]+$", "",word)#ARABIC SMALL HIGH YEH
        word =  re.sub("^[\u06E8]+$", "",word)#ARABIC SMALL HIGH NOON
        word =  re.sub("^[\u06E9]+$", "",word)#ARABIC PLACE OF SAJDAH
        word =  re.sub("^[\u06EA]+$", "",word)#ARABIC EMPTY CENTRE LOW STOP
        word =  re.sub("^[\u06EB]+$", "",word)#ARABIC EMPTY CENTRE HIGH STOP
        word =  re.sub("^[\u06EC]+$", "",word)#ARABIC ROUNDED HIGH STOP WITH FILLED CENTRE
        word =  re.sub("^[\u06ED]+$", "",word)#ARABIC SMALL LOW MEEM
        #Remove tatweel
        word =  re.sub("^[\u0640]+$", "",word)
        #Remove tashkeel
        word =  re.sub("^[\u064B]+$", "",word)#ARABIC FATHATAN
        word =  re.sub("^[\u064C]+$", "",word)#ARABIC DAMMATAN
        word =  re.sub("^[\u064D]+$", "",word)#ARABIC KASRATAN
        word =  re.sub("^[\u064E]+$", "",word)#ARABIC FATHA
        word =  re.sub("^[\u064F]+$", "",word)#ARABIC DAMMA
        word =  re.sub("^[\u0650]+$", "",word)#ARABIC KASRA
        word =  re.sub("^[\u0651]+$", "",word)#ARABIC SHADDA
        word =  re.sub("^[\u0652]+$", "",word)#ARABIC SUKUN
        word =  re.sub("^[\u0653]+$", "",word)#ARABIC MADDAH ABOVE
        word =  re.sub("^[\u0654]+$", "",word)#ARABIC HAMZA ABOVE
        word =  re.sub("^[\u0655]+$", "",word)#ARABIC HAMZA BELOW
        word =  re.sub("^[\u0656]+$", "",word)#ARABIC SUBSC^[RIPT A]+$LEF
        word =  re.sub("^[\u0657]+$", "",word)#ARABIC INVERTED DAMMA
        word =  re.sub("^[\u0658]+$", "",word)#ARABIC MARK NOON GHUNNA
        word =  re.sub("^[\u0659]+$", "",word)#ARABIC ZWARAKAY
        word =  re.sub("^[\u065A]+$", "",word)#ARABIC VOWEL SIGN SMALL V ABOVE
        word =  re.sub("^[\u065B]+$", "",word)#ARABIC VOWEL SIGN INVERTED SMALL V ABOVE
        word =  re.sub("^[\u065C]+$", "",word)#ARABIC VOWEL SIGN DOT BELOW
        word =  re.sub("^[\u065D]+$", "",word)#ARABIC REVERSED DAMMA
        word =  re.sub("^[\u065E]+$", "",word)#ARABIC FATHA WITH TWO DOTS
        word =  re.sub("^[\u065F]+$", "",word)#ARABIC WAVY HAMZA BELOW
        word =  re.sub("^[\u0670]+$", "",word)#ARABIC LETTER SUPERSCRIPT ALEF
        word =  word.replace("ى", "ي")
        word =  word.replace("ؤ", "ء")
        word =  word.replace("ئ", "ء")
        word =  word.replace("ة", "ه")
        word =  word.replace("گ", "ك")
        word = word.replace('ال','')
        return  word
if __name__ == '__main__':
    app.run('0.0.0.0')
