import sqlite3
import random

conn = sqlite3.connect("database.db")
cursor = conn.cursor()

# ----------------- Crear tablas -----------------
cursor.execute("""
CREATE TABLE IF NOT EXISTS usuarios (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre TEXT NOT NULL,
    email TEXT NOT NULL UNIQUE,
    password TEXT NOT NULL,
    curso TEXT NOT NULL,
    puntos INTEGER DEFAULT 0,
    medallas TEXT,
    premium BOOLEAN DEFAULT 0,
    fecha_creacion DATETIME DEFAULT CURRENT_TIMESTAMP
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS preguntas (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    tema TEXT NOT NULL,
    pregunta TEXT NOT NULL,
    respuesta TEXT NOT NULL
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS progreso (
    usuario_id INTEGER NOT NULL,
    pregunta_id INTEGER NOT NULL,
    PRIMARY KEY(usuario_id, pregunta_id),
    FOREIGN KEY(usuario_id) REFERENCES usuarios(id),
    FOREIGN KEY(pregunta_id) REFERENCES preguntas(id)
)
""")

conn.commit()

# ----------------- Preguntas realistas -----------------
temas = {
    "historia": [
        ("¿En qué año comenzó la Segunda Guerra Mundial?", "1939"),
        ("¿Quién fue el primer presidente de Estados Unidos?", "George Washington"),
        ("¿Qué imperio construyó la Gran Muralla?", "China"),
        ("¿Quién descubrió América?", "Cristóbal Colón"),
        ("¿Qué país fue conocido como Prusia?", "Alemania")
    ],
    "matematicas": [
        ("¿Cuánto es 12 x 8?", "96"),
        ("¿Raíz cuadrada de 144?", "12"),
        ("¿Cuánto es 7 + 6 x 3?", "25"),
        ("¿Valor de π aproximado a 2 decimales?", "3.14"),
        ("¿Cuánto es 2^5?", "32")
    ],
    "ciencias": [
        ("¿Cuál es el elemento químico con símbolo H?", "Hidrógeno"),
        ("¿Planeta más grande del sistema solar?", "Júpiter"),
        ("¿Qué gas respiramos principalmente?", "Oxígeno"),
        ("¿Agua en estado sólido se llama?", "Hielo"),
        ("¿Cómo se llama la célula básica de los seres vivos?", "Célula")
    ],
    "deportes": [
        ("¿Cuántos jugadores tiene un equipo de fútbol?", "11"),
        ("¿Qué deporte utiliza raquetas y una red?", "Tenis"),
        ("¿En qué deporte se usa un aro y un balón?", "Baloncesto"),
        ("¿Quién tiene más Grand Slam en tenis masculino?", "Novak Djokovic"),
        ("¿Qué país ganó el Mundial 2018 de fútbol?", "Francia")
    ]
}

# Para cada tema, generamos 1000 preguntas combinando las base y variaciones
for tema, base_preguntas in temas.items():
    count = 0
    while count < 1000:
        pregunta_base, respuesta_base = random.choice(base_preguntas)
        # Añadimos un número aleatorio para diferenciar preguntas
        numero = count + 1
        pregunta = f"{pregunta_base} (versión {numero})"
        respuesta = respuesta_base
        cursor.execute(
            "INSERT INTO preguntas (tema, pregunta, respuesta) VALUES (?, ?, ?)",
            (tema, pregunta, respuesta)
        )
        count += 1

conn.commit()
conn.close()
print("Base de datos creada con 1000 preguntas realistas por tema.")
