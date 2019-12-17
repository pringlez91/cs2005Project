# Set the path
import os, sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from project_app import app
import sqlalchemy
'''
This one is creating the engine for Database and commit method
for inputing our data to Database
'''
db_uri = 'sqlite:///database.db'
app.config['PROJECT_DATABASE_NAME'] = 'cs2005'
engine = sqlalchemy.create_engine(db_uri)
conn = engine.connect()
conn.execute("commit")
conn.execute("drop database "  + app.config['PROJECT_DATABASE_NAME'])
conn.execute("create database "  + app.config['PROJECT_DATABASE_NAME'])
conn.close()
