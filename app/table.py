from db import db_conection
import pandas as pd

def table(isolation, tiempo, succes, denied, usuarios):
    conn = None
    cur = None
    try:
        conn = db_conection()
        cur = conn.cursor()
        cur.execute(
            "INSERT INTO detalles_simulacion (nivel_aislamiento, usuarios, exitos, fracasos, tiempo) VALUES (%s, %s, %s, %s, %s)",
            (isolation, usuarios, succes, denied, tiempo)
        )
        conn.commit()
        return "[✅ Registro insertado correctamente]"
    except Exception as e:
        if conn:
            conn.rollback()
        return f"[❌ No se pudo insertar en la tabla: {e}]"
    finally:
        if cur:
            cur.close()
        if conn:
            conn.close()


def obtener_detalles():
    conn = None
    cur = None
    try:
        conn = db_conection()
        cur = conn.cursor()
        cur.execute("SELECT * FROM detalles_simulacion ORDER BY id DESC")
        registros = cur.fetchall()
        columnas = [desc[0] for desc in cur.description]
        df = pd.DataFrame(registros, columns=columnas)
        return df
    except Exception as e:
        print(f"Error al obtener registros: {e}")
        return None
    finally:
        if cur:
            cur.close()
        if conn:
            conn.close()