"""Enumeraciones del dominio (ver `diagram.puml`).

Usamos `enum.Enum` de la librería estándar para representar conjuntos cerrados
de valores. Esto evita "strings mágicos" repartidos por el código y aporta
seguridad de tipos, que es justamente lo que el diagrama UML expresa con
sus bloques `enum`.
"""

from enum import Enum


class TipoTransaccion(Enum):
    """Naturaleza de un movimiento registrado en el sistema."""
    COMPRA = "COMPRA"
    VENTA = "VENTA"
    DEPOSITO = "DEPOSITO"
    RETIRO = "RETIRO"


class IntervaloTiempo(Enum):
    """Ventanas temporales para consultar el historial de cotizaciones.

    El valor de cada miembro es la etiqueta que la interfaz muestra al usuario
    (los botones 1D, 1S, 1M, 1A, MAX de la pantalla de Acciones/Invertir).
    """
    UN_DIA = "1D"
    UNA_SEMANA = "1S"
    UN_MES = "1M"
    UN_ANIO = "1A"
    CINCO_ANIOS = "MAX"
