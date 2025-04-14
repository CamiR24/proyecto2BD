import streamlit as st
from cleaning_registers import cleaning_registers
import psycopg2.extensions
from simulation import reservar, simular_concurrencia
from db import db_conection
import pandas as pd
import time
from table import table, obtener_detalles

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
        num_hilos = st.slider("Cantidad de usuarios (hilos)", 1, 30, 10)
        nivel_aislamiento = st.selectbox("Nivel de aislamiento", ["read_committed", "repeatable_read", "serializable"])

        col1, col2, col3, col4 = st.columns(4)

        # Reservar individualmente
        if col1.button("Reservar individualmente"):
            resultado = reservar(id_usuario=1, id_asiento=asiento_id, isolation=nivel_aislamiento)
            st.info(f"Resultado individual: {resultado}")

        # Ejecutar concurrencia
        if col2.button("Simular concurrencia"):
            st.warning("Simulación en proceso, por favor espera...")
            inicio = time.time()
            resultados, exitos, fracasos = simular_concurrencia(asiento_id, num_hilos, nivel_aislamiento)
            fin = time.time()
            tiempo_simulacion = round(fin - inicio, 2)
            
            df_resultados = pd.DataFrame({"Resultado": resultados})
            st.success(f"Simulación terminada en {tiempo_simulacion} segundos")
            st.dataframe(df_resultados)
            st.info(f"Número de éxitos: {exitos}")
            st.info(f"Número de fracasos: {fracasos}")
            
            mensaje_insercion = table(nivel_aislamiento, tiempo_simulacion, exitos, fracasos, num_hilos)
            st.info(mensaje_insercion)


        if col3.button("Borrar registros para una nueva simulacion"):
            st.warning("Eliminación en proceso...")
            mensaje = cleaning_registers()
            st.info(mensaje)

        if col4.button("Mostrar registros de simulación"):
            df_detalles = obtener_detalles()
            if df_detalles is not None and not df_detalles.empty:
                st.dataframe(df_detalles)
        else:
            st.warning("No se encontraron registros en la tabla detalles_simulacion.")

        
    else:
        st.warning("⚠️ No hay asientos disponibles en la base de datos.")
    cur.close()
    conn.close()
except Exception as e:
    st.error(f"❌ Error al conectar a la base de datos: {e}")
    st.stop()