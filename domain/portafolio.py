"""Entidad `Portafolio` (ver `diagram.puml`)."""

from typing import Dict, List

from domain.accion import Accion
from domain.posicion import Posicion
from domain.proveedor_api import ProveedorAPI


class Portafolio:
    """Conjunto de posiciones de un usuario y operaciones agregadas sobre ellas.

    Relaciones del diagrama:
        - `Portafolio "1" *-- "*" Posicion`  (composición: contiene posiciones)
        - `Portafolio ..> ProveedorAPI`       (dependencia: usa la API de precios)

    El proveedor de precios se inyecta por constructor (inversión de dependencias):
    el portafolio no sabe NI le importa si los precios vienen de Yahoo Finance o
    de un mock de pruebas.
    """

    def __init__(self, proveedor: ProveedorAPI = None):
        self.__posiciones: Dict[str, Posicion] = {}
        self.__proveedor = proveedor

    @property
    def posiciones(self) -> List[Posicion]:
        return list(self.__posiciones.values())

    def obtener_posicion(self, simbolo: str) -> Posicion:
        return self.__posiciones.get(simbolo.strip().upper())

    def comprar_accion(self, simbolo: str, cantidad: float, precio: float) -> Posicion:
        """Añade unidades a la posición del símbolo (creándola si no existía)."""
        simbolo = simbolo.strip().upper()
        posicion = self.__posiciones.get(simbolo)
        if posicion is None:
            posicion = Posicion(Accion(simbolo, precio_actual=precio))
            self.__posiciones[simbolo] = posicion
        posicion.agregar_cantidad(cantidad, precio)
        return posicion

    def vender_accion(self, simbolo: str, cantidad: float) -> None:
        """Reduce unidades de una posición existente; la elimina si llega a cero."""
        simbolo = simbolo.strip().upper()
        posicion = self.__posiciones.get(simbolo)
        if posicion is None:
            return
        posicion.reducir_cantidad(cantidad)
        if posicion.cantidad <= 0:
            del self.__posiciones[simbolo]

    def actualizar_precios(self) -> None:
        """Refresca el precio de cada acción consultando al `ProveedorAPI` inyectado."""
        if self.__proveedor is None:
            return
        for posicion in self.__posiciones.values():
            precio = self.__proveedor.obtener_precio_actual(posicion.accion.simbolo)
            posicion.accion.actualizar_precio(precio)

    def obtener_valor_total(self) -> float:
        """Suma del valor de mercado de todas las posiciones."""
        return sum(p.calcular_valor_actual() for p in self.__posiciones.values())

    def obtener_rendimiento_total(self) -> float:
        """Suma de las ganancias/pérdidas de todas las posiciones."""
        return sum(p.calcular_ganancia_o_perdida() for p in self.__posiciones.values())
