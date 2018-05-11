from flask import Flask, request, jsonify
from sqlalchemy import create_engine
from sklearn.externals import joblib

import os
import project3utils

app = Flask(__name__)
sql_engine = create_engine('postgresql://{user}:{password}@{host}:{port}/{user}'.format(
    user=os.environ['POSTGRES_USER'],
    password=os.environ['POSTGRES_PASSWORD'],
    host='db', # docker-compose service name
    port='5432'
))
model = joblib.load('model.pkl')

@app.route('/')
def root():
    return app.send_static_file('index.html')

@app.route('/predict')
def predict():
    url = request.args.get('url')
    if not url: return 'Must supply a valid URL'
    features = project3utils.get_features_from_url(url)
    model_input = [[features[c] for c in project3utils.numeric_feature_columns]]
    response = {
        'prediction': model.predict_proba(model_input)[0,1],
        'features': features
    }
    return jsonify(response)
