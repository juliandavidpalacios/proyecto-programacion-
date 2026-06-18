"""Modelo de la pantalla de Expertos.

Capa de aplicación: decide QUÉ símbolos vigilar y delega la obtención de datos
en una abstracción `ProveedorExpertos` (inyección de dependencias). No conoce
Tkinter ni accede a disco.
"""

from typing import List

from domain.proveedor_expertos import ProveedorExpertos
from domain.yahoo_expertos import YahooExpertosProveedor
from domain.compra_institucional import CompraInstitucional
from domain.inversor_institucional import InversorInstitucional


class ExpertosModel:
    # Lista de grandes valores cuyas compras institucionales seguimos.
    SIMBOLOS_VIGILADOS = ["AAPL", "MSFT", "NVDA", "AMZN", "GOOGL", "TSLA", "META", "JPM"]

    def __init__(self, proveedor: ProveedorExpertos = None):
        # Por defecto Yahoo Finance, pero podría ser un mock en pruebas.
        self._proveedor = proveedor or YahooExpertosProveedor()

    def obtener_compras_trimestre(self) -> List[CompraInstitucional]:
        """Devuelve las compras institucionales recientes (ya ordenadas)."""
        return self._proveedor.obtener_compras_recientes(self.SIMBOLOS_VIGILADOS)

    def agrupar_por_inversor(self) -> List[InversorInstitucional]:
        """Agrupa las compras en objetos de dominio `InversorInstitucional`."""
        inversores = {}
        for compra in self.obtener_compras_trimestre():
            if compra.inversor not in inversores:
                inversores[compra.inversor] = InversorInstitucional(compra.inversor)
            inversores[compra.inversor].agregar_compra(compra)
        return list(inversores.values())
