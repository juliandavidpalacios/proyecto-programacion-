"""Entidad `Accion` (ver `diagram.puml`)."""

from typing import Dict, List

from domain.enums import IntervaloTiempo
from domain.cotizacion_historica import CotizacionHistorica


class Accion:
    """Representa un activo financiero negociable (acción o criptomoneda).

    Mantiene su precio actual y una caché de historiales por `IntervaloTiempo`
    (atributo `historial: Map<IntervaloTiempo, List<CotizacionHistorica>>`),
    para evitar pedir dos veces lo mismo al `ProveedorAPI`.
    """

    def __init__(self, simbolo: str, nombre_empresa: str = "", precio_actual: float = 0.0):
        self.__simbolo = simbolo.strip().upper()
        self.__nombre_empresa = nombre_empresa
        self.__precio_actual = float(precio_actual)
        # Caché de series temporales indexada por intervalo.
        self.__historial: Dict[IntervaloTiempo, List[CotizacionHistorica]] = {}

    # --- Propiedades de solo lectura (encapsulamiento) ---
    @property
    def simbolo(self) -> str:
        return self.__simbolo

    @property
    def nombre_empresa(self) -> str:
        return self.__nombre_empresa

    @property
    def precio_actual(self) -> float:
        return self.__precio_actual

    # --- Comportamiento (métodos del diagrama) ---
    def actualizar_precio(self, nuevo_precio: float) -> None:
        """Refresca el último precio de mercado conocido."""
        if nuevo_precio is not None and nuevo_precio >= 0:
            self.__precio_actual = float(nuevo_precio)

    def guardar_historial(
        self, intervalo: IntervaloTiempo, cotizaciones: List[CotizacionHistorica]
    ) -> None:
        """Almacena (cachea) la serie de cotizaciones para un intervalo dado."""
        self.__historial[intervalo] = list(cotizaciones)

    def tiene_historial_guardado(self, intervalo: IntervaloTiempo) -> bool:
        """Indica si ya tenemos cacheada la serie de ese intervalo."""
        return intervalo in self.__historial and len(self.__historial[intervalo]) > 0

    def obtener_historial(self, intervalo: IntervaloTiempo) -> List[CotizacionHistorica]:
        """Devuelve la serie cacheada (lista vacía si no existe)."""
        return list(self.__historial.get(intervalo, []))

    def __repr__(self) -> str:
        return f"Accion({self.__simbolo}, {self.__precio_actual:.2f}€)"
