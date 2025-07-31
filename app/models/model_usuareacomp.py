from typing import Optional
from models.model_usuario import Usuario
from models.model_computadora import *
from models.model_area import Area
from datetime import datetime

class UsuAreaComp:
    def __init__(self, usuario: Usuario, area: Area, computadora: Computadora, fecha_inicio: datetime, fecha_fin: Optional[datetime] = None):
        self.usuario = usuario
        self.area = area
        self.computadora = computadora
        self.fecha_inicio = fecha_inicio
        self.fecha_fin = fecha_fin

    @property
    def usuario(self) -> Usuario:
        return self._usuario
    @usuario.setter
    def usuario(self, valor: Usuario) -> None:
        if not isinstance(valor, Usuario):
            raise TypeError("El usuario debe ser una instancia de la clase Usuario")
        self._usuario = valor

    @property
    def area(self) -> Area:
        return self._area
    @area.setter
    def area(self, valor: Area) -> None:
        if not isinstance(valor, Area):
            raise TypeError("El área debe ser una instancia de la clase Area")
        self._area = valor

    @property
    def computadora(self) -> Computadora:
        return self._computadora
    @computadora.setter
    def computadora(self, valor: Computadora) -> None:
        if not isinstance(valor, Computadora):
            raise TypeError("La computadora debe ser una instancia de la clase Computadora")
        self._computadora = valor        

    @property
    def fecha_inicio(self) -> datetime:
        return self._fecha_inicio
    @fecha_inicio.setter
    def fecha_inicio(self, valor: datetime) -> None:
        if not isinstance(valor, datetime):
            raise TypeError("La fecha de inicio debe ser de tipo datetime")
        self._fecha_inicio = valor

    @property
    def fecha_fin(self) ->Optional[datetime]:
        return self._fecha_fin
    @fecha_fin.setter
    def fecha_fin(self, valor: Optional[datetime]):
        if valor is not None and not isinstance(valor, datetime):
            raise TypeError("La fecha de fin debe ser None o de tipo datetime")
        if valor and hasattr(self, '_fecha_inicio') and valor < self._fecha_inicio:
            raise ValueError("La fecha de fin no puede ser anterior a la fecha de inicio")
        self._fecha_fin = valor 

    def finalizar_asignacion(self) -> None:
        #Marca la fecha de fin cuando el usuario deja de usar la computadora.
        self.fecha_fin = datetime.now()

    def esta_activo(self) -> bool:
        #Indica si la asignación del usuario sigue activa (sin fecha de fin).
        return self.fecha_fin is None
    
