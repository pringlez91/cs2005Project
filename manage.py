# Set the path
import os, sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import unittest
from flask.ext.script import Manager, Server
from flask.ext.migrate import MigrateCommand
from project_app import app
'''
This module basically runs the whole app and manages the updgrade and degrade the database. The manager keeps track of all the commands and handles how they are called from the command line
'''

manager = Manager(app)
manager.add_command('db', MigrateCommand)

'''
The runserver basically runs the server for the app and use_debugger activates the debugger for the app and everytime there is a problem it will direct to the browser and use_reloader reloads the server
'''
manager.add_command("runserver", Server(
    use_debugger = True,
    use_reloader = True,
    )
)
'''
This test method is running all the test module from tests folder and can be accessed by command line together
'''
@manager.command
def test():
    tests = unittest.TestLoader().discover('tests', pattern='*.py')
    unittest.TextTestRunner(verbosity=2).run(tests)
'''
The manager.run() prepares the Manager instance to receive input from the command line
'''
if __name__ == "__main__":
    manager.run()
