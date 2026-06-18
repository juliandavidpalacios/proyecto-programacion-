"""Interfaz `ProveedorExpertos`.

Patrón: **Strategy + Inversión de Dependencias** (igual que `ProveedorAPI`).
El modelo de Expertos depende de esta abstracción, no de una fuente concreta de
datos institucionales. Así se puede intercambiar Yahoo Finance por un proveedor
de datos 13F de pago, o por datos simulados en pruebas, sin tocar la lógica.
"""

from abc import ABC, abstractmethod
from typing import List

from domain.compra_institucional import CompraInstitucional


class ProveedorExpertos(ABC):
    """Contrato para obtener las compras institucionales recientes."""

    @abstractmethod
    def obtener_compras_recientes(self, simbolos: List[str]) -> List[CompraInstitucional]:
        """Devuelve las compras (aumentos de posición) del último trimestre
        por parte de grandes inversores sobre los símbolos indicados."""
        raise NotImplementedError
