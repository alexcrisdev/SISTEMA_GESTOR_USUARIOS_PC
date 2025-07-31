from enum import Enum

class TipoComputadora(Enum):
    ESCRITORIO = "Escritorio"
    LAPTOP = "Laptop"
    SERVIDOR = "Servidor"

class RedComputadora(Enum):
    DOMINIO = "Dominio"
    GRUPO_TRABAJO = "Grupo de trabajo"

class Computadora:
    def __init__(self, id_computadora: str, clave_computadora: str, accesorios_computadora: str, codigo_ksd_computadora: str,
                 tipo_computadora: TipoComputadora, red_computadora: RedComputadora):
        self.id_computadora = id_computadora
        self.clave_computadora = clave_computadora
        self.accesorios_computadora = accesorios_computadora
        self.codigo_ksd_computadora = codigo_ksd_computadora
        self.tipo_computadora = tipo_computadora
        self.red_computadora = red_computadora

    @property
    def id_computadora(self) -> str:
        return self._id_computadora
    @id_computadora.setter
    def id_computadora(self, valor: str) -> None:
        if len(valor) != 6:
            raise ValueError("El ID de la computadora debe tener exactamente 6 caracteres")
        self._id_computadora = valor 

    @property
    def clave_computadora(self) -> str:
        return self._clave_computadora
    @clave_computadora.setter
    def clave_computadora(self, valor: str) -> None:
        if len(valor) != 8:
            raise ValueError("El valor debe contener 8 caracteres")
        self._clave_computadora = valor

    @property
    def accesorios_computadora(self) -> str:
        return self._accesorios_computadora
    @accesorios_computadora.setter
    def accesorios_computadora(self, valor: str) -> None:
        if not isinstance(valor, str) or not valor.strip():
            raise ValueError("Debe ingresar los accesorios de la computadora")
        self._accesorios_computadora = valor

    @property
    def codigo_ksd_computadora(self) -> str:
        return self._codigo_ksd_computadora
    @codigo_ksd_computadora.setter
    def codigo_ksd_computadora(self, valor: str) -> None:
        if valor:
            if len(valor) != 20:
                raise ValueError("El valor debe contener 20 caracteres")
        else:
            valor = "" #o None
        self._codigo_ksd_computadora = valor

    @property
    def tipo_computadora(self) -> TipoComputadora:
        return self._tipo_computadora
    @tipo_computadora.setter
    def tipo_computadora(self, valor: TipoComputadora) -> None:
        if not isinstance(valor, TipoComputadora):
            raise ValueError("Tipo de computadora no válido")
        self._tipo_computadora = valor

    @property
    def red_computadora(self) -> RedComputadora:
        return self._red_computadora
    @red_computadora.setter
    def red_computadora(self, valor: RedComputadora) -> None:
        if not isinstance(valor, RedComputadora):
            raise ValueError("Tipo de red no válido")
        self._red_computadora = valor