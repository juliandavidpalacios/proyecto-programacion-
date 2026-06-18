"""Entidad raíz `Usuario` (ver `diagram.puml`)."""

from typing import List

from domain.cuenta_bancaria import CuentaBancaria
from domain.portafolio import Portafolio
from domain.transaccion import Transaccion


class Usuario:
    """Cliente del sistema. Es la raíz del agregado de dominio.

    Relaciones del diagrama (composición, `*--`):
        - tiene 1 `CuentaBancaria`
        - tiene 1 `Portafolio`
        - realiza * `Transaccion`

    No conoce nada de archivos ni de Tkinter: es un objeto de negocio puro. La
    persistencia la resuelven los *Repository* del paquete `Models`.
    """

    def __init__(
        self,
        id_usuario: str,
        nombre: str,
        correo: str,
        contrasena: str,
        cuenta: CuentaBancaria = None,
        portafolio: Portafolio = None,
    ):
        self.__id_usuario = id_usuario
        self.__nombre = nombre
        self.__correo = correo
        self.__contrasena = contrasena
        self.__cuenta = cuenta or CuentaBancaria()
        self.__portafolio = portafolio or Portafolio()
        self.__transacciones: List[Transaccion] = []

    # --- Propiedades ---
    @property
    def id_usuario(self) -> str:
        return self.__id_usuario

    @property
    def nombre(self) -> str:
        return self.__nombre

    @property
    def correo(self) -> str:
        return self.__correo

    @property
    def cuenta(self) -> CuentaBancaria:
        return self.__cuenta

    @property
    def portafolio(self) -> Portafolio:
        return self.__portafolio

    @property
    def transacciones(self) -> List[Transaccion]:
        return list(self.__transacciones)

    # --- Comportamiento ---
    def verificar_credenciales(self, correo: str, contrasena: str) -> bool:
        """Regla de negocio: comprueba si las credenciales coinciden."""
        return self.__correo == correo and self.__contrasena == contrasena

    def registrar_transaccion(self, transaccion: Transaccion) -> None:
        """Asocia una transacción al historial del usuario."""
        self.__transacciones.append(transaccion)

    def __repr__(self) -> str:
        return f"Usuario({self.__id_usuario}, {self.__correo})"
