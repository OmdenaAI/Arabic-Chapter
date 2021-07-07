# Arabic-Chapter Task 8: Word Embedding

<h2>Pre-trained models</h2>

<ol>

<li>Aravec</li>
Wrapper to list, download, and load AraVec models.

<li>Mottagah <br />
Two unigram models, trained for 5 epochs with different min_counts
<br /><br />

Note: These are wordvector models. They have half the size of full models but miss <a href="https://radimrehurek.com/gensim/models/word2vec.html#usage-examples">some features</a>
<br />

<ol>

<li> 
&nbsp; 
<a href="https://drive.google.com/file/d/1EE9cpNUND5SSlQK9PZbYqz-Ux7eitJH9">mottagah_wv</a> 
&nbsp; Vocab size: 112164 </li>

<li> 
&nbsp;
<a href="https://drive.google.com/file/d/1oT8XW02IjMEuJRqYscSVrQTPi-f8pf8M">mottagah_large_wv</a> 
&nbsp; Vocab size: 571460 </li>

</ol>
<br />
Data used for training: (5.4GB .txt)

<ol>
<li>ArCOV (~2.5Million tweets) (605 MBs)</li>
<li>Arabic Wikipedia dump (2.9 GBs)</li>
<li>Egyptian Arabic Wikipedia dump (1.5 GBs)</li>
<li>Various sources (325 MBs)</li>

</ol>
</li>
</ol>

<h2>Implementations</h2>
<ol>
<li>Keras Word2Vec</li>
<li>Keras GloVe</li>
<li>Keras FastText</li>

</ol>

<h2>Usage</h2>

<p>Check Embedding_Demo.ipynb</p>

<h2>References</h2>
<a href="https://arxiv.org/abs/2004.05861">ArCOV</a><br />
<a href="https://github.com/bakrianoo/aravec">AraVec</a> <br />
<a href="https://github.com/ozgurdemir/word2vec-keras">Keras Word2Vec</a> <br />
<a href="https://github.com/erwtokritos/keras-glove">Keras GloVe</a> <br />
<a href="https://www.kaggle.com/allank/simple-keras-fasttext-with-increased-training-data
">Keras FastText</a> <br />
<a href="https://www.kaggle.com/jeffd23/visualizing-word-vectors-with-t-sne
">Plotting with TSNE</a> <br />
<a href="http://download.tensorflow.org/data/questions-words.txt
">Google Word Analogy Dataset</a> <br />
<a href="https://www.researchgate.net/publication/249313626_Arabic_Word_Semantic_Similarity
">Semantic Similarity Dataset</a> <br />
<a href="https://www.researchgate.net/publication/346052809_Comparative_study_of_Arabic_Word_Embeddings_Evaluation_and_Application
">Concept Categorization</a> <br />
<a href="https://www.kaggle.com/mksaad/arabic-sentiment-twitter-corpus
">Twitter Sentiment Analysis Dataset</a> <br />
