import os
import psycopg2
import streamlit as st
import pandas as pd
import random
from datetime import datetime


st.title("Dashboard de Eventos")

db_host = os.getenv("DB_HOST", "localhost")
db_port = os.getenv("DB_PORT", "5432")
db_user = os.getenv("DB_USER", "user")
db_pass = os.getenv("DB_PASSWORD", "password")
db_name = os.getenv("DB_NAME", "el_trebol")

try:
    conn = psycopg2.connect(
        host=db_host,
        port=db_port,
        user=db_user,
        password=db_pass,
        dbname=db_name
    )
    st.success("Conexión a la base de datos exitosa")
except Exception as e:
    st.error(f"Error al conectar a la base de datos: {e}")
    st.stop()



