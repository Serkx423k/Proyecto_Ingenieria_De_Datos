create table genero (
  id_genero int primary key,
  nombre_genero varchar(50)
);


create table consola (
  id_consola int,	
  nombre_consola varchar(30),	
  fecha_lanzamiento date,
  empresa varchar (20),
  primary key (id_consola)
);


create table desarrolladora (
  id_desarrolladora int primary key,
  nombre_desarrolladora varchar(50)
);


create table videojuego(
  id_videojuego int,
  id_genero int,
  nombre_videojuego varchar(200),
  primary key (id_videojuego),
  foreign key (id_genero) references genero(id_genero)
);

create table version_videojuego(
  id_version int,
  nombre_videojuego varchar (200),
  ano_lanzamiento int,
  id_desarrolladora int,
  id_videojuego_base int,
  primary key (id_version),
  foreign key (id_videojuego_base) references videojuego(id_videojuego),
  foreign key (id_desarrolladora) references desarrolladora(id_desarrolladora)
  
);




create table requiere (
  id_videojuego int,
  id_consola int,
  primary key (id_videojuego),
  foreign key (id_consola) references consola(id_consola),
  foreign key (id_videojuego) references version_videojuego(id_version)
);


create table venta (
  id_version_videojuego int,
  id_venta int,
  ventas_na	numeric(10,2),
  ventas_eu	numeric(10,2),
  ventas_jp	numeric(10,2),
  otras_ventas numeric(10,2),
  ventas_globales numeric(10,2),
  primary key (id_venta),
  foreign key (id_version_videojuego) references version_videojuego(id_version)
);



COPY genero (id_genero, nombre_genero)
FROM 'C:\Users\Laboratorios EICT\Downloads\Proyecto_Ingenieria_De_Datos-main\Proyecto_Ingenieria_De_Datos-main\csv\genero.csv'
WITH DELIMITER ',' CSV HEADER;

COPY desarrolladora (id_desarrolladora, nombre_desarrolladora)
FROM 'C:\Users\Laboratorios EICT\Downloads\Proyecto_Ingenieria_De_Datos-main\Proyecto_Ingenieria_De_Datos-main\csv\desarrolladora.csv'
WITH DELIMITER ',' CSV HEADER;

COPY consola (id_consola, nombre_consola, fecha_lanzamiento, empresa)
FROM 'C:\Users\Laboratorios EICT\Downloads\Proyecto_Ingenieria_De_Datos-main\Proyecto_Ingenieria_De_Datos-main\csv\consola.csv'
WITH DELIMITER ',' CSV HEADER;

COPY videojuego (id_videojuego, id_genero, nombre_videojuego)
FROM 'C:\Users\Laboratorios EICT\Downloads\Proyecto_Ingenieria_De_Datos-main\Proyecto_Ingenieria_De_Datos-main\csv\videojuego.csv' 
WITH DELIMITER ',' CSV HEADER;




COPY version_videojuego (id_version, nombre_videojuego, ano_lanzamiento, id_desarrolladora, id_videojuego_base)
FROM 'C:\Users\Laboratorios EICT\Downloads\Proyecto_Ingenieria_De_Datos-main\Proyecto_Ingenieria_De_Datos-main\csv\version_videojuego.csv' 
WITH DELIMITER ',' CSV HEADER;


COPY venta (id_version_videojuego, id_venta, ventas_na, ventas_eu, ventas_jp, otras_ventas, ventas_globales)
FROM 'C:\Users\Laboratorios EICT\Downloads\Proyecto_Ingenieria_De_Datos-main\Proyecto_Ingenieria_De_Datos-main\csv\venta.csv'
WITH DELIMITER ',' CSV HEADER;



COPY requiere (id_videojuego, id_consola)
FROM 'C:\Users\Laboratorios EICT\Downloads\Proyecto_Ingenieria_De_Datos-main\Proyecto_Ingenieria_De_Datos-main\csv\requiere.csv'
WITH DELIMITER ',' CSV HEADER



