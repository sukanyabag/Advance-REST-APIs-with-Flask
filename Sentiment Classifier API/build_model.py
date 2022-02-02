from model import SentimentClassifierModel
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split


def build_model():
    model = SentimentClassifierModel()

    with open('D:/Projects/REST APIs Flask/NLP Sentiment Classifier API/lib/data/train.tsv') as f:
        data = pd.read_csv(f, sep='\t')
        data = data.replace(to_replace = 'None', value = np.nan).dropna()

    positive_negative = data[(data['Sentiment'] == 0) | (data['Sentiment'] == 4)]

    positive_negative['Binary'] = positive_negative.apply(lambda x : 0 if x['Sentiment'] == 0 else 1, axis=1)

    model.fit_vectorizer(positive_negative.loc[:,'Phrase'])
    
    x = model.transform_vectorizer(positive_negative.loc[:,'Phrase'])
    y = positive_negative.loc[:, 'Binary']

    x_train, x_test, y_train, y_test = train_test_split(x,y)

    model.train(x_train, y_train)
    print("Model trained successfully!")

    model.pickle_classifier()
    model.pickle_tfidfvec()

if __name__ == "__main__":
    build_model()
