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

        time.sleep(random.uniform(0.1, 0.5))  # Simular concurrencia

        #Lock explícito sobre la fila del asiento
        try :
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
            return f"[{id_usuario}] Reserva exitosa para asiento {id_asiento}"
        
        except Exception as e:
            conn.rollback()
            return f"[{id_usuario}] Asiento ya reservado"

    except Exception as e:
        conn.rollback()
        return f"[{id_usuario}] Error durante la reserva: {e}"
    
    finally:
        cur.close()
        conn.close()


def simular_concurrencia(asientos_disponibles, num_usuarios, isolation):
    threads = []
    resultados = []
    tiempos = []
    exitos = 0
    fracasos = 0

    # un usuario reserva un asiento aleatorio de los disponibles
    def tarea(id_usuario):
        nonlocal exitos, fracasos
        id_asiento = random.choice(asientos_disponibles)
        inicio = time.time()
        resultado = reservar(id_usuario, id_asiento, isolation)
        fin = time.time()
        duracion = (fin-inicio) * 1000 
        tiempos.append(duracion)
        resultados.append(resultado)
        if "exitosa" in resultado:
            exitos += 1
        else:
            fracasos += 1

    for i in range(num_usuarios):
        t = threading.Thread(target=tarea, args=(i+1,))
        threads.append(t)
        t.start()

    for t in threads:
        t.join()

    tiempo_promedio = round(sum(tiempos)/len(tiempos),2) if tiempos else 0

    return resultados, exitos, fracasos, tiempo_promedio

