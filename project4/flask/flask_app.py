from flask import Flask, request, jsonify
import pickle

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
plt.style.use('seaborn-darkgrid')
plt.rcParams.update({'font.size': 12})

app = Flask(__name__)

with open('nb_model_components.pkl', 'rb') as file:
    components = pickle.load(file)
    count_vectorizer = components['count_vectorizer']
    clf = components['clf']

@app.route('/')
def root():
    return app.send_static_file('index.html')

def generate_prediction_graph(sentence):
    pred = clf.predict_proba(count_vectorizer.transform([sentence]))[0]
    plt.figure(figsize=(16, 4))
    plt.title('"{}"'.format(sentence))
    plt.ylim((0, 1))
    decades = range(1600, 1600 + 10 * len(pred), 10)
    plt.xticks([d for d in decades if ((d / 10) + 1) % 2])
    plt.bar(decades, pred, width=10, align='edge')
    plt.savefig('static/fig.png', format='png')

@app.route('/predict')
def predict():
    text = request.args.get('text')
    generate_prediction_graph(text)
    return app.send_static_file('fig.png')
