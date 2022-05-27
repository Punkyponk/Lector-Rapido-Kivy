CREATE DATABASE LibroKivy;
CREATE USER 'HADES'@'localhost' IDENTIFIED BY 'vivaelhentai';
GRANT ALL PRIVILEGES ON LibroKivy.* TO 'HADES'@'localhost';
FLUSH PRIVILEGES;

USE LibroKivy;

---Tabla Contador
---Esta tabla se puede actualizar cada vez que nosotros generamos el reporte
CREATE TABLE contador(
    id_contador INT (3) PRIMARY KEY, ---Diferencia los registros
    pag_retomar INT (3) NOT NULL, ---Este  atributo señala la página de donde se va a retomar la lectura
    cont_regresar INT (3) NOT NULL, ---Este atributo cuenta las veces que pulso el bóton "Regresar"
    cont_continuar INT (3) NOT NULL, ---Este atributo cuenta las veces que pulso el botón "Continuar"
    fin_lectura DATETIME NOT NULL ---Se guarda exactamente el dia y hora en que presionamos el botón de reporte
)ENGINE=InnoDB

---Libro
---Esta tabla contiene todas las lineas de un libro que se leyo en formato .txt
CREATE TABLE libro(
    num_linea INT (3) PRIMARY KEY, 
    linea VARCHAR (70) NOT NULL
)ENGINE=InnoDB;
