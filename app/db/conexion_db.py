import logging #Imprimir mensajes de info, warning, error
#Cargar las variables de entorno
from dotenv import load_dotenv
import os
#Importar la librería MySQL
import mysql.connector
from mysql.connector import Error, MySQLConnection

#Configuar logging
logging.basicConfig(level=logging.INFO, format='[%(levelname)s] %(message)s')

#Cargar las variables desde .env
load_dotenv()

class ConexionDB:
    def __init__(self):
        self.host = os.getenv('DB_HOST', 'localhost')
        self.user = os.getenv('DB_USER')
        self.port = int(os.getenv('DB_PORT','3306'))
        self.password = os.getenv('DB_PASSWORD')
        self.database = os.getenv('DB_DATABASE')

        #Validar que ninguna variable sea None o esté vacía
        if not all([self.host, self.user, self.port, self.password, self.database]):
            raise ValueError("❌ Faltan variables de entorno requeridas para la conexión.")
        
        self.connection: MySQLConnection | None = None
        self.conectar()

    def conectar(self) -> None:
        #Establecer conexión con la base de datos
        if self.connection and self.connection.is_connected():
            return #Ya está conectado

        try:
            self.connection = mysql.connector.connect(
                host = self.host,
                user = self.user,
                port = self.port,
                password = self.password,
                database = self.database
            )
            if self.connection.is_connected():
                logging.info(f"Conectado a la base de datos: {self.database}")
        except Error as e:
            logging.error(f"Error al conectar con la base de datos: {self.database}")
            raise

    def cerrar(self) -> None:
        if self.connection and self.connection.is_connected():
            self.connection.close()
            logging.info("Conexión cerrada automáticamente")

    def obtener_cursor(self):
        try:
            if self.connection is None or not self.connection.is_connected():
                self.conectar()
            return self.connection.cursor(dictionary=True)
        except Error as e:
            logging.error(f"Error al obtener el cursor: {e}")
            raise     
    
    def commit(self):
        if self.connection and self.connection.is_connected():
            self.connection.commit()

    def rollback(self):
        if self.connection and self.connection.is_connected():
            self.connection.rollback()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        if exc_type:
            logging.error(f"Se produjo un error: {exc_value}")
        self.cerrar()