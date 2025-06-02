from flask import Flask, request, render_template, redirect, url_for, session
import os
from datetime import timedelta
import threading

app = Flask(__name__)
app.secret_key = 'секретная_строка_соли_базара_джексон'
app.permanent_session_lifetime = timedelta(minutes=30)

LOG_FILE = 'received.log'
USERNAME = 'admin'
PASSWORD = 'admin123'

# -------------------- AUTH --------------------

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        if request.form['username'] == USERNAME and request.form['password'] == PASSWORD:
            session['user'] = USERNAME
            return redirect(url_for('dashboard'))
        return render_template('login.html', error="Неверные данные")
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect(url_for('login'))

def is_logged_in():
    return 'user' in session

# -------------------- UPLOAD --------------------

@app.route('/api/upload-app', methods=['POST'])
def upload_log():
    file = request.files.get('file')
    if file:
        file.save(LOG_FILE)
        return 'OK', 200
    return 'No file received', 400



@app.route('/api/upload-system', methods=['POST'])
def upload_system_logs():
    saved = []
    for key in request.files:
        file = request.files[key]
        if file:
            filename = f"received_{key}.log"
            file.save(filename)
            saved.append(filename)

    if saved:
        return f"Принято: {', '.join(saved)}", 200
    return 'Нет файлов', 400


# -------------------- DASHBOARD --------------------

@app.route('/app-logs')
def dashboard():
    if not is_logged_in():
        return redirect(url_for('login'))

    logs = []
    if os.path.exists(LOG_FILE):
        with open(LOG_FILE, 'r', encoding='utf-8', errors='ignore') as f:
            for line in reversed(f.readlines()):
                parts = line.strip().split(']')
                if len(parts) < 3:
                    continue
                timestamp = parts[0].strip('[')
                event_type = parts[1].strip().strip('[')
                rest = parts[2].strip()
                logs.append({
                    'time': timestamp,
                    'event': event_type,
                    'info': rest
                })

    return render_template('dashboard.html', logs=logs)


@app.route('/system-logs')
def system_logs():
    if not is_logged_in():
        return redirect(url_for('login'))

    filenames = {
        "auth": "received_auth.log",
        "syslog": "received_syslog.log",
        "nginx_access": "received_nginx_access.log",
        "nginx_error": "received_nginx_error.log"
    }

    logs = {}
    for name, path in filenames.items():
        if os.path.exists(path):
            with open(path, 'r', encoding='utf-8', errors='ignore') as f:
                logs[name] = list(reversed(f.readlines()))

    return render_template('system_logs.html', logs=logs)




if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)