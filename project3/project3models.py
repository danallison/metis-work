import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.metrics import f1_score, accuracy_score, classification_report
from sklearn.externals import joblib

import project3utils
import project3data
import project3viz

from importlib import reload

model_names = ['domain_model','path_model','model']
feature_columns = {
    'domain_model': project3utils.nonpath_feature_columns,
    'path_model': project3utils.path_feature_columns,
    'model': project3utils.numeric_feature_columns
}

def get_models():
    return {name: joblib.load('{}.pkl'.format(name)) for name in model_names}

def print_model_stats(model, name, X_test, y_test):
    # reload(project3viz)
    predictions = model.predict(X_test)
    probabilities = model.predict_proba(X_test)[:,1]
    acc = round(accuracy_score(y_test, predictions), 2)
    print('============= {} ============='.format(name))
    print("Accuracy: {}".format(acc))
    print(classification_report(y_test, predictions))
    project3viz.plot_roc_curve(y_test, probabilities)

def train_models(data=None, names=None, callback=None):
    if data is None: data = get_training_data()
    if names is None: names = model_names
    if callback is None: callback = print_model_stats
    X = data[project3utils.numeric_feature_columns]
    y = data['is_phishing']
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=987)
    for name in model_names:
        columns = feature_columns[name]
        Xi_train, Xi_test, yi_train, yi_test = X_train[columns], X_test[columns], y_train, y_test
        if name == 'path_model':
            # Filter out data with no path
            train_mask = (Xi_train.path_empty_string == 0)
            test_mask = (Xi_test.path_empty_string == 0)
            Xi_train, Xi_test = Xi_train[train_mask], Xi_test[test_mask]
            yi_train, yi_test = yi_train[train_mask], yi_test[test_mask]
        model = RandomForestClassifier(n_estimators=32, criterion='gini')
        model.fit(Xi_train, yi_train)
        callback(model, name, Xi_test, yi_test)
        joblib.dump(model, '{}.pkl'.format(name))
