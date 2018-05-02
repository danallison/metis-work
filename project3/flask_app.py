from flask import Flask
from sqlalchemy import create_engine

import os

app = Flask(__name__)
sql_engine = create_engine('postgresql://{user}:{password}@{host}:{port}/{user}'.format(
    user=os.environ['POSTGRES_USER'],
    password=os.environ['POSTGRES_PASSWORD'],
    host='db', # docker-compose service name
    port='5432'
))

@app.route('/')
def hello():
    with sql_engine.connect() as connection:
        id, key, val = connection.execute(
            'select * from foo limit 1'
        ).fetchone()
    return '<h1>Hi, World!</h1><p>{}:{}:{}</p>'.format(id, key, val)
