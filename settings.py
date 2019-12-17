import os

'''
This portion is setting the secret key and debug mode on,
It also giving the sqlite database to SQL Alchmey so that it can create a 
Database and set ORM (Object Relational Model) for the append
'''
SECRET_KEY = 'never guess'
DEBUG=True
SQLALCHEMY_DATABASE_URI = 'sqlite:///database.db'
SQLALCHEMY_TRACK_MODIFICATIONS = True
