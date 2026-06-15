"""Entidad de dominio `InversorInstitucional`.

Agrega (composición) las compras recientes de un gran inversor (fondo, banco o
gestora). Relación: `InversorInstitucional "1" *-- "*" CompraInstitucional`.
"""

from typing import List

from domain.compra_institucional import CompraInstitucional


class InversorInstitucional:
    def __init__(self, nombre: str):
        self.__nombre = nombre
        self.__compras: List[CompraInstitucional] = []

    @property
    def nombre(self) -> str:
        return self.__nombre

    @property
    def compras(self) -> List[CompraInstitucional]:
        return list(self.__compras)

    def agregar_compra(self, compra: CompraInstitucional) -> None:
        """Asocia una compra a este inversor (solo si realmente es una compra)."""
        if compra.es_compra():
            self.__compras.append(compra)

    def obtener_valor_total_comprado(self) -> float:
        """Suma del valor de todas las compras del trimestre."""
        return sum(c.valor for c in self.__compras)

    def __repr__(self) -> str:
        return f"InversorInstitucional({self.__nombre}, {len(self.__compras)} compras)"
