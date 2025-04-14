from db import db_conection
import psycopg2.extensions

def cleaning_registers():
    conn = db_conection(psycopg2.extensions.ISOLATION_LEVEL_READ_COMMITTED)
    cur = conn.cursor()
    try:
        # Limpiar reservas en orden correcto
        cur.execute("DELETE FROM detalle_reservas;")
        cur.execute("DELETE FROM reservas;")

        # Reiniciar secuencias opcionalmente
        cur.execute("ALTER SEQUENCE reservas_id_seq RESTART WITH 1;")
        cur.execute("ALTER SEQUENCE detalle_reservas_id_seq RESTART WITH 1;")

        conn.commit()
        return f"Se eliminaron los registros de reservas correctamente."
    except Exception as e:
        conn.rollback()
        return f"ERROR al limpiar los registros: {e}"
    finally:
        cur.close()
        conn.close()


