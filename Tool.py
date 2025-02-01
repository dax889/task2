from flask import Flask, request, redirect, jsonify
import random
import string
import sqlite3

app = Flask(__name__)

db_file = "url_shortener.db"

def init_db():
    conn = sqlite3.connect(db_file)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS urls (
                    id INTEGER PRIMARY KEY,
                    long_url TEXT NOT NULL,
                    short_code TEXT UNIQUE NOT NULL,
                    clicks INTEGER DEFAULT 0
                )''')
    conn.commit()
    conn.close()

def generate_short_code(length=6):
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))

@app.route('/shorten', methods=['POST'])
def shorten_url():
    data = request.get_json({"long_url": "https://example.com"})
    long_url = data.get({"long_url": "https://example.com"})
    if not long_url:
        return jsonify({"error": "Missing URL"}), 400
    
    conn = sqlite3.connect(db_file)
    c = conn.cursor()
    short_code = generate_short_code()
    c.execute("INSERT INTO urls (long_url, short_code) VALUES (?, ?)", (long_url, short_code))
    conn.commit()
    conn.close()
    
    return jsonify({"short_url": "http://localhost:5000/{short_code}"})

@app.route('/<short_code>', methods=['GET'])
def redirect_url(short_code):
    conn = sqlite3.connect(db_file)
    c = conn.cursor()
    c.execute("SELECT long_url, clicks FROM urls WHERE short_code = ?", (short_code,))
    result = c.fetchone()
    if result:
        long_url, clicks = result
        c.execute("UPDATE urls SET clicks = ? WHERE short_code = ?", (clicks + 1, short_code))
        conn.commit()
        conn.close()
        return redirect(long_url)
    else:
        conn.close()
        return jsonify({"error": "URL not found"}), 404

@app.route('/analytics/<short_code>', methods=['GET'])
def analytics(short_code):
    conn = sqlite3.connect(db_file)
    c = conn.cursor()
    c.execute("SELECT clicks FROM urls WHERE short_code = ?", (short_code,))
    result = c.fetchone()
    conn.close()
    if result:
        return jsonify({"short_code": short_code, "clicks": result[0]})
    else:
        return jsonify({"error": "URL not found"}), 404

if __name__ == '__main__':
    init_db()
    app.run(debug=True)
