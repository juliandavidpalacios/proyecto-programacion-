"""Entidad `Transaccion` (ver `diagram.puml`)."""

from datetime import datetime

from domain.enums import TipoTransaccion


class Transaccion:
    """Registro inmutable de una operación realizada por el usuario.

    Relación del diagrama: `Usuario "1" *-- "*" Transaccion : realiza`.
    Cubre tanto operaciones de bolsa (COMPRA/VENTA, con símbolo y nº de acciones)
    como movimientos de cuenta (DEPOSITO/RETIRO).
    """

    def __init__(
        self,
        id_transaccion: str,
        tipo: TipoTransaccion,
        monto_total: float,
        fecha_hora: datetime = None,
        simbolo_accion: str = "",
        cantidad_acciones: float = 0.0,
    ):
        self.__id_transaccion = id_transaccion
        self.__fecha_hora = fecha_hora or datetime.now()
        self.__tipo = tipo
        self.__monto_total = float(monto_total)
        self.__simbolo_accion = simbolo_accion
        self.__cantidad_acciones = float(cantidad_acciones)

    # --- Propiedades de solo lectura ---
    @property
    def id_transaccion(self) -> str:
        return self.__id_transaccion

    @property
    def fecha_hora(self) -> datetime:
        return self.__fecha_hora

    @property
    def tipo(self) -> TipoTransaccion:
        return self.__tipo

    @property
    def monto_total(self) -> float:
        return self.__monto_total

    @property
    def simbolo_accion(self) -> str:
        return self.__simbolo_accion

    @property
    def cantidad_acciones(self) -> float:
        return self.__cantidad_acciones

    # --- Comportamiento (método del diagrama) ---
    def generar_recibo(self) -> str:
        """Construye una descripción legible de la operación para mostrar al usuario."""
        sello = self.__fecha_hora.strftime("%Y-%m-%d %H:%M:%S")
        if self.__tipo in (TipoTransaccion.COMPRA, TipoTransaccion.VENTA):
            return (
                f"[{sello}] {self.__tipo.value} | Activo: {self.__simbolo_accion} | "
                f"Dinero usado: {self.__monto_total:.2f} € | "
                f"Acciones obtenidas: +{self.__cantidad_acciones:.6f}"
            )
        return f"[{sello}] {self.__tipo.value} | Monto: {self.__monto_total:.2f} €"

    def a_linea_historial(self) -> str:
        """Serializa la transacción al formato de `historial_inversiones.txt`."""
        sello = self.__fecha_hora.strftime("%Y-%m-%d %H:%M:%S")
        return (
            f"[{sello}] {self.__tipo.value} | Activo: {self.__simbolo_accion} | "
            f"Dinero usado: {self.__monto_total:.2f} € | "
            f"Acciones obtenidas: +{self.__cantidad_acciones:.6f}\n"
        )
