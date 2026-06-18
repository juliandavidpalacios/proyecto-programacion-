"""Entidad `CuentaBancaria` (ver `diagram.puml`)."""


class CuentaBancaria:
    """Cuenta con dos bolsas de dinero: saldo disponible y saldo de ahorros.

    Relación del diagrama: `Usuario "1" *-- "1" CuentaBancaria`.
    Toda la lógica de mover dinero (depositar, retirar, transferir entre bolsas)
    vive aquí, garantizando que nunca queden saldos negativos.
    """

    def __init__(self, saldo_disponible: float = 0.0, saldo_ahorros: float = 0.0):
        self.__saldo_disponible = float(saldo_disponible)
        self.__saldo_ahorros = float(saldo_ahorros)

    @property
    def saldo_disponible(self) -> float:
        return self.__saldo_disponible

    @property
    def saldo_ahorros(self) -> float:
        return self.__saldo_ahorros

    def depositar(self, monto: float) -> bool:
        """Ingresa dinero en el saldo disponible. Devuelve True si fue válido."""
        if monto <= 0:
            return False
        self.__saldo_disponible += monto
        return True

    def retirar(self, monto: float) -> bool:
        """Retira del saldo disponible si hay fondos suficientes."""
        if monto <= 0 or monto > self.__saldo_disponible:
            return False
        self.__saldo_disponible -= monto
        return True

    def transferir_a_ahorros(self, monto: float) -> bool:
        """Mueve dinero de disponible a ahorros."""
        if monto <= 0 or monto > self.__saldo_disponible:
            return False
        self.__saldo_disponible -= monto
        self.__saldo_ahorros += monto
        return True

    def transferir_a_disponible(self, monto: float) -> bool:
        """Mueve dinero de ahorros a disponible."""
        if monto <= 0 or monto > self.__saldo_ahorros:
            return False
        self.__saldo_ahorros -= monto
        self.__saldo_disponible += monto
        return True
