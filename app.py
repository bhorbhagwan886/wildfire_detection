from flask import Flask, render_template, request, redirect, url_for, session
import sqlite3

app = Flask(__name__)
app.secret_key = "wildfire_secret_key"

# ------------------------
# Database Setup
# ------------------------
def init_db():
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            email TEXT UNIQUE,
            password TEXT
        )
    """)
    conn.commit()
    conn.close()

init_db()

# ------------------------
# Routes
# ------------------------

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/contact")
def contact():
    return render_template("contact.html")

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        name = request.form["name"]
        email = request.form["email"]
        password = request.form["password"]

        try:
            conn = sqlite3.connect("users.db")
            cursor = conn.cursor()
            cursor.execute("INSERT INTO users (name, email, password) VALUES (?, ?, ?)",
                           (name, email, password))
            conn.commit()
            conn.close()
            return redirect(url_for("login"))
        except:
            return "Email already exists!"

    return render_template("register.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]

        conn = sqlite3.connect("users.db")
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE email=? AND password=?",
                       (email, password))
        user = cursor.fetchone()
        conn.close()

        if user:
            session["user"] = user[1]
            return redirect(url_for("home"))
        else:
            return "Invalid Email or Password"

    return render_template("login.html")

@app.route("/logout")
def logout():
    session.pop("user", None)
    return redirect(url_for("home"))

if __name__ == "__main__":
    app.run(debug=True)
