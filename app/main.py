import streamlit as st
import pandas as pd
import random
import os
from datetime import datetime
from simulation import reservar
from db import db_conection
import psycopg2.extensions


st.title("Dashboard de Reservas")

# Conexion a la base de datos antes que nada
try:
    # se coloca un isolation level de prueba
    conn = db_conection(psycopg2.extensions.ISOLATION_LEVEL_READ_COMMITTED)
    st.success("Conexión a la base de datos exitosa")
    cur = conn.cursor()

    # Mostrar asientos 
    cur.execute("SELECT id, numero_asiento, seccion FROM asientos ORDER BY numero_asiento")
    asientos = cur.fetchall()

    if asientos:
        opciones = {f"Asiento {a[1]} - {a[2]} (ID {a[0]})": a[0] for a in asientos}
        seleccion = st.selectbox("Selecciona un asiento para reservar:", list(opciones.keys()))
        asiento_id = opciones[seleccion]

        if st.button("Reservar este asiento"):
            resultado = reservar(id_usuario=1, id_asiento=asiento_id, isolation='serializable')
            st.info(resultado)
    else:
        st.warning(" No hay asientos disponibles para reservar.")
    cur.close()
    conn.close()
except Exception as e:
    st.error(f" Error al conectar a la base de datos: {e}")
    st.stop()