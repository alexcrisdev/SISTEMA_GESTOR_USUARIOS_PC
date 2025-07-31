import logging
from datetime import datetime
from typing import List, Optional
from db.conexion_db import ConexionDB
from models.model_usuareacomp import UsuAreaComp
from models.model_usuario import Usuario
from models.model_area import Area
from models.model_computadora import *
from mysql.connector import Error

logger = logging.getLogger(__name__)

class UsuAreaCompDAO:
    def __init__(self, conexion: ConexionDB):
        self.conexion = conexion

    def insertar_UsuAreaComp_DAO(self, usu_area_comp: UsuAreaComp) -> bool:
        if not isinstance(usu_area_comp, UsuAreaComp):
            logger.error("Tipo de dato inválido: Se esperaba un objeto de la clase UsuAreaComp")
            raise TypeError("Se espera un objeto de la clase UsuAreaComp")
        
        query = """
            INSERT INTO USUAREACOMP(IdUsuario, IdComputadora, IdArea, FechaInicio, FechaFin)
            VALUES(%s,%s,%s,%s,%s)
        """
        valores = (usu_area_comp.usuario.id_usuario, usu_area_comp.computadora.id_computadora, usu_area_comp.area.id_area,
                   usu_area_comp.fecha_inicio, usu_area_comp.fecha_fin)

        try:
            with self.conexion.obtener_cursor() as cursor:
                cursor.execute(query, valores)
                self.conexion.commit()
                logger.info("Registrado insertado correctamente")
                return True
        except Error as e:
            self.conexion.rollback()
            logger.error(f"Error al insertar el registro: {e}")
            return False
        
    def actualizar_UsuAreaComp_DAO(self, usu_area_comp: UsuAreaComp) -> bool:
        if not isinstance(usu_area_comp, UsuAreaComp):
            logger.error("Tipo de dato inválido: Se esperaba un objeto de la clase UsuAreaComp")
            raise TypeError("Se espera un objeto de la clase UsuAreaComp")
        
        query = """
            UPDATE USUAREACOMP SET FechaInicio = %s, FechaFin = %s 
            WHERE IdUsuario = %s AND IdComputadora = %s AND IdArea = %s
        """
        valores = (usu_area_comp.fecha_inicio, usu_area_comp.fecha_fin, usu_area_comp.usuario.id_usuario,
                   usu_area_comp.computadora.id_computadora, usu_area_comp.area.id_area)
        
        try:
            with self.conexion.obtener_cursor() as cursor:
                cursor.execute(query, valores)
                self.conexion.commit()
                if cursor.rowcount > 0:
                    logger.info("Registro actualizado correctamente")
                    return True
                else:
                    logger.warning("No se encontró el registro")
                    return False
        except Error as e:
            self.conexion.rollback()
            logger.error(f"Error al actualizar el registro: {e}")
            return False
        
    def eliminar_UsuAreaComp_DAO(self, usuario: Usuario, area: Area, computadora: Computadora) ->bool:
        query = "DELETE FROM USUAREACOMP WHERE IdUsuario = %s AND IdComputadora = %s AND IdArea = %s"
        valores = (usuario.id_usuario, computadora.id_computadora, area.id_area)

        try:
            with self.conexion.obtener_cursor() as cursor:
                cursor.execute(query, valores)
                self.conexion.commit()
                if cursor.rowcount > 0:
                    logger.info(f"Registro eliminado correctamente")
                    return True
                else:
                    logger.warning("Registro no encontrado")
                    return False
        except Error as e:
            self.conexion.rollback()
            logger.error(f"Error al eliminar el registro: {e}")
            return False

    def obtener_UsuAreaComp_por_id_DAO(self, usuario: Usuario, area: Area, computadora: Computadora) -> Optional[UsuAreaComp]:
        query = """
            SELECT FechaInicio, FechaFin
            FROM USUAREACOMP
            WHERE IdUsuario = %s AND IdComputadora = %s AND IdArea = %s
        """
        valores = (usuario.id_usuario, computadora.id_computadora, area.id_area)

        try:
            with self.conexion.obtener_cursor() as cursor:
                cursor.execute(query, valores)
                resultado = cursor.fetchone()
                if resultado:
                    logger.info(f"Asignación encontrado")
                    return UsuAreaComp(**resultado)
                else:
                    logger.warning(f"Asignación no encontrada")
                    return None
        except Error as e:
            logger.error(f"Error al obtener el registro: {e}")
            return None


    def obtener_todos_UsuAreaComp_DAO(self) -> List[UsuAreaComp]:
        query = "SELECT IdUsuario, IdComputadora, IdArea, FechaInicio, FechaFin FROM USUAREACOMP"
        registros = []

        try:
            with self.conexion.obtener_cursor() as cursor:
                cursor.execute(query)
                resultados = cursor.fetchall()
                logger.info(f"{len(resultados)} asignaciones encontrados")
                return [UsuAreaComp(**fila) for fila in resultados] if resultados else []
        except Error as e:
            logger.error(f"Error al obtener todos los registros: {e}")
            return []


    def existe_UsuAreaComp_DAO(self, usuario: Usuario, area: Area, computadora: Computadora) -> bool:
        query = """
            SELECT 1 FROM USUAREACOMP
            WHERE IdUsuario = %s AND IdComputadora = %s AND IdArea = %s
            LIMIT 1
        """
        valores = (usuario.id_usuario, computadora.id_computadora, area.id_area)

        try:
            with self.conexion.obtener_cursor() as cursor:
                cursor.execute(query, valores)
                resultado = cursor.fetchone()
                if resultado:
                    logger.info(f"Registro encontrado")
                    return True
                else:
                    logger.warning(f"Registro no encontrada")
                    return False
        except Error as e:
            logger.error(f"Error al verificar existencia del registro: {e}")
            return False

        

