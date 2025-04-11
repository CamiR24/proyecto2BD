import streamlit as st
import psycopg2.extensions
from simulation import reservar, simular_concurrencia
from db import db_conection
import pandas as pd
import time

st.set_page_config(page_title="Simulador de Reservas", layout="centered")
st.title("Dashboard de Reservas")

# --- Conexión a la BD
try:
    conn = db_conection(psycopg2.extensions.ISOLATION_LEVEL_READ_COMMITTED)
    cur = conn.cursor()

    # --- Obtener asientos
    cur.execute("SELECT id, numero_asiento, seccion FROM asientos ORDER BY numero_asiento")
    asientos = cur.fetchall()

    if asientos:
        opciones = {f"Asiento {a[1]} - {a[2]} (ID {a[0]})": a[0] for a in asientos}
        seleccion = st.selectbox("Selecciona un asiento:", list(opciones.keys()))
        asiento_id = opciones[seleccion]

        st.markdown("### Configuración de Simulación")
        num_hilos = st.slider("Cantidad de usuarios (hilos)", 1, 30, 5)
        nivel_aislamiento = st.selectbox("Nivel de aislamiento", ["read_committed", "repeatable_read", "serializable"])

        col1, col2 = st.columns(2)

        # Reservar individualmente
        if col1.button("Reservar individualmente"):
            resultado = reservar(id_usuario=1, id_asiento=asiento_id, isolation=nivel_aislamiento)
            st.info(f"Resultado individual: {resultado}")

        # Ejecutar concurrencia
        if col2.button("Simular concurrencia"):
            st.warning("Simulación en proceso, por favor espera...")
            inicio = time.time()
            resultados = simular_concurrencia(asiento_id, num_hilos, nivel_aislamiento)
            fin = time.time()

            df_resultados = pd.DataFrame({"Resultado": resultados})
            st.success(f"Simulación terminada en {round(fin - inicio, 2)} segundos")
            st.dataframe(df_resultados)

    else:
        st.warning("⚠️ No hay asientos disponibles en la base de datos.")
    cur.close()
    conn.close()
except Exception as e:
    st.error(f"❌ Error al conectar a la base de datos: {e}")
    st.stop()