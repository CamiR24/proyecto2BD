
-- 1. Crear la tabla Eventos
CREATE TABLE eventos (
    id serial PRIMARY KEY,
    nombre varchar(100) NOT NULL,
    fecha timestamp NOT NULL,
    asientos_disponibles int NOT NULL
);

-- 2. Crear la tabla Tipo_boletos, que depende de Eventos
CREATE TABLE tipo_boletos (
    id serial PRIMARY KEY,
    nombre varchar(100) NOT NULL,
    precio numeric(10,2) NOT NULL,
    id_evento int NOT NULL REFERENCES Eventos(id)
);

-- 3. Crear la tabla Usuarios
CREATE TABLE usuarios (
    id serial PRIMARY KEY,
    nombre varchar(100) NOT NULL,
    email varchar(150) NOT NULL UNIQUE,
    telefono varchar(100) NOT NULL UNIQUE
);

-- 4. Crear la tabla Reservas, que depende de Usuarios
CREATE TABLE reservas (
    id serial PRIMARY KEY,
    fecha_reserva timestamp NOT NULL,
    id_usuario int NOT NULL REFERENCES Usuarios(id)
);

-- 5. Crear la tabla Asientos, que depende de Tipo_boletos
CREATE TABLE asientos (
    id serial PRIMARY KEY,
    numero_asiento int NOT NULL,
    seccion varchar(100) NOT NULL,
    estado boolean NOT NULL DEFAULT FALSE,
    id_tipo_boleto int NOT NULL REFERENCES Tipo_boletos(id),
    UNIQUE (numero_asiento)  -- solo existe un asiento con ese numero
);

-- 6. Crear la tabla Detalle_reservas, que depende de Asientos y Reservas
CREATE TABLE detalle_reservas (
    id serial PRIMARY KEY,
    id_asiento int NOT NULL REFERENCES Asientos(id),
    id_reserva int NOT NULL REFERENCES Reservas(id),
    UNIQUE (id_asiento)  -- Un asiento no puede reservarse dos veces
);
