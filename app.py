from flask import Flask
import psycopg2
import os
import time

app = Flask(__name__)

APP_NAME = os.getenv("APP_NAME", "Mi Aplicacion")
VERSION = os.getenv("VERSION", "1.0.0")

DB_HOST = os.getenv("DB_HOST")
DB_NAME = os.getenv("DB_NAME")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")


def get_connection():
    return psycopg2.connect(
        host=DB_HOST,
        database=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD
    )


def init_db():

    time.sleep(10)

    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
    CREATE TABLE IF NOT EXISTS productos(
        id SERIAL PRIMARY KEY,
        nombre VARCHAR(100),
        precio NUMERIC(10,2),
        stock INTEGER
    )
    """)

    cur.execute("SELECT COUNT(*) FROM productos")
    total = cur.fetchone()[0]

    if total == 0:

        cur.execute("""
        INSERT INTO productos(nombre,precio,stock)
        VALUES
        ('Laptop',850,10),
        ('Mouse',25,50),
        ('Teclado',40,30),
        ('Monitor',200,15),
        ('Impresora',180,8)
        """)

    conn.commit()
    cur.close()
    conn.close()


@app.route("/")
def home():

    try:

        conn = get_connection()
        conn.close()

        estado = "Conectado a PostgreSQL"

    except:
        estado = "Sin conexión"

    return f"""
    <h1>{APP_NAME}</h1>
    <h2>Version {VERSION}</h2>
    <h3>{estado}</h3>
    """


@app.route("/productos")
def productos():

    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
    SELECT id,nombre,precio,stock
    FROM productos
    """)

    datos = cur.fetchall()

    html = """
    <h1>Productos</h1>
    <table border='1'>
    <tr>
    <th>ID</th>
    <th>Nombre</th>
    <th>Precio</th>
    <th>Stock</th>
    </tr>
    """

    for p in datos:
        html += f"""
        <tr>
        <td>{p[0]}</td>
        <td>{p[1]}</td>
        <td>{p[2]}</td>
        <td>{p[3]}</td>
        </tr>
        """

    html += "</table>"

    cur.close()
    conn.close()

    return html


if __name__ == "__main__":
    init_db()
    app.run(host="0.0.0.0", port=5000)