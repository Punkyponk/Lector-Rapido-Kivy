CREATE DATABASE LibroKivy;
CREATE USER 'HADES'@'localhost' IDENTIFIED BY 'vivaelhentai';
GRANT ALL PRIVILEGES ON LibroKivy.* TO 'HADES'@'localhost';
FLUSH PRIVILEGES;

USE LibroKivy;

---Tabla Contador
---Esta tabla se puede actualizar cada vez que nosotros generamos el reporte
CREATE TABLE contador(
      id_contador INT (3) AUTO_INCREMENT PRIMARY KEY, ---Diferencia lps registros
      fecha DATE NOT NULL, -- Se guarda exactamente el dia que presionamos el boton de reporte
      cont_siguiente INT (3)NOT NULL, ---Este atributo cuenta las veces que pulso el boton siguiente
      cont_regresar INT (3) NOT NULL,   ---Este atributo cuenta las veces que pulso regresar
      pag_retomar INT (3) NOT NULL ---Este  atributo señala la pagina de donde se va a retomar la lectura
)ENGINE=InnoDB;


-- LIbro
---Esta tabla contiene todas las lineas de un libro que se leyo en formato .txt
CREATE TABLE libro(
      num_linea INT (3) AUTO_INCREMENT PRIMARY KEY, 
      linea VARCHAR (30) NOT NULL
)ENGINE=InnoDB;
