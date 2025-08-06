import logging
from typing import List, Optional
from db.conexion_db import ConexionDB
from app.models.model_area import Area
from mysql.connector import Error

logger = logging.getLogger(__name__)

class AreaDAO:
    def __init__(self, conexion: ConexionDB):
        self.conexion = conexion

    def insertar_area_DAO(self, area: Area) -> bool:
        if not isinstance(area, Area):
            logger.error(f"Tipo de dato inválido: se esperaba un objeto Area.")
            raise TypeError("Se espera un objeto Area")
        
        query = "INSERT INTO AREA(NombreArea) VALUES(%s)"
        valor = (area.nombre_area,)

        try:
            with self.conexion.obtener_cursor() as cursor:
                cursor.execute(query, valor)
                self.conexion.commit()
                area.id_area = cursor.lastrowid #Guarda el ID generado
                logger.info(f"Area insertado con ID: {area.id_area}")
                return True
        except Error as e:
            self.conexion.rollback()
            logger.error(f"Error al insertar el área: {e}")
            return False
        
    def insertar_area_lotes_DAO(self, lista_areas: List[Area]) -> bool:
            if not isinstance(lista_areas, List):
                logger.error(f"Tipo de dato inválido: se esperaba una lista")
                raise TypeError("Se esperaba una lista")
            
            query = "INSERT INTO AREA(NombreArea) VALUES (%s)"
            datos = [(u.nombre_area,) for u in lista_areas]
            try:
                with self.conexion.obtener_cursor() as cursor:
                    cursor.executemany(query, datos)
                    logger.info('Listas de áreas insertadas correctamente')    
                    self.conexion.commit()    
                    return True
            except Error as e:
                self.conexion.cerrar()
                logger.error({'error': 'Error al insertar las áreas'})
                return False

    def actualizar_area_DAO(self, area: Area, id_area: int) -> bool:
        if not isinstance(area, Area):
            logger.error(f"Tipo de dato inválido: se esperaba un objeto Area.")
            raise TypeError("Se espera un objeto Area")
        
        query = "UPDATE AREA SET NombreArea = %s WHERE IdArea = %s"
        valores = (area.nombre_area, id_area)

        try:
            with self.conexion.obtener_cursor() as cursor:
                cursor.execute(query, valores)
                self.conexion.commit()
                if cursor.rowcount > 0:
                    logger.info(f"Se actualizó el área con el ID: {id_area}")
                    return True
                else:
                    logger.warning(f"No se encontró el área con el ID: {id_area}")
                    return False
        except Error as e:
            self.conexion.rollback()
            logger.error(f"Error al actualizar el área: {e}")
            return False
        
    def eliminar_area_DAO(self, id_area: int) -> bool:
        if not isinstance(id_area, int):
            logger.error(f"Se espera un número")
            raise TypeError("Se espera un número")
        
        try:
            with self.conexion.obtener_cursor() as cursor:
                cursor.execute("DELETE FROM AREA WHERE IdArea = %s", (id_area,))
                self.conexion.commit()
                if cursor.rowcount > 0:
                    logger.info(f"Se eliminó el área con el ID: {id_area}")
                    return True
                else:
                    logger.warning(f"No se encontró el área con el ID: {id_area}")
                    return False
        except Error as e:
            self.conexion.rollback()
            logger.error(f"Error al eliminar el área: {e}")
            return False
        
    def obtener_area_por_id_DAO(self, id_area: int) -> Optional[Area]:
        if not isinstance(id_area, int):
            logger.error("Se esperaba un número del IdArea")
            raise TypeError("Se espera un número del idArea")
        
        try:
            with self.conexion.obtener_cursor() as cursor:
                cursor.execute("SELECT IdArea AS id_area, NombreArea as nombre_area FROM AREA WHERE IdArea = %s", (id_area,))
                fila = cursor.fetchone()
                if fila:
                    logger.info(f"Se obtuvo el area con el ID: {id_area}")
                    return Area(**fila)
                else:
                    logger.warning(f"No se encontró el área con el ID: {id_area}")
                    return None
        except Error as e:
            self.conexion.rollback()
            logger.error(f"Error al obtener el área por ID")
            return None
        
    def obtener_todos_area_DAO(self) -> List[Area]:
        try:
            with self.conexion.obtener_cursor() as cursor:
                cursor.execute("SELECT IdArea AS id_area, NombreArea as nombre_area FROM AREA")
                filas = cursor.fetchall()
                logger.info(f"{len(filas)} áreas encontradas")
                return [Area(**fila) for fila in filas] if filas else []
        except Error as e:
            logger.error(f"Error al obtener todas las áreas: {e}")
            return []
        
    def existe_area_DAO(self, id_area: str) -> bool:
        query = "SELECT 1 FROM AREA WHERE IdArea = %s LIMIT 1"
        try:
            with self.conexion.obtener_cursor() as cursor:
                cursor.execute(query, (id_area,))
                resultado = cursor.fetchone()
                if resultado:
                    logger.info(f"Área encontrado con el ID: {id_area}")
                    return True
                else:
                    logger.warning(f"Área no encontrada con el ID: {id_area}")
                    return False
        except Error as e:
            logger.error(f"Error al verificar existencia del area: {e}")
            return False