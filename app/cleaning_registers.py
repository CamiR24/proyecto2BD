from db import db_conection

def cleaning_registers():
    conn = None
    cur = None
    try:
        conn = db_conection()
        cur = conn.cursor()
        cur.execute("DELETE FROM detalle_reservas")
        conn.commit()
        rowcount = cur.rowcount
        return f"[✅ Se eliminaron {rowcount} registros de la tabla detalle_reservas]"
    except Exception as e:
        if conn:
            conn.rollback()
        return f"[❌ Error al limpiar los registros: {e}]"
    finally:
        if cur:
            cur.close()
        if conn:
            conn.close()



