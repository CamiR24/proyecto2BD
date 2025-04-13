from db import db_conection
from psycopg2 import sql

def cleaning_registers():
    conn = None
    cur = None
    try:
        conn = db_conection()
        cur = conn.cursor()
        cur.execute("DELETE FROM detalle_reservas")
        conn.commit()
        # Obtenemos la cantidad de filas afectadas
        rowcount = cur.rowcount
        return f"[✅ Se eliminaron {rowcount} registros de la tabla]"
    except Exception as e:
        if conn:
            conn.rollback()
        return f"[❌ Error al limpiar los registros: {e}]"
    finally:
        if cur:
            cur.close()
        if conn:
            conn.close()


