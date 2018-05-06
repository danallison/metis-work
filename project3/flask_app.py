from flask import Flask, request
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
def hello():
    with sql_engine.connect() as connection:
        id, key, val = connection.execute(
            'select * from foo limit 1'
        ).fetchone()
    return '<h1>Hi, World!</h1><p>{}:{}:{}</p>'.format(id, key, val)

@app.route('/predict')
def predict():
    url = request.args.get('url')
    if not url: return 'Must supply a valid URL'
    features = project3utils.get_numeric_features_list_from_url(url)
    return str(model.predict_proba([features])[0][1])
