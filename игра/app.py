from flask import Flask, render_template, request, redirect, session, url_for
import os

app = Flask(__name__)
app.secret_key = '192168'  # Замените на свой секретный ключ

# Проверка существования файлов
if not os.path.exists('users.txt'):
    open('users.txt', 'w').close()
if not os.path.exists('mess.txt'):
    open('mess.txt', 'w').close()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        with open('users.txt', 'r') as f:
            users = f.readlines()
        
        for user in users:
            user_login, user_password = user.strip().split(':')
            if user_login == username and user_password == password:
                session['username'] = username
                return redirect(url_for('chat'))
        
        return 'Неверный логин или пароль'
    
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        with open('users.txt', 'a') as f:
            f.write(f"{username}:{password}\n")
        
        return redirect(url_for('login'))
    
    return render_template('register.html')

@app.route('/chat', methods=['GET', 'POST'])
def chat():
    if 'username' not in session:
        return redirect(url_for('login'))
    
    if request.method == 'POST':
        message = f"{session['username']}: {request.form['message']}"
        with open('mess.txt', 'a') as f:
            f.write(f"{message}\n")
        return redirect(url_for('chat'))
    
    with open('mess.txt', 'r') as f:
        messages = f.readlines()
    
    return render_template('chat.html', messages=messages)

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
