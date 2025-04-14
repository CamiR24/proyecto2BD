import streamlit as st
from cleaning_registers import cleaning_registers
import psycopg2.extensions
from simulation import simular_concurrencia
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
    cur.execute("SELECT id, numero_asiento, id_tipo_boleto FROM asientos ORDER BY numero_asiento")
    asientos = cur.fetchall()

    if asientos:
        st.markdown("### Configuración de Simulación")
        num_hilos = st.slider("Cantidad de usuarios (hilos)", 1, 30, 10)
        nivel_aislamiento = st.selectbox("Nivel de aislamiento", ["read_committed", "repeatable_read", "serializable"])

        col1, col2, col3 = st.columns(3)

        # Ejecutar concurrencia
        if col1.button("Simular concurrencia"):
            st.warning("Simulación en proceso, por favor espera...")
            asientos_disponibles = [a[0] for a in asientos]
            inicio = time.time()
            resultados, exitos, fracasos, tiempo_promedio = simular_concurrencia(
                asientos_disponibles, num_hilos, nivel_aislamiento)
            fin = time.time()
            tiempo_simulacion = round((fin - inicio) * 1000, 2)  # en ms
            
            df_resultados = pd.DataFrame({"Resultado": resultados})
            st.success(f"Simulación terminada en {tiempo_simulacion} ms")
            st.dataframe(df_resultados)

            # Mostrar tabla resumen
            resumen_df = pd.DataFrame([{
                "Usuarios": num_hilos,
                "Nivel Aislamiento": nivel_aislamiento.upper(),
                "Éxitos": exitos,
                "Fallos": fracasos,
                "Tiempo Promedio (ms)": tiempo_promedio
            }])
            st.markdown("### Resumen de esta simulación")
            st.dataframe(resumen_df)

            # Insertar en tabla detalles_simulacion
            mensaje_insercion = table(nivel_aislamiento, tiempo_simulacion, exitos, fracasos, num_hilos)
            st.info(mensaje_insercion)

        # Borrar registros
        if col2.button("Borrar registros para una nueva simulación"):
            st.warning("Eliminación en proceso...")
            mensaje = cleaning_registers()
            st.info(mensaje)

        # Mostrar historial
        if col3.button("Mostrar registros de simulación"):
            df_detalles = obtener_detalles()
            if df_detalles is not None and not df_detalles.empty:
                st.dataframe(df_detalles)
            else:
                st.warning("No se encontraron registros en la tabla detalles_simulacion.")

    else:
        st.warning(" No hay asientos disponibles en la base de datos.")
    cur.close()
    conn.close()
except Exception as e:
    st.error(f"ERROR al conectar a la base de datos: {e}")
    st.stop()
