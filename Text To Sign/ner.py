from sklearn.feature_extraction.text import CountVectorizer, TfidfTransformer,TfidfVectorizer
from sklearn.svm import LinearSVC
import pickle
import sys
import numpy as np

filename = 'models/ner_model.sav'
lsvm,vectorizer,tfidf = pickle.load(open(filename, 'rb'))

def ner_recognizer(phrase):
    arr=phrase.split()

    y=[]
    token=[]
    for x in arr:
        x=[x]
        test_str = vectorizer.transform(x)
        test_tfstr = tfidf.transform(test_str)
        test_tfstr.shape
        token.append(x)
        y.append(lsvm.predict(test_tfstr.toarray())[0])



    res = {}
    for key in range(len(token)):
        res[token[key][0]] = y[key]


    return res