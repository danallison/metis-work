import pymongo
import secrets

mongo_client = pymongo.MongoClient(
    # Docker hostname
    host='mongo',
    port=27017,
    username=secrets.mongo_user,
    password=secrets.mongo_password,
    connect=True
)
