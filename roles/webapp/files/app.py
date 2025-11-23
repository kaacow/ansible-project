import os
from flask import Flask, request, render_template_string
import mysql.connector

app = Flask(__name__)

DB_HOST = os.getenv('DB_HOST', 'localhost')
DB_USER = os.getenv('DB_USER', 'myappuser')
DB_PASS = os.getenv('DB_PASS', 'StrongPassword123')
DB_NAME = os.getenv('DB_NAME', 'myappdb')

HTML = """
<!doctype html>
<html>
<head>
    <title>Attack on DevOps - Credentials Check</title>
    <style>
        body {
            margin: 0;
            padding: 0;
            font-family: Arial, sans-serif;
            background-image: url('https://i.pinimg.com/736x/cb/fd/39/cbfd397a677556467c41f4d308a15c35.jpg');
            background-size: cover;
            background-position: center;
            background-attachment: fixed;
            color: white;
        }

        .overlay {
            background: rgba(0, 0, 0, 0.7);
            min-height: 100vh;
            padding-top: 80px;
        }

        .container {
            width: 400px;
            margin: auto;
            padding: 30px;
            background: rgba(15, 23, 42, 0.9);
            border-radius: 12px;
            text-align: center;
            box-shadow: 0 0 20px black;
        }

        h1 {
            margin-bottom: 10px;
        }

        input {
            width: 90%;
            padding: 10px;
            margin: 8px 0;
            border-radius: 6px;
            border: none;
        }

        button {
            padding: 10px 20px;
            border: none;
            border-radius: 6px;
            background-color: #16a34a;
            color: white;
            font-size: 15px;
            cursor: pointer;
        }

        img {
            margin-top: 15px;
            width: 100%;
            border-radius: 10px;
        }

        .status {
            font-size: 18px;
            margin-top: 15px;
            font-weight: bold;
        }
    </style>
</head>
<body>

<div class="overlay">
    <div class="container">
        <h1>Attack on DevOps</h1>
        <p>Credential Verification System</p>

        <form method="POST" action="/login">
            <input type="text" name="username" placeholder="Username" required><br>
            <input type="password" name="password" placeholder="Password" required><br>
            <button type="submit">Check</button>
        </form>

        {% if result == "success" %}
            <p class="status" style="color:#22c55e;">True credentials ✅</p>
            <img src="https://i.pinimg.com/736x/1a/7c/9d/1a7c9d53a01027986c75c7510933ee0f.jpg" alt="Happy Mikasa">
        {% elif result == "fail" %}
            <p class="status" style="color:#ef4444;">Try again ❌</p>
            <img src="https://i.redd.it/since-people-are-complaining-yet-again-on-erens-face-i-v0-kzgyanlqq3la1.jpg?width=1920&format=pjpg&auto=webp&s=ee2393c542c57e380d130f6ea1fb435319fab158" alt="Sad Eren">
        {% endif %}
    </div>
</div>

</body>
</html>
"""

@app.route("/", methods=["GET"])
def home():
    return render_template_string(HTML, result=None)


@app.route("/login", methods=["POST"])
def login():
    username = request.form.get("username")
    password = request.form.get("password")

    try:
        conn = mysql.connector.connect(
            host=DB_HOST,
            user=DB_USER,
            password=DB_PASS,
            database=DB_NAME
        )

        cursor = conn.cursor(dictionary=True)
        cursor.execute(
            "SELECT * FROM users WHERE username=%s AND password=%s",
            (username, password)
        )
        user = cursor.fetchone()

        cursor.close()
        conn.close()

        if user:
            return render_template_string(HTML, result="success")
        else:
            return render_template_string(HTML, result="fail")

    except Exception as e:
        return render_template_string(
            "<h2 style='color:red;'>Database error:</h2><p>{{error}}</p>", 
            error=str(e)
        )


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=3000, debug=True)

