#importing dependencies
from sklearn.naive_bayes import MultinomialNB
from sklearn.feature_extraction.text import TfidfVectorizer
import pickle

class SentimentClassifierModel(object):

    def __init__(self):
        self.classifier = MultinomialNB()
        self.vectorizer = TfidfVectorizer()

    def fit_vectorizer(self, x):
        #fit tfidf to corpus
        self.vectorizer.fit(x)

    def transform_vectorizer(self,x):
        #transform corpus to vector matrix (sparse tfidf matx)
        transform_x = self.vectorizer.transform(x)
        return transform_x

    def train(self, x, y):
        #trains the text classifier to associate target labels(sentiment scores) with matrix labels
        self.classifier.fit(x,y)

    def predict_proba(self,x):
        #returns conditional probability of class y (target) wrt x for bin class 1
        proba_y = self.classifier.predict_proba(x)
        return proba_y[:,1]

    def predict_sentiment(self,x):
        y_pred = self.classifier.predict(x)
        return y_pred

    def pickle_tfidfvec(self, path = 'lib/models/tfidf_vectorizer.pkl'):
        with open(path, 'wb') as f:
            pickle.dump(self.vectorizer, f)
            print("Pickled tfidf-vectorizer at {}".format(path))

    def pickle_classifier(self, path ='lib/models/SentimentClassifier.pkl'):
        with open(path, 'wb') as f:
            pickle.dump(self.classifier, f)
            print("Pickled classifier at {}".format(path))

