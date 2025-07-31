import re

def _validar_nombre_o_apellido(valor: str, campo: str) -> str:
    if not isinstance(valor, str):
        raise ValueError(f"El {campo} debe ser una cadena de texto")
    if not valor.strip():
        raise ValueError(f"El {campo} no puede estar vacío")
    if not re.match(r'^[^\W\d_]+(?:\s[^\W\d_]+)*$', valor, re.UNICODE):
        raise ValueError(f"El {campo} solo puede contener letras y espacios")
    if len(valor) > 50:
        raise ValueError(f"El {campo} no puede superar los 50 caracteres")
    return valor

def _validar_correo(valor: str) ->str:
    if not isinstance(valor, str):
        raise ValueError("El correo debe ser una cadena de texto")
    if not re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', valor):
        raise ValueError("Correo no válido (Ejemplo: usuario@dominio.com)")
    if len(valor) > 50:
        raise ValueError("El correo no puede superar los 50 caracteres")
    return valor

class Usuario:
    def __init__(self, id_usuario: str, nombre_usuario: str, apellido_usuario: str, correo_usuario: str):
        self.id_usuario = id_usuario
        self.nombre_usuario = nombre_usuario
        self.apellido_usuario = apellido_usuario
        self.correo_usuario = correo_usuario

    @property
    def id_usuario(self) -> str:
        return self._id_usuario
    @id_usuario.setter
    def id_usuario(self, valor: str) -> None:
        if len(valor) !=8 or not valor.isdigit():
            raise ValueError("El ID debe contener 8 dígitos numéricos")
        self._id_usuario = valor

    @property
    def nombre_usuario(self) -> str:
        return self._nombre_usuario
    @nombre_usuario.setter
    def nombre_usuario(self, valor: str) -> None:
        self._nombre_usuario = _validar_nombre_o_apellido(valor, "Nombre")

    @property
    def apellido_usuario(self) -> str:
        return self._apellido_usuario
    @apellido_usuario.setter
    def apellido_usuario(self, valor: str) -> None:
        self._apellido_usuario = _validar_nombre_o_apellido(valor, "Apellido")

    @property
    def correo_usuario(self) -> str:
        return self._correo_usuario
    @correo_usuario.setter
    def correo_usuario(self, valor: str) -> None:
        self._correo_usuario = _validar_correo(valor)

    def to_dict(self) -> dict:
        return{
            'id_usuario': self.id_usuario,
            'nombre_usuario': self.nombre_usuario,
            'apellido_usuario': self.apellido_usuario,
            'correo_usuario': self.correo_usuario
        }