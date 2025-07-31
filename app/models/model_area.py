import re

def _validar_area(valor: str) -> str:
    if not isinstance(valor, str):
        raise ValueError("El nombre del área debe ser una cadena de texto")
    if not valor.strip():
        raise ValueError("El nombre del área no puede estar vacío")
    if not re.match(r'^[^\W\d_]+(?:\s[^\W\d_]+)*$', valor, re.UNICODE):
        raise ValueError(f"El área solo puede contener letras y espacios")
    if len(valor) > 30:
        raise ValueError("El nombre del área no puede superar los 30 caracteres")
    return valor


class Area:
    def __init__(self, nombre_area: str, id_area: int = None):
        self.id_area = id_area
        self.nombre_area = nombre_area

    @property
    def id_area(self) -> int:
        return self._id_area
    @id_area.setter
    def id_area(self, valor: int) -> None:
        if valor is not None and not isinstance(valor, int):
            raise ValueError("El id_area debe ser entero o None")
        self._id_area = valor

    @property
    def nombre_area(self) -> str:
        return self._nombre_area
    @nombre_area.setter
    def nombre_area(self, valor: str) -> None:
        self._nombre_area = _validar_area(valor)

    def to_dict(self) -> dict:
        return {
            'id_area': self.id_area,
            'nombre_area': self.nombre_area
        }
    