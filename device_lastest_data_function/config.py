# -*- coding:utf-8 -*-

import psycopg2
from pymongo import mongo_client

from .settings import settings


class PGClient(object):

    def __init__(self):
        self.host = settings.PG_HOST
        self.port = settings.PG_PORT
        self.database = settings.PG_DATABASE
        self.user = settings.PG_USER
        self.password = settings.PG_PASSWORD

    def connect(self):
        connect = psycopg2.connect(host=self.host,
                                        port=self.port,
                                        database=self.database,
                                        user=self.user,
                                        password=self.password)
        return connect

class MongoClient(object):

    def __init__(self):
        self.mongodb_host=settings.MONGODB_HOST
        self.mongodb_port = settings.MONGODB_PORT
        self.mongodb_db = settings.MONGODB_DB
        self.mongodb_password = settings.MONGODB_PASSWORD
        self.mongodb_username = settings.MONGODB_USERNAME
       
        self.client = mongo_client.MongoClient(
        "mongodb://" + self.mongodb_username + ":" + self.mongodb_password + "@" + self.mongodb_host + ":"
        + self.mongodb_port + "/" + self.mongodb_db)

    def db(self):
        db = self.client[self.mongodb_db]
        return db

    def client(self):
        return self.client 