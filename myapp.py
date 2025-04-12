from flask import Flask, render_template, request
import sqlite3
import os

app = Flask(__name__)

def init_db():
    conn = sqlite3.connect("specimen_data.db")
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS specimens (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    username TEXT,
                    specimen TEXT,
                    image_size REAL,
                    magnification REAL,
                    actual_size REAL
                )''')
    conn.commit()
    conn.close()

def save_to_db(username, specimen, image_size, magnification, actual_size):
    conn = sqlite3.connect("specimen_data.db")
    c = conn.cursor()
    c.execute("INSERT INTO specimens (username, specimen, image_size, magnification, actual_size) VALUES (?, ?, ?, ?, ?)",
              (username, specimen, image_size, magnification, actual_size))
    conn.commit()
    conn.close()

@app.route("/", methods=["GET", "POST"])
def index():
    result = None
    if request.method == "POST":
        try:
            username = request.form["username"]
            specimen = request.form["specimen"]
            image_size = float(request.form["imageSize"])
            magnification = float(request.form["magnification"])

            if magnification == 0:
                result = "❌ Magnification cannot be zero."
            else:
                actual_size = image_size / magnification
                save_to_db(username, specimen, image_size, magnification, actual_size)
                result = f"Hi {username}, the real size of '{specimen}' is {actual_size:.4f} mm."
        except:
            result = "❌ Invalid input. Please enter valid numbers."
    return render_template("index.html", result=result)

if __name__ == "__main__":
    init_db()
    
 port = int(os.environ.get("PORT", 5000))
 app.run(host='0.0.0.0', port=port)

