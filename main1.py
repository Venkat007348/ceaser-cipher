from flask import Flask, render_template, request, redirect, session
from app.cipher import encrypt, decrypt
from app.utils import validate_shift
from auth.login import check_login, register_user, user_exists

app = Flask(__name__)
app.secret_key = 'caesar_secret_key'

@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        user = request.form['username']
        pwd = request.form['password']
        if check_login(user, pwd):
            session['user'] = user
            return redirect('/dashboard')
        else:
            return render_template('login.html', error="Invalid credentials")
    return render_template('login1.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        user = request.form['username']
        pwd = request.form['password']
        confirm_pwd = request.form['confirm_password']

        if user_exists(user):
            return render_template('register.html', error="Username already exists")
        if pwd != confirm_pwd:
            return render_template('register.html', error="Passwords do not match")

        register_user(user, pwd)
        return redirect('/')

    return render_template('register.html')


@app.route('/dashboard', methods=['GET', 'POST'])
def dashboard():
    if 'user' not in session:
        return redirect('/')
    result = ''
    if request.method == 'POST':
        text = request.form['text']
        shift = int(request.form['shift'])
        action = request.form['action']
        try:
            validate_shift(shift)
            if action == 'encrypt':
                result = encrypt(text, shift)
            else:
                result = decrypt(text, shift)
        except Exception as e:
            result = f"Error: {e}"
    return render_template('dashboard1.html', result=result)

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')

if __name__ == '__main__':
    app.run(debug=True)
