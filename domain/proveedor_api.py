"""Interfaz `ProveedorAPI` (ver `diagram.puml`).

Patrón de diseño: **Strategy / Adapter + Dependency Inversion**.

`Portafolio` y los modelos NO dependen de `yfinance` directamente, dependen de
esta abstracción. Así podemos intercambiar la fuente de precios (Yahoo Finance,
una API de pago, datos simulados para tests...) sin tocar la lógica de negocio.
Eso es exactamente lo que el diagrama representa con `Portafolio ..> ProveedorAPI`.
"""

from abc import ABC, abstractmethod
from typing import List

from domain.enums import IntervaloTiempo
from domain.cotizacion_historica import CotizacionHistorica


class ProveedorAPI(ABC):
    """Contrato que debe cumplir cualquier proveedor de datos de mercado."""

    @abstractmethod
    def obtener_precio_actual(self, simbolo: str) -> float:
        """Devuelve el último precio conocido del símbolo (en EUR)."""
        raise NotImplementedError

    @abstractmethod
    def obtener_serie_de_tiempo(
        self, simbolo: str, intervalo: IntervaloTiempo
    ) -> List[CotizacionHistorica]:
        """Devuelve la serie histórica de cierres para el intervalo pedido."""
        raise NotImplementedError
