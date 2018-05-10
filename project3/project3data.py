import pandas as pd
import numpy as np

import project3utils

training_data = None

def reload_training_data():
    phishing_urls = pd.read_csv('data/phishtank2018-05-02_verified_online.csv').head(10000).url
    nonphishing_urls = pd.read_csv('data/scraped_urls.txt', header=None, names=['url']).url
    phishing_features = pd.DataFrame(list(phishing_urls.apply(project3utils.get_features_from_url)), dtype=np.float64)
    nonphishing_features = pd.DataFrame(list(nonphishing_urls.apply(project3utils.get_features_from_url)), dtype=np.float64)
    phishing_features['is_phishing'] = 1
    nonphishing_features['is_phishing'] = 0
    training_data = pd.concat([phishing_features, nonphishing_features], ignore_index=True)
    return training_data

def get_training_data():
    if training_data is None: return reload_training_data()
    return training_data
