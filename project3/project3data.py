import os
import pandas as pd
import numpy as np

from project3utils import get_features_from_url
from project3sql_helpers import with_remote_sql_session, with_local_sql_session

training_data = None

def reload_training_data():
    phishing_urls = pd.read_csv('data/phishtank2018-05-02_verified_online.csv').head(10000).url
    nonphishing_urls = pd.read_csv('data/scraped_urls.txt', header=None, names=['url']).url
    phishing_features = pd.DataFrame(list(phishing_urls.apply(get_features_from_url)), dtype=np.float64)
    nonphishing_features = pd.DataFrame(list(nonphishing_urls.apply(get_features_from_url)), dtype=np.float64)
    phishing_features['is_phishing'] = 1
    nonphishing_features['is_phishing'] = 0
    training_data = pd.concat([phishing_features, nonphishing_features], ignore_index=True)
    return training_data

def get_training_data():
    if training_data is None: return reload_training_data()
    return training_data

def run_migrations(remote=False):
    def run(session):
        session.execute(
            """
            CREATE TABLE IF NOT EXISTS migrations (
              migrated VARCHAR(255)
            );
            """
        )
        # Assuming that 'db_migrations' contains only sql migration files
        # and that the files follow the naming convention YYYYMMDDHH_description.sql
        completed_migration_count = 0
        for filename in sorted(os.listdir('db_migrations')):
            migration_id, _ = filename.split('_')
            already_run = session.execute(
                "SELECT * FROM migrations WHERE migrated = '{}'".format(migration_id)
            ).fetchone()
            if already_run:
                print('skipping migration {}'.format(filename))
                continue
            else:
                print('starting migration {}'.format(filename))
                with open('db_migrations/{}'.format(filename), 'r') as sql_file:
                    session.execute('BEGIN')
                    session.execute(sql_file.read())
                    session.execute("INSERT INTO migrations (migrated) VALUES ('{}')".format(migration_id))
                    session.execute('COMMIT')
                print('completed migration {}'.format(filename))
                completed_migration_count += 1
        print('completed {} pending migration(s)'.format(completed_migration_count))
    if remote:
        with_remote_sql_session(run)
    else:
        with_local_sql_session(run)
