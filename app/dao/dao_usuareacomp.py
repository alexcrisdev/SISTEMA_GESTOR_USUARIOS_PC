import logging
from typing import List, Optional
from db.conexion_db import ConexionDB
from app.models.model_usuareacomp import UsuAreaComp
from mysql.connector import Error
from datetime import datetime

logger = logging.getLogger(__name__)

class UsuAreaCompDAO:
    def __init__(self, conexion: ConexionDB):
        self.conexion = conexion

    def insertar_UsuAreaComp_lote(self, lista_registros:List[UsuAreaComp]) -> bool:
        if not lista_registros:
            logger.warning("Lista de registros vacía")
            return False

        query = """
            INSERT INTO USUAREACOMP(IdUsuario, IdComputadora, IdArea, FechaInicio, FechaFin)
            VALUES (%s,%s,%s,%s,%s)
        """
        valores = [
            (r.id_usuario, r.id_computadora, r.id_area,
             r.fecha_inicio, r.fecha_fin)
            for r in lista_registros
        ]

        try:
            with self.conexion.obtener_cursor() as cursor:
                cursor.executemany(query,valores)
                self.conexion.commit()
                logger.info(f"Insertados {len(valores)} registros")
                return True
        except Error as e:
            self.conexion.rollback()
            logger.error(f"Error en inserción por lote: {e}")
            return False

    def insertar_UsuAreaComp_DAO(self, usu_area_comp: UsuAreaComp) -> bool:
        query = """
            INSERT INTO USUAREACOMP(IdUsuario, IdComputadora, IdArea, FechaInicio, FechaFin)
            VALUES(%s,%s,%s,%s,%s)
        """
        valores = (
            usu_area_comp.id_usuario, 
            usu_area_comp.id_computadora,
            usu_area_comp.id_area,
            usu_area_comp.fecha_inicio, 
            usu_area_comp.fecha_fin
        )

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
        
    def actualizar_UsuAreaComp_DAO(self, id_usuario: str, id_computadora: str, id_area: int, usu_area_comp: UsuAreaComp) -> bool:
        
        if not all([id_usuario, id_computadora, id_area]):
            logger.error("IDs incompletos para actualización")
            return False
        
        query = """
            UPDATE USUAREACOMP 
            SET FechaInicio = %s, FechaFin = %s 
            WHERE IdUsuario = %s AND IdComputadora = %s AND IdArea = %s
        """
        valores = (
            usu_area_comp.fecha_inicio,
            usu_area_comp.fecha_fin, 
            id_usuario,
            id_computadora, 
            id_area
        )
        
        try:
            with self.conexion.obtener_cursor() as cursor:
                cursor.execute(query, valores)
                self.conexion.commit()
                if cursor.rowcount == 0:
                    logger.warning("Ningún registro actualizado (¿IDs correctos?)")
                return cursor.rowcount > 0
        except Error as e:
            self.conexion.rollback()
            logger.error(f"Error al actualizar el registro: {e}")
            return False
        
    def eliminar_UsuAreaComp_DAO(self, id_usuario: str, id_computadora: str, id_area: int) ->bool:
        query = """
            DELETE FROM USUAREACOMP 
            WHERE IdUsuario = %s AND IdComputadora = %s AND IdArea = %s
        """
        valores = (id_usuario, id_computadora, id_area)

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

    def obtener_UsuAreaComp_por_id_DAO(self, id_usuario: str, id_computadora: str, id_area: int) -> Optional[UsuAreaComp]:
        query = """
            SELECT IdUsuario, IdComputadora, IdArea, FechaInicio, FechaFin
            FROM USUAREACOMP
            WHERE IdUsuario = %s AND IdComputadora = %s AND IdArea = %s
        """
        valores = (id_usuario, id_computadora, id_area)

        try:
            with self.conexion.obtener_cursor() as cursor:
                cursor.execute(query, valores)
                resultado = cursor.fetchone()
                if resultado:
                    logger.info(f"Asignación encontrado")
                    return UsuAreaComp(
                        id_usuario=resultado['IdUsuario'],
                        id_computadora=resultado['IdComputadora'],
                        id_area=resultado['IdArea'],
                        fecha_inicio=resultado['FechaInicio'],
                        fecha_fin=resultado['FechaFin']
                    )
                else:
                    logger.warning(f"Asignación no encontrada")
                    return None
        except Error as e:
            logger.error(f"Error al obtener el registro: {e}")
            return None

    def obtener_todos_UsuAreaComp_DAO(self) -> List[UsuAreaComp]:
        query = """
            SELECT 
            IdUsuario, IdComputadora, IdArea, FechaInicio, FechaFin
            FROM USUAREACOMP
        """        
        try:
            with self.conexion.obtener_cursor() as cursor:
                cursor.execute(query)
                filas = cursor.fetchall()
                logger.info(f'{len(filas)} asignaciones encontradas.')

                return [
                    UsuAreaComp(
                        id_usuario=fila['IdUsuario'],
                        id_computadora=fila['IdComputadora'],
                        id_area=fila['IdArea'],
                        fecha_inicio=fila['FechaInicio'],
                        fecha_fin = fila['FechaFin']
                    )
                    for fila in filas
                ]
        except Error as e:
            logger.error(f"Error al obtener todos los registros de asignaciones: {e}")
            return []

    def existe_UsuAreaComp_DAO(self, id_usuario: str, id_computadora: str, id_area: int) -> bool:
        query = """
            SELECT 1 FROM USUAREACOMP WHERE 
            IdUsuario = %s AND IdComputadora = %s AND IdArea = %s 
            LIMIT 1
        """
        valores = (id_usuario, id_computadora, id_area)

        try:
            with self.conexion.obtener_cursor() as cursor:
                cursor.execute(query, valores)
                return cursor.fetchone() is not None
        except Error as e:
            logger.error(f"Error al verificar existencia del registro: {e}")
            return False