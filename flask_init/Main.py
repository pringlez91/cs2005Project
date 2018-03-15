from flask import Flask,url_for,request, render_template, flash, redirect, url_for, session, logging
import sqlite3
from wtforms import Form, StringField, TextAreaField, PasswordField, IntegerField, validators, ValidationError
from passlib.hash import sha256_crypt

app = Flask(__name__)
def check_password(hashed_password, user_password):
    return hashed_password == hashlib.md5(user_password.encode()).hexdigest()


# @app.route('/',methods=['GET', 'POST'])
# def login():
#     error= None
#     if request.method == 'POST':
#         username = request.form['username']
#         password = request.form['password']
#         if valid_login(username,password):
#             return redirect(url_for('secret'))
#         else:
#             error = 'Incorrect username and password'
#     return render_template('login.html',error=error)
#
# def valid_login(username, password):
#     con = sqlite3.connect('Database/Users.db')
#     completion = False
#     with con:
#                 cur = con.cursor()
#                 cur.execute("SELECT * FROM Users")
#                 rows = cur.fetchall()
#                 for row in rows:
#
#
#                     dbUser = row[0]
#                     dbPass = row[1]
#                     if dbUser==username:
#                         completion=check_password(dbPass, password)
#     return completion
#
# @app.route('/secret')
# def secret():
#     return "You have successfully logged in"

@app.route('/login',methods=['GET', 'POST'])
def login():

    if request.method == 'POST':
        ##get From fields
        username = request.form['username']
        password_c = request.form['password']
        sqlite_file = '/home/pringlez/cs2005/Database/EazyA.db'


        conn = sqlite3.connect(sqlite_file)
        cur=conn.cursor()


        cur.execute("SELECT username FROM users")
        names = {name[0] for name in cur.fetchall()}
        if username in names:
            return render_template('baseLogin.html')
        else:
            return "fail"







    return render_template('login.html')


# def valid_login(username, password):
#
#
#
#
#     if result > 0:
#         data= cur.fetchone()
#         password = data["password"]
#
#     with con:
#                 cur = con.cursor()
#                 cur.execute("SELECT * FROM Users")
#                 rows = cur.fetchall()
#                 for row in rows:
#
#
#                     dbUser = row[0]
#                     dbPass = row[1]
#                     if dbUser==username:
#                         completion=check_password(dbPass, password)
#     return completion

# @app.route('/secret')
# def secret():
#     return "You have successfully logged in"

class SignUp(Form):
    sn = StringField('Student Number',[validators.InputRequired()] )
    def validate_sn(form, field):
        if len(field.data) != 9 or field.data.isdigit()==False:
            raise ValidationError('Please Enter a valied MUN student number')

        sqlite_file = '/home/pringlez/cs2005/Database/EazyA.db'

        conn = sqlite3.connect(sqlite_file)
        cur=conn.cursor()
        cur.execute("SELECT student_number FROM users")
        sns = {student_number[0] for student_number in cur.fetchall()}
        if field.data in sns:
            raise ValidationError(' ST Number already exist')


    username = StringField('Username',[validators.InputRequired()] )
    def validate_username(form, field):
        invalid=['!','@','#','%','(',')','+','=']
        if len(field.data) <= 4 or len(field.data) >= 30 :
            raise ValidationError('Please enter username between 4 and 30 characters')
        if field.data.isdigit()==True :
            raise ValidationError('Please enter username containing letters and alphabets')
        for c in invalid:
            if c in field.data:
                raise ValidationError("Username cannot contain '!','@','#','%','(',')','+','='")
        sqlite_file = '/home/pringlez/cs2005/Database/EazyA.db'

        conn = sqlite3.connect(sqlite_file)
        cur=conn.cursor()

        cur.execute("SELECT username FROM users")
        usernames = {username[0] for username in cur.fetchall()}
        if field.data in usernames:
            raise ValidationError('Username already exist')


    last = StringField('Last Name',[validators.InputRequired()] )
    def validate_last(form, field):
        if any(i.isdigit() for i in field.data)==True:
            raise ValidationError('Please Enter a Valied Last Name')

    first = StringField('First Name',[validators.InputRequired()] )
    def validate_first(form, field):
        if any(i.isdigit() for i in field.data)==True:
            raise ValidationError('Please Enter a Valied First Name')

    email = StringField('Email',[validators.InputRequired(),validators.Email(message="Enter a Valied Email Address")] )
    def validate_email(form,field):
        sqlite_file = '/home/pringlez/cs2005/Database/EazyA.db'


        conn = sqlite3.connect(sqlite_file)
        cur=conn.cursor()

        cur.execute("SELECT email FROM users")
        emails = {email[0] for email in cur.fetchall()}
        if field.data in emails:
            raise ValidationError('email already exist')

    password = PasswordField('Password',
    [validators.InputRequired(),
    validators.EqualTo('confirm', message='Password do not Match ' )])
    confirm=PasswordField('Confirm Password')
    def validate_password(form, field):
        if field.data.isalpha()==True or field.data.isnumeric()==True \
        or field.data.isdigit()==True or field.data.islower()==True \
        or field.data.isupper()==True or len(field.data) >= 16 or len(field.data) <= 6:
            raise ValidationError( """Password must conatin alphabets and
            numbers  Password cannot contain space Password must
            be between 6 and 16 characters Password must be in lower and upper case""")

@app.route('/signup', methods=['GET', 'POST'])
def register():
    form= SignUp(request.form)
    if request.method == 'POST' and form.validate():
      sn = form.sn.data
      username = form.username.data
      last = form.last.data
      first = form.first.data
      email = form.email.data
      password = sha256_crypt.encrypt(str(form.password.data))
      sqlite_file = '/home/pringlez/cs2005/Database/EazyA.db'
      conn = sqlite3.connect(sqlite_file)
      cur=conn.cursor()
      cur.execute('''INSERT INTO users(student_number, username, last, first, email,pass )
                VALUES(?,?,?,?,?,?)''', (sn,username, last, first, email,password))
      conn.commit()
      conn.close()

      return "You are now registered and can login"




    return render_template('signup.html', form=form)
if __name__ == '__main__':
    app.secret_key = 'my unobvious secret key'

    app.debug = True
    app.run()
