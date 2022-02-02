from flask import Flask
from flask_restful import reqparse, abort, Api, Resource
import pickle
import numpy as np
from model import SentimentClassifierModel

app = Flask(__name__)
api = Api(app)

model = SentimentClassifierModel()

classifier_path = 'lib/models/SentimentClassifier.pkl'
with open(classifier_path, 'rb') as f:
    model.classifier = pickle.load(f)

vectorizer_path = 'lib/models/tfidf_vectorizer.pkl'
with open(vectorizer_path, 'rb') as f:
    model.vectorizer = pickle.load(f)

#parse args
parser = reqparse.RequestParser()
parser.add_argument('query')

class PredictUserSentiments(Resource):
    def get(self):
        args = parser.parse_args()
        user_query  = args['query']

        vectorize_userq = model.transform_vectorizer(np.array([user_query]))
        prediction = model.predict_sentiment(vectorize_userq)
        predict_probability = model.predict_proba(vectorize_userq)

        if prediction == 0:
            predicted_sentiment = 'Negative'
        else:
            predicted_sentiment = 'Positive'

        #confidence level
        c_level = round(predict_probability[0], 3)

        #json obj 
        output_as_json = {'sentiment': predicted_sentiment, 'confidence': c_level}

        return output_as_json

#add resource routes
api.add_resource(PredictUserSentiments, '/')

#run app
if __name__ == '__main__':
    app.run(debug=True)
