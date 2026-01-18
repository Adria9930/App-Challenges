import sqlite3
import random

conn = sqlite3.connect("database.db")
cursor = conn.cursor()

# Limpiar tabla preguntas antes de generar
cursor.execute("DELETE FROM preguntas")
conn.commit()

# ────────────── Datos base para las preguntas ──────────────

# Matemáticas
operaciones = ["+", "-", "*"]
valores = list(range(1, 101))  # números del 1 al 100

# Historia
eventos_historia = [
    ("Primera Guerra Mundial", 1914),
    ("Segunda Guerra Mundial", 1939),
    ("Revolución Francesa", 1789),
    ("Descubrimiento de América", 1492),
    ("Independencia de México", 1810),
]

# Ciencia
elementos = [("hidrógeno", "H"), ("oxígeno", "O"), ("oro", "Au"), ("plata", "Ag"), ("hierro", "Fe")]
formulas = [("agua", "H2O"), ("dióxido de carbono", "CO2"), ("sal común", "NaCl")]

# Geografía
capitales = [
    ("Francia", "París"), ("España", "Madrid"), ("Japón", "Tokio"),
    ("Brasil", "Brasilia"), ("Argentina", "Buenos Aires"), ("Italia", "Roma")
]

# Lengua
palabras = [
    ("luz", "luces"), ("flor", "flores"), ("coche", "coches"),
    ("rápido", "lento"), ("alto", "bajo"), ("feliz", "triste")
]

temas = ["matematicas", "historia", "ciencia", "geografia", "lengua"]

# ────────────── Función para generar 1000 preguntas por tema ──────────────
def generar_pregunta(tema, numero):
    if tema == "matematicas":
        a = random.choice(valores)
        b = random.choice(valores)
        op = random.choice(operaciones)
        if op == "+":
            respuesta = str(a + b)
        elif op == "-":
            respuesta = str(a - b)
        else:
            respuesta = str(a * b)
        pregunta = f"Pregunta {numero}: ¿Cuánto es {a} {op} {b}?"
    elif tema == "historia":
        evento, año = random.choice(eventos_historia)
        pregunta = f"Pregunta {numero}: ¿En qué año ocurrió {evento}?"
        respuesta = str(año)
    elif tema == "ciencia":
        if random.random() < 0.5:
            elem, simbolo = random.choice(elementos)
            pregunta = f"Pregunta {numero}: ¿Cuál es el símbolo químico de {elem}?"
            respuesta = simbolo
        else:
            sust, formula = random.choice(formulas)
            pregunta = f"Pregunta {numero}: ¿Cuál es la fórmula química de {sust}?"
            respuesta = formula
    elif tema == "geografia":
        pais, capital = random.choice(capitales)
        pregunta = f"Pregunta {numero}: ¿Cuál es la capital de {pais}?"
        respuesta = capital
    elif tema == "lengua":
        palabra, resp = random.choice(palabras)
        pregunta = f"Pregunta {numero}: Escribe el plural o antónimo de '{palabra}'."
        respuesta = resp
    else:
        pregunta = f"Pregunta {numero}: {tema} desconocido"
        respuesta = "respuesta"
    return pregunta, respuesta

# ────────────── Generar y guardar preguntas ──────────────
for tema in temas:
    for i in range(1, 1001):  # 1000 preguntas por tema
        preg, resp = generar_pregunta(tema, i)
        cursor.execute(
            "INSERT INTO preguntas (tema, pregunta, respuesta) VALUES (?, ?, ?)",
            (tema, preg, resp)
        )

conn.commit()
conn.close()
print("Se generaron 1000 preguntas realistas por cada tema.")
