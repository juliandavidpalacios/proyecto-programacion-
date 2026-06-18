"""Entidad de dominio `CompraInstitucional`.

Representa una compra (aumento de posición) de un activo realizada por un gran
inversor institucional durante el último trimestre. Es un *Value Object*
inmutable con atributos privados expuestos por propiedades de solo lectura.
"""


class CompraInstitucional:
    def __init__(
        self,
        inversor: str,
        simbolo: str,
        empresa: str,
        acciones: float,
        valor: float,
        variacion_pct: float,
        fecha_reporte: str = "",
    ):
        self.__inversor = inversor
        self.__simbolo = simbolo.strip().upper()
        self.__empresa = empresa
        self.__acciones = float(acciones)
        self.__valor = float(valor)
        self.__variacion_pct = float(variacion_pct)
        self.__fecha_reporte = fecha_reporte

    # --- Propiedades de solo lectura (encapsulamiento) ---
    @property
    def inversor(self) -> str:
        return self.__inversor

    @property
    def simbolo(self) -> str:
        return self.__simbolo

    @property
    def empresa(self) -> str:
        return self.__empresa

    @property
    def acciones(self) -> float:
        return self.__acciones

    @property
    def valor(self) -> float:
        return self.__valor

    @property
    def variacion_pct(self) -> float:
        return self.__variacion_pct

    @property
    def fecha_reporte(self) -> str:
        return self.__fecha_reporte

    # --- Comportamiento ---
    def es_compra(self) -> bool:
        """Regla de negocio: solo es 'compra' si el inversor aumentó su posición."""
        return self.__variacion_pct > 0

    def __repr__(self) -> str:
        return f"CompraInstitucional({self.__inversor} -> {self.__simbolo}, {self.__valor:.0f}€)"
