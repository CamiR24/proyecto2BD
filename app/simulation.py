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

        time.sleep(random.uniform(0.1, 0.9))  # Simular concurrencia

        #Lock explícito sobre la fila del asiento
        try :
            cur.execute("SELECT * FROM asientos WHERE id = %s FOR UPDATE NOWAIT", (id_asiento,))

            time.sleep(random.uniform(0.4, 0.7))

            cur.execute(
                "INSERT INTO reservas (id_usuario, fecha_reserva, id_evento) VALUES (%s, now(), %s) RETURNING id", 
                (id_usuario, 1)
            )
            id_reserva = cur.fetchone()[0]

            # Asociar asiento
            cur.execute(
                "INSERT INTO detalle_reservas (id_reserva, id_asiento) VALUES (%s, %s)", 
                (id_reserva, id_asiento)
            )

            conn.commit()
            return f"[{id_usuario}] ✅ Reserva exitosa para asiento {id_asiento}"
        
        except Exception as e:
            conn.rollback()
            return f"[{id_usuario}] ❌ Asiento ya reservado"

    except Exception as e:
        conn.rollback()
        return f"[{id_usuario}] ❌ Error durante la reserva: {e}"
    
    finally:
        cur.close()
        conn.close()


def simular_concurrencia(asiento_id, num_usuarios, isolation):
    threads = []
    resultados = []
    exitos = 0
    fracasos = 0

    def tarea(id_usuario):
        nonlocal exitos, fracasos
        resultado = reservar(id_usuario, asiento_id, isolation)
        resultados.append(resultado)
        if "✅" in resultado:
            exitos += 1
        else:
            fracasos += 1

    for i in range(num_usuarios):
        t = threading.Thread(target=tarea, args=(i+1,))
        threads.append(t)
        t.start()

    for t in threads:
        t.join()

    return resultados, exitos, fracasos

