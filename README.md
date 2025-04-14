# 🪑 Proyecto 2 – ACID + Concurrencia

Este proyecto es un simulador académico desarrollado con **Python**, **PostgreSQL** y **Streamlit**, donde múltiples usuarios intentan reservar asientos al mismo tiempo. Se implementan **transacciones**, **niveles de aislamiento**, y concurrencia usando **hilos** para observar el comportamiento real del sistema ante posibles conflictos.

---

## 📦 Tecnologías utilizadas

- Python 3.11
- PostgreSQL 15+
- Streamlit
- Docker & Docker Compose
- psycopg2
- Concurrencia con threading

---

## 📁 Estructura del Proyecto
```
PROYECTO2BD/
├── app/
│   ├── cleaning_registers.py       # Elimina registros para nueva simulación
│   ├── db.py                       # Configura conexión a PostgreSQL
│   ├── main.py                     # Interfaz Streamlit
│   ├── simulation.py               # Simulación con hilos y concurrencia
│   └── table.py                    # Inserta resumen en la tabla detalles_simulacion
├── database/
│   ├── 1_ddl.sql                   # Script SQL para crear tablas
│   └── 2_data.sql                  # Datos iniciales
├── docker-compose.yml             # Orquestación con PostgreSQL y App
├── Dockerfile                     # Construye la imagen de la app
├── requirements.txt               # Dependencias Python
└── README.md                     
```
---

## ⚙️ Requisitos

- Docker  
- Docker Compose  
- Navegador (para abrir la interfaz)  
- (Opcional) Python 3.11+ si quieres correrlo sin Docker

---

## 🛠️ Instalación y ejecución con Docker

### 1. Clona el repositorio
```
git clone https://github.com/tu-usuario/PROYECTO2BD.git
cd PROYECTO2BD
```
### 2. Levanta el entorno completo
```
docker-compose up --build
```
### 3. Abre la interfaz web
```
http://localhost:8501
```
### 4. (Opcional) Si quieres reiniciar la BD desde cero
```
docker-compose down -v
docker-compose up --build
```
---

##  Cómo funciona internamente

- Cada hilo representa un usuario tratando de reservar un asiento aleatorio.
- Se usa una transacción por hilo con el nivel de aislamiento indicado.
- Si dos hilos intentan reservar el mismo asiento, solo uno tiene éxito (dependiendo del aislamiento).
- Se insertan los resultados y el resumen de cada simulación en la tabla detalles_simulacion.

---

## 🖱️ Botones disponibles en la app
```
| Botón                       | Función                                                    |
|-----------------------------|------------------------------------------------------------|
| Simular concurrencia        | Ejecuta la simulación con hilos e inserta resultados       |
| Borrar registros            | Limpia las reservas y permite nueva simulación limpia      |
| Mostrar registros históricos| Muestra todas las simulaciones guardadas                   |
```
---

## 📂 Scripts de base de datos

### 1_ddl.sql
Contiene toda la estructura de las tablas necesarias:
- eventos  
- tipo_boletos  
- usuarios  
- reservas  
- asientos  
- detalle_reservas  
- detalles_simulacion  

### 2_data.sql
Contiene datos iniciales:
- 30 asientos (10 por tipo)
- 30 usuarios
- 1 evento
- 3 tipos de boletos

---

## 👩‍💻 Autores
- Vianka Castro - 23201
- Ricardo Godínez - 23247
- Camila Ritcher - 23183

---
