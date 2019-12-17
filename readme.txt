Project Title:
Computer Science 2005 Group Project - F
This group projectis about creating a collaborative tool for students to
communicate with one another, the following is a prototype of what the
application should look like and what is should do.
It is a tool that allows students exchange information and materials used
and other helpful resourses among eachother.
Getting Started:
The following instructions will help you get a copy of the project up
and running on your local machine for development and testing.
However for deployment of the program see Deployment.
Prerequistes :
Later versions of Python - Python 3.4 or newer
requirments.txt - the text file will install all the distributions needed
                    for the project
Installation instructions to get the development env running:
Step 1: Navigate to the directory the project app is saved
eg: cd \users\Desktop\GroupF-1/project_app
-------------------------------------------------------------------------------
For Windows:
Step 2: install the virtual enviroment
    "virtualenv flask"
Step 3: install all the distributions associated with the project
    "flask\Scripts\ pip3 install -r requirments.txt"
Step 4: Return to root directory
    cd \
Step 5: navigate back to the directory where flask is installed

    cd users\Desktop\app\flask\Scripts
Step 6: activate virtualenv with command

    "activate"
Step 7: navigate back to the app directory
Step 8: run the python files using the command python3 "filename".py
-------------------------------------------------------------------------------
For Linux:
Step 2: install virtual enviroment with
	"virtualenv -p python3 venv"
Step 3: install flask with
	"pip install flask"
Step 4: install all the distributions associated with the project
	"pip install -r requirement.txt
Step 5: Run the application with,
	"python manage.py runserver"
Step 6: To run the unittest
	"python manage.py test"
Extra Feature:
	To Update or change the database do input these following commands,
	"python manage.py db migrate"
	"python manage.py db upgrade"
-------------------------------------------------------------------------------
Running the tests:
The test should be run using python3 manage.py test. All the tests are in a seperate folder named tests.
Our unittest is testing the three module in our main folder:
test_model.py: tests the model.py in our main folder. It checks IF our tables in our main database are formated correctly and if our db methods are adding data to the right table
test_form.py: tests the form.py in our main folder. It checks if our wtf form classes for the login,signup, and post forms are producing the right errors and if ther are holding the right data after validation.
test_view.py: This is our main test. It test our integration to limited extend by checking the respons codes and data displayed on the html.
Deployment:
to deploy the application on the system, the command is:
flask run manage.py runserver

-------------------------------------------------------------------------------
Files included:
	|project_app
		|main
      \form.py
      \models.py
      \views.py
    |doc
      \cs2005_FinalProject.pdf
      \Group F FinalProject.pod
    |migrations
      |versions
        \ad02ebc5355f_.py
      \alembic.ini
      \env.py
      \README
      \script.py.mako
      |templates
        \all the html templates
        |includes
          \html files
      |tests
        \test.db
        \test_form.py
        \test_model.py
        \test_view.py
      \database.db
      \dbinit.py
      \__init__.py
      \manage.py
      \readme.txt
      \requirements.txt
      \settings.py


Built With:
SQLAlchemy
Flask
Authors:
Afrah Abdulmajid
Zayed D Imam
Jay D Patel
Ahmed Mohammed
Tirth Patel
