create Table Usuarios (
	id serial primary key,
	nombre varchar(100) not null,
	email varchar(150) not null unique,
	telefono varchar(100) not null unique
);

create Table Reservas (
	id serial primary key,
	fecha_reserva timestamp not null,
	estado varchar(100) not null,
	id_usuario int not null references Usuarios(id)
);

create Table Asientos (
	id serial primary key,
	numero_asiento int not null,
	seccion varchar(100) not null,
	id_tipo_boleto int not null references Tipo_boletos(id)
);

create Table Asientos_reservas (
	id_asiento int not null references Asientos(id),
	id_reserva int not null references Reservas(id)
);

create Table Tipo_boletos (
	id serial primary key,
	nombre varchar(100) not null,
	precio numeric(10,2) not null,
	id_evento int not null references Eventos(id)
);

create Table Eventos (
	id serial primary key,
	nombre varchar(100) not null,
	fecha timestamp not null,
	asientos_disponibles int not null
);