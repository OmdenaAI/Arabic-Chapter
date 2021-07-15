from flask import Flask, jsonify, request
from word_embedding.embedding import WordEmbedding

app = Flask(__name__)
app.config['JSON_SORT_KEYS'] = False


@app.route("/", methods=['GET'])
def root():
    return jsonify({
        'similar words' : "to get similar words use /aravec/similar/ (or word2vec)",
        'analogy': "use /aravec/analogy?text=" " to get analogies (or word2vec)"

    })


@app.route("/aravec/analogy", methods=['GET', 'POST'])
def predict_aravec_analogy():
    text = request.args.get('text')
    em = WordEmbedding(text=text, method="aravec")
    text = em.get_preprocessed_aravec()
    model = em.get_model()
    return em.get_analogy(text, model)

@app.route("/aravec/similar", methods=['GET', 'POST'])
def predict_aravec_similar():
    text = request.args.get('text')
    em = WordEmbedding(text=text, method="aravec")
    text = em.get_preprocessed_aravec()
    model = em.get_model()
    return em.get_similar(text, model)


@app.route("/word2vec/analogy", methods=['GET', 'POST'])
def predict_word2vec_analogy():
    text = request.args.get('text')
    em = WordEmbedding(text=text, method="word2vec")
    text = em.get_preprocessed_word2vec()
    model = em.get_model()
    return em.get_analogy(text, model)

@app.route("/word2vec/similar", methods=['GET', 'POST'])
def predict_word2vec_similar():
    text = request.args.get('text')
    em = WordEmbedding(text=text, method="word2vec")
    text = em.get_preprocessed_word2vec()
    model = em.get_model()
    return em.get_similar(text, model)



if __name__ == '__main__':
    app.run()