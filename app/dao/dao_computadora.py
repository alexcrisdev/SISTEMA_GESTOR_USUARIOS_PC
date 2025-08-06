import logging
from typing import List, Optional
from db.conexion_db import ConexionDB
from app.models.model_computadora import *
from mysql.connector import Error

logger = logging.getLogger(__name__)

class ComputadoraDAO:
    def __init__(self, conexion: ConexionDB):
        self.conexion = conexion

    def _validar_id(self, id_computadora: str) -> None:
        if not isinstance(id_computadora, str) or len(id_computadora) != 6:
            logger.error("ID no válido: debe ser una cadena de 6 caracteres.")
            raise ValueError("ID debe ser una cadena de 6 caracteres")

    def insertar_computadora_DAO(self, computadora: Computadora) -> bool:
        if not isinstance(computadora, Computadora):
            logger.error(f"Tipo de dato inválido: se esperaba un objeto Computadora.")
            raise TypeError("Se espera un objeto Computadora")
        
        query = """
            INSERT INTO COMPUTADORA(IdComputadora, ClaveComputadora, AccesoriosComputadora, CodigoKSDComputadora, TipoComputadora, RedComputadora)
            VALUES(%s,%s,%s,%s,%s,%s)
        """
        valores = (computadora.id_computadora, computadora.clave_computadora, computadora.accesorios_computadora,
                   computadora.codigo_ksd_computadora, computadora.tipo_computadora.value, computadora.red_computadora.value)
        
        try:
            with self.conexion.obtener_cursor() as cursor:
                cursor.execute(query, valores)
                self.conexion.commit()
                logger.info(f"Se creó correctamente la computadora con el ID: {computadora.id_computadora}")
                return True
        except Error as e:
            self.conexion.rollback()
            logger.error(f"Error al insertar la computadora: {e}")
            return False
        
    def insertar_computadoras_lote(self, lista_pc: List[Computadora]) -> bool:
        if not isinstance(lista_pc, list):
            logger.error("Tipo de dato inválido: Se esperaba una lista")
            raise TypeError("Se esperana una lista de usuarios")
        
        query = """
            INSERT INTO COMPUTADORA(IdComputadora, ClaveComputadora, AccesoriosComputadora, CodigoKSDComputadora, TipoComputadora, RedComputadora)
            VALUES(%s,%s,%s,%s,%s,%s)
        """
        valores = [(u["id_computadora"], u["clave_computadora"], u["accesorios_computadora"],
                    u["codigo_ksd_computadora"], u["tipo_computadora"], u["red_computadora"]) for u in lista_pc]
        
        try:
            with self.conexion.obtener_cursor() as cursor:
                cursor.executemany(query, valores)
                self.conexion.commit()
                logger.info(f'{len(lista_pc)} computadoras insertadas correctamente.')
                return True
        except Error as e:
            self.conexion.rollback()
            logger.error(f"Error al insertar computadoras en lote: {e}")
            return False

    def actualizar_computadora_DAO(self, nueva_computadora: Computadora, id_anterior: str) -> bool:
        if not isinstance(nueva_computadora, Computadora):
            logger.error("Tipo de dato inválido: Se esperaba un objeto de la clase computadora")
            raise TypeError("Se espera un objeto de la clase computadora")
        
        self._validar_id(id_anterior)

        query = """
            UPDATE COMPUTADORA SET
                IdComputadora = %s,
                ClaveComputadora = %s,
                AccesoriosComputadora = %s,
                CodigoKSDComputadora = %s,
                TipoComputadora = %s,
                RedComputadora = %s
            WHERE IdComputadora = %s
        """

        valores = (nueva_computadora.id_computadora, nueva_computadora.clave_computadora, nueva_computadora.accesorios_computadora,
                   nueva_computadora.codigo_ksd_computadora, nueva_computadora.tipo_computadora.value, nueva_computadora.red_computadora.value, id_anterior)

        try:
            with self.conexion.obtener_cursor() as cursor:
                cursor.execute(query, valores)
                self.conexion.commit()
                if cursor.rowcount > 0:
                    logger.info(f"Computadora actualizada: {id_anterior} -> {nueva_computadora.id_computadora}")
                    return True
                else:
                    logger.warning(f"No se encontró la computadora con ID: {id_anterior}")
                    return False
        except Error as e:
            self.conexion.rollback()
            logger.error(f"Error al actualizar computadora: {e}")
            return False
        
    def obtener_computadora_por_id_DAO(self, id_computadora: str) -> Optional[Computadora]:

        self._validar_id(id_computadora)

        try:
            with self.conexion.obtener_cursor() as cursor:
                cursor.execute("""SELECT 
                                IdComputadora as id_computadora,
                                ClaveComputadora as clave_computadora,
                                AccesoriosComputadora as accesorios_computadora,
                                CodigoKSDComputadora as codigo_ksd_computadora,
                                TipoComputadora as tipo_computadora,
                                RedComputadora as red_computadora
                                FROM COMPUTADORA WHERE IdComputadora = %s""",
                               (id_computadora,))
                fila = cursor.fetchone()
                if fila:
                    #Convierte strings a Enums automáticamente
                    fila["tipo_computadora"] = TipoComputadora(fila["tipo_computadora"])
                    fila["red_computadora"] = RedComputadora(fila["red_computadora"])
                    logger.info(f"Se obtuvo la computadora con el ID: {id_computadora}")
                    return Computadora(**fila)
                else:
                    logger.warning(f"No se encontró la computadora con el ID: {id_computadora}")
                    return None
        except Error as e:
            logger.error(f"Error al obtener por IDComputadora: {e}")
            return None        

    def obtener_todas_computadora_DAO(self) -> List[Computadora]:
        try:
            with self.conexion.obtener_cursor() as cursor:
                cursor.execute("""SELECT IdComputadora as id_computadora,
                               ClaveComputadora as clave_computadora,
                               AccesoriosComputadora as accesorios_computadora,
                               CodigoKSDComputadora as codigo_ksd_computadora,
                               TipoComputadora as tipo_computadora,
                               RedComputadora as red_computadora
                               FROM COMPUTADORA """)
                filas = cursor.fetchall()
                logger.info(f"{len(filas)} computadoras encontradas")
                return [
                    Computadora(
                        **{
                            **fila,
                            "tipo_computadora": TipoComputadora(fila["tipo_computadora"]),
                            "red_computadora": RedComputadora(fila["red_computadora"])
                        }
                    ) 
                    for fila in filas
                ] if filas else []
        except Error as e:
            logger.error(f"Error al obtener todas las computadoras: {e}")
            return []
        
    def eliminar_computadora_DAO(self, id_computadora: str) -> bool:
        self._validar_id(id_computadora)
        try:
            with self.conexion.obtener_cursor() as cursor:
                cursor.execute("DELETE FROM COMPUTADORA WHERE IdComputadora = %s", (id_computadora,))
                self.conexion.commit()
                if cursor.rowcount > 0:
                    logger.info(f"Computadora eliminada con el ID: {id_computadora}")
                    return True
                else:
                    logger.warning(f"Computadora no encontrada con el ID: {id_computadora}")
                    return False
        except Error as e:
            self.conexion.rollback()
            logger.error(f"Error al eliminar computadora: {e}")
            return False

    def existe_computadora_DAO(self, id_computadora: str) -> bool:
        self._validar_id(id_computadora)

        query = "SELECT 1 FROM COMPUTADORA WHERE IdComputadora = %s LIMIT 1"
        try:
            with self.conexion.obtener_cursor() as cursor:
                cursor.execute(query, (id_computadora, ))
                resultado = cursor.fetchone()
                if resultado:
                    logger.info(f"Computadora encontrado con el ID: {id_computadora}")
                    return True
                else:
                    logger.warning(f"Computadora no encontrada con el ID: {id_computadora}")
                    return False
        except Error as e:
            logger.error(f"Error al verificar existencia de la computadora: {e}")
            return False