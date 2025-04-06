
-- Insertar evento
INSERT INTO eventos (nombre, fecha, asientos_disponibles)
VALUES ('Super Bowl 2025', '2025-04-21 18:30:00', 10);

-- Insertar tipos de boletos
INSERT INTO tipo_boletos (nombre, precio, id_evento)
VALUES 
  ('General', 25.00, 1),
  ('Preferencial', 60.00, 1);

-- Insertar usuarios
INSERT INTO usuarios (id, nombre, email, telefono)
VALUES 
  (1,'Antonio Rivera', 'antonio1@correo.com', '555-1001'),
  (2,'Beatriz Cruz', 'beatriz2@correo.com', '555-1002'),
  (3,'Carlos Solís', 'carlos3@correo.com', '555-1003'),
  (4,'Diana Molina', 'diana4@correo.com', '555-1004'),
  (5,'Ernesto Ruiz', 'ernesto5@correo.com', '555-1005'),
  (6,'Fabiola Jiménez', 'fabiola6@correo.com', '555-1006'),
  (7,'Gerardo Salas', 'gerardo7@correo.com', '555-1007'),
  (8,'Helena Vargas', 'helena8@correo.com', '555-1008'),
  (9,'Iván Cortés', 'ivan9@correo.com', '555-1009'),
  (10,'Julia Herrera', 'julia10@correo.com', '555-1010'),
  (11,'Kevin Zamora', 'kevin11@correo.com', '555-1011'),
  (12,'Laura Méndez', 'laura12@correo.com', '555-1012'),
  (13,'Marco Ortiz', 'marco13@correo.com', '555-1013'),
  (14,'Nadia León', 'nadia14@correo.com', '555-1014'),
  (15,'Ricardo Arturo', 'ric15@correo.com', '555-1015'),
  (16,'Paula Alfaro', 'paula16@correo.com', '555-1016'),
  (17,'Quetzal García', 'quetzal17@correo.com', '555-1017'),
  (18,'Raúl Esquivel', 'raul18@correo.com', '555-1018'),
  (19,'Sandra López', 'sandra19@correo.com', '555-1019'),
  (20,'Tomás Fuentes', 'tomas20@correo.com', '555-1020'),
  (21,'Peque Rrito', 'peque21@correo.com', '555-1021'),
  (22,'Úrsula Ramos', 'ursula22@correo.com', '555-1022'),
  (23,'Víctor Blanco', 'victor23@correo.com', '555-1023'),
  (24,'Wendy Rosales', 'wendy24@correo.com', '555-1024'),
  (25,'Ximena Guzmán', 'ximena25@correo.com', '555-1025'),
  (26,'Yahir Trejo', 'yahir26@correo.com', '555-1026'),
  (27,'Zulema Castillo', 'zulema27@correo.com', '555-1027'),
  (28,'Ángel Medina', 'angel28@correo.com', '555-1028'),
  (29,'Bárbara Flores', 'barbara29@correo.com', '555-1029'),
  (30,'César Bravo', 'cesar30@correo.com', '555-1030');

-- Insertar 10 asientos (4 reservados)
INSERT INTO asientos (id, numero_asiento, seccion, estado, id_tipo_boleto)
VALUES 
  (1,101,'General Norte', TRUE, 1),
  (2,102,'General Norte', TRUE, 1),
  (3,103,'General Norte', TRUE, 1),
  (4,104,'General Norte', FALSE, 1),
  (5,105,'General Norte', FALSE, 1),
  (6,201,'Preferencial Sur', TRUE, 2),
  (7,202,'Preferencial Sur', FALSE, 2),
  (8,203,'Preferencial Sur', FALSE, 2),
  (9,204,'Preferencial Sur', FALSE, 2),
  (10,205,'Preferencial Sur', FALSE, 2);

-- Insertar 4 reservas iniciales
INSERT INTO reservas (fecha_reserva, estado, id_usuario)
VALUES 
  ('2025-04-01 08:00:00', 1),
  ('2025-04-01 08:10:00', 2),
  ('2025-04-01 08:20:00', 3),
  ('2025-04-01 08:30:00', 4);

-- Asignar esos asientos en detalle_reservas
INSERT INTO detalle_reservas (id_asiento, id_reserva)
VALUES 
  (1, 1),
  (2, 2),
  (3, 3),
  (6, 4);
