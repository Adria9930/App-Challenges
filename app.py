from flask import Flask, request, jsonify, render_template, redirect, url_for, session
import sqlite3
import bcrypt
import random

app = Flask(__name__)
app.secret_key = "TU_CLAVE_SECRETA_AQUI"  # Cambia por una clave fuerte

# ----------------- DB -----------------
def get_db():
    conn = sqlite3.connect("database.db")
    conn.row_factory = sqlite3.Row
    return conn

# ----------------- Usuario -----------------
@app.route("/")
def home_redirect():
    return redirect(url_for("login_page"))

@app.route("/register-page")
def register_page():
    return render_template("register.html")

@app.route("/register", methods=["POST"])
def register():
    data = request.get_json()
    nombre = data.get("nombre")
    email = data.get("email")
    password = data.get("password")
    curso = data.get("curso")

    hashed_password = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())

    conn = get_db()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO usuarios (nombre, email, password, curso) VALUES (?, ?, ?, ?)",
        (nombre, email, hashed_password, curso)
    )
    conn.commit()
    conn.close()

    return jsonify({"message": "Usuario registrado correctamente"})

@app.route("/login-page")
def login_page():
    return render_template("login.html")

@app.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    email = data.get("email")
    password = data.get("password")

    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM usuarios WHERE email = ?", (email,))
    user = cursor.fetchone()
    conn.close()

    if user and bcrypt.checkpw(password.encode("utf-8"), user["password"]):
        session["user_id"] = user["id"]
        session["user_name"] = user["nombre"]
        return jsonify({"message": "Login correcto"})
    else:
        return jsonify({"error": "Credenciales incorrectas"}), 401

@app.route("/home")
def home():
    if "user_id" not in session:
        return redirect(url_for("login_page"))
    return render_template("home.html")

@app.route("/profile")
def profile():
    if "user_id" not in session:
        return redirect(url_for("login_page"))
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM usuarios WHERE id = ?", (session["user_id"],))
    user = cursor.fetchone()
    conn.close()
    return render_template("profile.html", user=user)

@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login_page"))

# ----------------- Retos -----------------
@app.route("/retos/<tema>/siguiente")
def siguiente_pregunta(tema):
    if "user_id" not in session:
        return redirect(url_for("login_page"))

    conn = get_db()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT * FROM preguntas WHERE LOWER(tema) = ? ORDER BY RANDOM() LIMIT 1",
        (tema.lower(),)
    )
    row = cursor.fetchone()
    conn.close()

    if not row:
        return "No hay preguntas para este tema"

    # 🔥 ESTA LÍNEA ES LA CLAVE
    pregunta = dict(row)

    return render_template("participar_pregunta.html", pregunta=pregunta)

@app.route("/retos/<int:pregunta_id>/participar", methods=["POST"])
def participar_pregunta(pregunta_id):
    if "user_id" not in session:
        return jsonify({"error": "No autenticado"}), 401

    respuesta_usuario = request.get_json().get("respuesta", "").lower().strip()
    user_id = session["user_id"]

    conn = get_db()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM preguntas WHERE id = ?", (pregunta_id,))
    pregunta = cursor.fetchone()
    if not pregunta:
        conn.close()
        return jsonify({"error": "Pregunta no encontrada"}), 404

    correcta = pregunta["respuesta"].lower().strip()
    correcto = False

    if respuesta_usuario == correcta:
        # Sumar punto
        cursor.execute("UPDATE usuarios SET puntos = puntos + 1 WHERE id = ?", (user_id,))
        correcto = True

    # Registrar progreso para no repetir
    cursor.execute(
        "INSERT OR IGNORE INTO progreso (usuario_id, pregunta_id) VALUES (?, ?)",
        (user_id, pregunta_id)
    )

    conn.commit()
    conn.close()
    return jsonify({"correcto": correcto})

# ----------------- Ranking -----------------
@app.route("/ranking")
def ranking():
    if "user_id" not in session:
        return redirect(url_for("login_page"))
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT nombre, puntos FROM usuarios ORDER BY puntos DESC LIMIT 10")
    top10 = cursor.fetchall()
    conn.close()
    return render_template("ranking.html", top10=top10)

# ----------------- Inicialización -----------------
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
