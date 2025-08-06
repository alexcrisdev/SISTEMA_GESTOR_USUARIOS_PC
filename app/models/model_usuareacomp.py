from typing import Optional, Union
from datetime import datetime, date

class UsuAreaComp:
    def __init__(self, id_usuario: str, id_area: int, id_computadora: str, fecha_inicio: Union[datetime,str], fecha_fin: Optional[Union[datetime,str]] = None):
        self.id_usuario = id_usuario
        self.id_area = id_area
        self.id_computadora = id_computadora
        self.fecha_inicio = fecha_inicio
        self.fecha_fin = fecha_fin
        self._validar_fechas()

    def _validar_fechas(self):
        if self.fecha_fin is not None and self.fecha_fin < self.fecha_inicio:
            raise ValueError("La fecha de fin no puede ser anterior a la fecha de inicio")

    @property
    def id_usuario(self) -> str:
        return self._id_usuario
    @id_usuario.setter
    def id_usuario(self, valor: str) -> None:
        if not isinstance(valor, str):
            raise TypeError("El id_usuario debe ser una cadena")
        self._id_usuario = valor

    @property
    def id_area(self) -> int:
        return self._id_area
    @id_area.setter
    def id_area(self, valor: int) -> None:
        if not isinstance(valor, int):
            raise TypeError("El id_area debe ser un entero")
        self._id_area = valor

    @property
    def id_computadora(self) -> str:
        return self._id_computadora
    @id_computadora.setter
    def id_computadora(self, valor: str) -> None:
        if not isinstance(valor, str):
            raise TypeError("El id_computadora debe ser un entero")
        self._id_computadora = valor        

    @property
    def fecha_inicio(self) -> datetime:
        return self._fecha_inicio
    @fecha_inicio.setter
    def fecha_inicio(self, valor: Union[datetime, str]) -> None:
        self._fecha_inicio = self._normalizar_fecha(valor, "inicio")

    @property
    def fecha_fin(self) ->Optional[datetime]:
        return self._fecha_fin
    @fecha_fin.setter
    def fecha_fin(self, valor: Optional[datetime]):
        self._fecha_fin = self._normalizar_fecha(valor, "fin") if valor is not None else None
        self._validar_fechas()   

    def _normalizar_fecha(self, valor: Union[datetime, date, str], campo: str) -> datetime:
        if isinstance(valor, datetime):
            return valor
        if isinstance(valor, date):
            return datetime.combine(valor, datetime.min.time())
        if isinstance(valor, str):
            try:
                return datetime.fromisoformat(valor)
            except ValueError:
                try:
                    return datetime.strptime(valor, '%Y-%m-%d %H:%M:%S')
                except ValueError:
                    return datetime.strptime(valor, '%Y-%m-%d')
        raise TypeError(f"Formato de fecha {campo} no soportado: {type(valor)}")

    def finalizar_asignacion(self) -> None:
        #Marca la fecha de fin cuando el usuario deja de usar la computadora.
        self.fecha_fin = datetime.now()

    def esta_activo(self) -> bool:
        #Indica si la asignación del usuario sigue activa (sin fecha de fin).
        return self.fecha_fin is None
    
    def to_dict(self):
        return {
            'id_usuario': self.id_usuario,
            'id_computadora': self.id_computadora,
            'id_area': self.id_area,
            'fecha_inicio': self.fecha_inicio.strftime("%Y-%m-%d"),
            'fecha_fin': self.fecha_fin.strftime("%Y-%m-%d") if self.fecha_fin else None
        }
