import time
import psycopg2.extensions
import threading
from db import db_conection
import random

#Niveles a utilizar para las simulaciones
ISOLATION_LEVELS = {
    'read_committed': psycopg2.extensions.ISOLATION_LEVEL_READ_COMMITTED,
    'repeatable_read': psycopg2.extensions.ISOLATION_LEVEL_REPEATABLE_READ,
    'serializable': psycopg2.extensions.ISOLATION_LEVEL_SERIALIZABLE
}

def reservar(id_usuario, id_asiento, isolation):
    try: 
        conn = db_conection(ISOLATION_LEVELS[isolation])
        cur = conn.cursor()
        conn.autocommit = False

        time.sleep(random.uniform(0.1,0.4)) # retraso entre hilos

        # Verifica que si el asiento ya está reservado para el evento 
        cur.execute("""
            SELECT 1 
            FROM detalle_reservas dr
            JOIN reservas r ON dr.id_reserva = r.id 
            WHERE dr.id_asiento = %s AND r.id_evento = %s
            FOR UPDATE
            """,(id_asiento, 1))
        
        if cur.fetchone():
            conn.rollback()
            return f"[{id_usuario}] -> Asiento ya reservado"
        else:
            # Crear reserva
            cur.execute("INSERT INTO reservas (id_usuario, fecha_reserva, id_evento) VALUES (%s, now(), %s) RETURNING id", (id_usuario,1))
            id_reserva = cur.fetchone()[0]

            # Relacionar con asiento
            cur.execute("INSERT INTO detalle_reservas (id_reserva, id_asiento) VALUES (%s, %s)", (id_reserva, id_asiento))

            # Marcar asiento como ocupado
            cur.execute("UPDATE asientos SET estado = TRUE WHERE id = %s", (id_asiento,))

            conn.commit()
            return f"[{id_usuario}] -> Reserva exitosa para el asiento {id_asiento}"

                    
    except Exception as e:
        conn.rollback()
        return f" Error durante la reserva: {e}"
    finally:
        cur.close()
        conn.close()

