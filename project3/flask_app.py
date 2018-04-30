from flask import Flask

import numpy as np
import json

app = Flask(__name__)

@app.route('/')
def hello():
    return '<h1>Hello, World!</h1>'

@app.route('/uniform/<shape>')
def uniform(shape):
    shape = tuple(int(s) for s in shape.split('x'))
    return json.dumps(np.random.uniform(size=shape).tolist())
