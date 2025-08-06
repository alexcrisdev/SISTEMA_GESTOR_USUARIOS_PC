CREATE DATABASE IF NOT EXISTS BD_GESTOR_USUARIOS
USE BD_GESTOR_USUARIOS

-- TABLA USUARIO
CREATE TABLE USUARIO(
	IdUsuario VARCHAR(8) PRIMARY KEY NOT NULL,
    NombreUsuario VARCHAR(50) NOT NULL,
    ApellidoUsuario VARCHAR(50) NOT NULL,
    CorreoUsuario VARCHAR(50) NOT NULL,
    
    CHECK(CHAR_LENGTH(IdUsuario) = 8),
    CHECK (CorreoUsuario REGEXP '^[^@]+@[^@]+\\.[^@]{2,}$')
);
-- TABLA COMPUTADORA
CREATE TABLE COMPUTADORA(
	IdComputadora VARCHAR(6) PRIMARY KEY NOT NULL,
    ClaveComputadora VARCHAR(8) NOT NULL UNIQUE,
    AccesoriosComputadora TEXT NOT NULL,
    CodigoKSDComputadora VARCHAR(20) NULL UNIQUE,
    TipoComputadora VARCHAR(20) NOT NULL,
    RedComputadora VARCHAR(20) NOT NULL,
    
    CHECK (TipoComputadora IN ('Servidor','Escritorio','Laptop')),
    CHECK (RedComputadora IN ('Dominio', 'Grupo_Trabajo'))
);
-- TABLA AREA
CREATE TABLE AREA(
	IdArea INT PRIMARY KEY AUTO_INCREMENT,
    NombreArea VARCHAR(30) NOT NULL UNIQUE
);
-- TABLA USUAREACOMP
CREATE TABLE USUAREACOMP(
	IdUsuario VARCHAR(8) NOT NULL,
    IdComputadora VARCHAR(6) NOT NULL,
    IdArea INT NOT NULL,
    FechaInicio DATE NOT NULL,
    FechaFin DATE NULL COMMENT 'NULL significa que la asignación está activa',
    
	CHECK(FechaFin IS NULL OR FechaFin > FechaInicio),
    PRIMARY KEY(IdUsuario, IdComputadora, IdArea),    
    
    FOREIGN KEY(IdUsuario) REFERENCES USUARIO(IdUsuario)
		ON UPDATE CASCADE
        ON DELETE CASCADE,
    
    FOREIGN KEY(IdComputadora) REFERENCES COMPUTADORA(IdComputadora)
		ON UPDATE CASCADE
        ON DELETE CASCADE,
    
    FOREIGN KEY(IdArea) REFERENCES AREA(IdArea)
		ON UPDATE CASCADE
        ON DELETE CASCADE
);