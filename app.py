from flask import Flask, request, render_template
import jwt
import sqlite3

app = Flask(__name__)

# Create DB SQLite
conn = sqlite3.connect('database.db', check_same_thread=False)
c = conn.cursor()
c.execute('''CREATE TABLE IF NOT EXISTS users
             (id INTEGER PRIMARY KEY, username TEXT, role TEXT, kid INTEGER, secret TEXT)''')
c.execute("INSERT OR IGNORE INTO users (username, role, kid, secret) VALUES ('admin', 'admin', 1, '123sdfzxczv'), ('user', 'user', 2, '345123sdf')")
conn.commit()

    
@app.route('/', methods=['GET'])
def index():
    token = request.headers.get('Authorization')
    print(token)
    if token:
        token = token.split(' ')[1]
        try:
            kid = jwt.get_unverified_header(token)['kid']
            c.execute("SELECT secret FROM users WHERE kid = ?", (kid,))
            secret = c.fetchone()
            print(kid)
            if secret:
                decoded = jwt.decode(token, secret[0])
                print(decoded)
                try:
                    if decoded['role'] == 'admin':
                        return 'You are Admin'
                    else:
                        return 'Nobe!'
                except jwt.exceptions.InvalidTokenError:
                    return 'Invalid token'
            else:
                return 'Invalid token'
        except jwt.exceptions.DecodeError:
            return 'Invalid token'
    else:
        return 'Missing token'

@app.route('/index.html')
def serve_index():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(host="0.0.0.0", debug=True)