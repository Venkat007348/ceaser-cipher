from flask import Flask, render_template, request, redirect, session
from app.cipher import encrypt, decrypt
from app.utils import validate_shift
from auth.login import check_login

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
    return render_template('login.html')

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
    return render_template('dashboard.html', result=result)

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')

if __name__ == '__main__':
    app.run(debug=True)
