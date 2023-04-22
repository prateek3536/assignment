from flask import Flask, render_template, request, redirect, url_for, make_response
import uuid

app = Flask(__name__)
app.secret_key = 'secret_key'

# Define a dictionary of users (replace with your own authentication mechanism)
users = {'prateek': '123', 'rohan': 'xyz'}

# Define a dictionary to store the user tokens
tokens = {}

# Define the login route
@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        if username in users and users[username] == password:
            token = str(uuid.uuid4())
            tokens[token] = username
            response = make_response(redirect(url_for('secret')))
            response.set_cookie('token', token)
            return response
        else:
            return render_template('login.html', error=True)
    else:
        return render_template('login.html', error=False)

# Define the secret route
@app.route('/secret')
def secret():
    token = request.cookies.get('token')

    if token in tokens:
        username = tokens[token]
        return render_template('secret.html', username=username)
    else:
        return redirect(url_for('login'))

# Define the logout route
@app.route('/logout')
def logout():
    token = request.cookies.get('token')

    if token in tokens:
        del tokens[token]

    response = make_response(redirect(url_for('login')))
    response.set_cookie('token', '', expires=0)
    return response

if __name__ == '__main__':
    app.run(debug=True)
