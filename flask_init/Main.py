from flask import Flask,url_for,request, render_template
import sqlite3
import hashlib

app = Flask(__name__)
def check_password(hashed_password, user_password):
    return hashed_password == hashlib.md5(user_password.encode()).hexdigest()


@app.route('/',methods=['GET', 'POST'])
def login():
    error= None
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if valid_login(username,password):
            return redirect(url_for('secret'))    
        else:
            error = 'Incorrect username and password' 
    return render_template('login.html',error=error)

def valid_login(username, password):
    con = sqlite3.connect('Database/Users.db')
    completion = False
    with con:
                cur = con.cursor()
                cur.execute("SELECT * FROM Users")
                rows = cur.fetchall()
                for row in rows:
                    dbUser = row[0]
                    dbPass = row[1]
                    if dbUser==username:
                        completion=check_password(dbPass, password)
    return completion

@app.route('/secret')
def secret():
    return "You have successfully logged in"

if __name__ == '__main__':
    app.debug = True
    app.run()
