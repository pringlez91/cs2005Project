from flask import Flask,url_for,request, render_template

app = Flask(__name__)

@app.route('/',methods=['GET', 'POST'])
def login():
    error= None
    if request.method == 'POST':
        if valid_login(request.form['username'], request.form['passowrd']):
            return "Welcome back, %" % request.form['username']
        else:
            error = 'Incorrect username and password'
    return render_template('login.html')
def valid_login(username, password):
    if username == password:
        return True
    else:
        return False

if __name__ == '__main__':
    app.debug = True
    app.run()
