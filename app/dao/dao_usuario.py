import logging
from typing import List, Optional
from db.conexion_db import ConexionDB
from app.models.model_usuario import Usuario
from mysql.connector import Error

logger = logging.getLogger(__name__)

class UsuarioDAO:
    def __init__(self, conexion: ConexionDB):
        self.conexion = conexion

    def insertar_usuario_DAO(self, usuario: Usuario) -> bool:
        if not isinstance(usuario, Usuario):
            logger.error("Tipo de dato inválido: se esperaba un objeto Usuario.")
            raise TypeError("Se espera un objeto Usuario")
        
        query = """
            INSERT INTO USUARIO(IdUsuario, NombreUsuario, ApellidoUsuario, CorreoUsuario)
            VALUES(%s,%s,%s,%s)
        """
        valores = (usuario.id_usuario, usuario.nombre_usuario, usuario.apellido_usuario, usuario.correo_usuario)

        try:
             with self.conexion.obtener_cursor() as cursor:
                 cursor.execute(query, valores)
                 self.conexion.commit()
                 logger.info(f"Usuario insertado con ID: {usuario.id_usuario}")
                 return True
        except Error as e:
            self.conexion.rollback()
            logger.error(f"Error al insertar usuario: {e}")
            return False
    
    def insertar_usuarios_lote(self, lista_usuarios: List[dict]) -> bool:
        if not isinstance(lista_usuarios, list):
            logger.error("Tipo de dato inválido: Se esperaba una lista")
            raise TypeError("Se esperaba una lista de usuarios")
        
        query = """
            INSERT INTO USUARIO(IdUsuario, NombreUsuario, ApellidoUsuario, CorreoUsuario)
            VALUES(%s,%s,%s,%s)
        """
        datos = [(u["id_usuario"], u["nombre_usuario"], u["apellido_usuario"], u["correo_usuario"]) for u in lista_usuarios]
        
        try:
            with self.conexion.obtener_cursor() as cursor:
                cursor.executemany(query, datos)
                self.conexion.commit()
                logger.info("Lista de usuarios insertados correctamente")
                return True
        except Exception as e:
            self.conexion.rollback()
            logger.error(f"Error al insertar el lote de usuario: {e}")
            return False

    def actualizar_usuario_DAO(self, nuevo_usuario: Usuario, id_anterior: str) -> bool:
        if not isinstance(nuevo_usuario, Usuario):
            logger.error("Tipo de dato inválido: se esperaba un objeto Usuario.")
            raise TypeError("Se espera un objeto Usuario")
        
        if not id_anterior or len(id_anterior) != 8:
            logger.error("ID de usuario no válido (se espera 8 caracteres).")
            raise ValueError("ID de usuario no válido (se espera 8 caracteres).")
        
        query = """
            UPDATE USUARIO
            SET IdUsuario = %s, NombreUsuario = %s, ApellidoUsuario = %s, CorreoUsuario = %s
            WHERE IdUsuario = %s
        """
        
        valores = (
            nuevo_usuario.id_usuario,
            nuevo_usuario.nombre_usuario,
            nuevo_usuario.apellido_usuario,
            nuevo_usuario.correo_usuario,
            id_anterior
        )

        try:
            with self.conexion.obtener_cursor() as cursor:
                cursor.execute(query, valores)
                self.conexion.commit()
                if cursor.rowcount > 0:
                    logger.info(f"Usuario actualizado: {id_anterior} -> {nuevo_usuario.id_usuario}")
                    return True
                else:
                    logger.warning(f"No se encontró el usuario con ID: {id_anterior}")
                    return False
        except Error as e:
            self.conexion.rollback()
            logger.error(f"Error al actualizar ID del usuario: {e}")
            return False
        
    def eliminar_usuario_DAO(self, id_usuario: str) -> bool:
        if not id_usuario or len(id_usuario) != 8:
            logger.error("ID de usuario no válido (se espera 8 caracteres).")
            raise ValueError("ID de usuario no válido (se espera 8 caracteres).")
        
        query = "DELETE FROM USUARIO WHERE IdUsuario = %s"
        valor = (id_usuario, )

        try:
            with self.conexion.obtener_cursor() as cursor:
                cursor.execute(query, valor)
                self.conexion.commit()
                if cursor.rowcount > 0:
                    logger.info(f"Usuario eliminado con ID: {id_usuario}")
                    return True
                else:
                    logger.warning(f"No se encontró el usuario con ID: {id_usuario}")
                    return False
        except Error as e:
            self.conexion.rollback()
            logger.error(f"Error al eliminar el usuario: {e}")
            return False

    def obtener_usuario_por_id_DAO(self, id_usuario: str) -> Optional[Usuario]:        
        try:
            query = """
                SELECT
                    IdUsuario AS id_usuario,
                    NombreUsuario AS nombre_usuario,
                    ApellidoUsuario as apellido_usuario,
                    CorreoUsuario as correo_usuario
                FROM USUARIO
                WHERE IdUsuario = %s
            """
            valor = (id_usuario,)
            with self.conexion.obtener_cursor() as cursor:
                cursor.execute(query, valor)
                fila = cursor.fetchone()
                if fila:
                    logger.info(f"Usuario encontrado: {id_usuario}")
                    return Usuario(**fila)
                else:
                    logger.warning(f"Usuario no encontrado, ID: {id_usuario}")
                    return None
        except Error as e:
            logger.error(f"Error al obtener el usuario por ID: {e}")
            return None
                        
    def obtener_todos_usuario_DAO(self) -> List[Usuario]:
        query = """
            SELECT 
                IdUsuario AS id_usuario,
                NombreUsuario AS nombre_usuario,
                ApellidoUsuario as apellido_usuario,
                CorreoUsuario as correo_usuario
            FROM USUARIO
        """
        try:
            with self.conexion.obtener_cursor() as cursor:
                cursor.execute(query)
                filas = cursor.fetchall() #Almacenar todas las respuestas
                logger.info(f"{len(filas)} usuarios encontrados")
                return [Usuario(**fila) for fila in filas] if filas else []
        except Error as e:
            logger.error(f"Error al obtener todos los usuarios: {e}")
            return []

    def existe_usuario_DAO(self, id_usuario: str) -> bool:
        if not id_usuario or len(id_usuario) != 8:
            logger.error("ID de usuario no válido (se espera 8 caracteres).")
            raise ValueError("ID de usuario no válido (se espera 8 caracteres).")

        query = "SELECT 1 FROM USUARIOS WHERE IdUsuario = %s LIMIT 1"
        try:
            with self.conexion.obtener_cursor() as cursor:
                cursor.execute(query, (id_usuario))
                resultado = cursor.fetchone()
                if resultado:
                    logger.info(f"Área encontrado con el ID: {id_usuario}")
                    return True
                else:
                    logger.warning(f"Área no encontrada con el ID: {id_usuario}")
                    return False
        except Error as e:
            logger.error(f"Error al verificar existencia del usuario: {e}")
            return False