"""
Paquete de Dominio (Modelo de Negocio Orientado a Objetos).

Contiene las entidades y reglas de negocio puras de la aplicación, sin ninguna
dependencia de la interfaz gráfica (Tkinter) ni del almacenamiento físico
(archivos .txt). Es la traducción directa del diagrama de clases `diagram.puml`.

Capas:
    - Vista (screens/)      -> solo dibuja y captura eventos.
    - Presentador (presenters/) -> coordina, no conoce Tkinter ni el disco.
    - Modelo (Models/)      -> orquesta dominio + persistencia (Repository).
    - Dominio (domain/)     -> ESTE paquete: objetos de negocio puros.
"""

from domain.enums import TipoTransaccion, IntervaloTiempo
from domain.cotizacion_historica import CotizacionHistorica
from domain.accion import Accion
from domain.posicion import Posicion
from domain.proveedor_api import ProveedorAPI
from domain.yahoo_finance import YahooFinanceProveedor
from domain.portafolio import Portafolio
from domain.transaccion import Transaccion
from domain.cuenta_bancaria import CuentaBancaria
from domain.usuario import Usuario

__all__ = [
    "TipoTransaccion",
    "IntervaloTiempo",
    "CotizacionHistorica",
    "Accion",
    "Posicion",
    "ProveedorAPI",
    "YahooFinanceProveedor",
    "Portafolio",
    "Transaccion",
    "CuentaBancaria",
    "Usuario",
]
