"""Entidad `CotizacionHistorica` (ver `diagram.puml`)."""

from datetime import datetime


class CotizacionHistorica:
    """Punto de una serie de tiempo: el precio de cierre de un activo en un instante.

    Es un *Value Object* inmutable: una vez creado no cambia. Encapsula sus dos
    atributos privados y los expone mediante propiedades de solo lectura.
    """

    def __init__(self, fecha_hora: datetime, precio_cierre: float):
        self.__fecha_hora = fecha_hora
        self.__precio_cierre = float(precio_cierre)

    @property
    def fecha_hora(self) -> datetime:
        return self.__fecha_hora

    @property
    def precio_cierre(self) -> float:
        return self.__precio_cierre

    def __repr__(self) -> str:
        return f"CotizacionHistorica({self.__fecha_hora!r}, {self.__precio_cierre:.2f})"
