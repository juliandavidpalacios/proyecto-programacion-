"""Entidad `Posicion` (ver `diagram.puml`)."""

from domain.accion import Accion


class Posicion:
    """Tenencia de un usuario sobre una `Accion` concreta dentro del portafolio.

    Relación del diagrama: `Posicion "*" --> "1" Accion`.
    Guarda cuántas unidades se poseen y a qué precio medio se compraron, lo que
    permite calcular el valor actual y la ganancia/pérdida.
    """

    def __init__(self, accion: Accion, cantidad: float = 0.0, precio_compra_promedio: float = 0.0):
        self.__accion = accion
        self.__cantidad = float(cantidad)
        self.__precio_compra_promedio = float(precio_compra_promedio)

    # --- Propiedades ---
    @property
    def accion(self) -> Accion:
        return self.__accion

    @property
    def cantidad(self) -> float:
        return self.__cantidad

    @property
    def precio_compra_promedio(self) -> float:
        return self.__precio_compra_promedio

    # --- Comportamiento (métodos del diagrama) ---
    def agregar_cantidad(self, cantidad: float, precio: float) -> None:
        """Suma unidades recalculando el precio medio ponderado de compra."""
        if cantidad <= 0:
            return
        coste_previo = self.__cantidad * self.__precio_compra_promedio
        coste_nuevo = cantidad * precio
        self.__cantidad += cantidad
        if self.__cantidad > 0:
            self.__precio_compra_promedio = (coste_previo + coste_nuevo) / self.__cantidad

    def reducir_cantidad(self, cantidad: float) -> None:
        """Resta unidades vendidas (sin bajar de cero). El precio medio no cambia."""
        self.__cantidad = max(0.0, self.__cantidad - cantidad)

    def calcular_valor_actual(self) -> float:
        """Valor de mercado de la posición: cantidad x precio actual de la acción."""
        return self.__cantidad * self.__accion.precio_actual

    def calcular_ganancia_o_perdida(self) -> float:
        """Plusvalía/minusvalía: valor de mercado menos coste de adquisición."""
        coste = self.__cantidad * self.__precio_compra_promedio
        return self.calcular_valor_actual() - coste

    def calcular_rendimiento_pct(self) -> float:
        """Rendimiento porcentual respecto al coste de adquisición."""
        coste = self.__cantidad * self.__precio_compra_promedio
        if coste <= 0:
            return 0.0
        return self.calcular_ganancia_o_perdida() / coste * 100.0

    def __repr__(self) -> str:
        return f"Posicion({self.__accion.simbolo} x{self.__cantidad:.4f})"
