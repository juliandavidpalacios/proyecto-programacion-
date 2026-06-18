"""Implementación concreta de `ProveedorAPI` sobre Yahoo Finance (yfinance).

Patrón de diseño: **Adapter**. `yfinance` devuelve `DataFrame` de pandas con un
formato complejo (MultiIndex, sufijos -EUR para cripto...). Esta clase *adapta*
esa interfaz externa al contrato limpio que pide nuestro dominio
(`obtener_precio_actual`, `obtener_serie_de_tiempo`), de modo que el resto de la
aplicación no dependa nunca de pandas ni de yfinance.
"""

from typing import List

from domain.enums import IntervaloTiempo
from domain.cotizacion_historica import CotizacionHistorica
from domain.proveedor_api import ProveedorAPI


class YahooFinanceProveedor(ProveedorAPI):
    """Adaptador de la librería `yfinance` al contrato `ProveedorAPI`."""

    # Cripto-activos que en Yahoo Finance se consultan con el sufijo "-EUR".
    _CRIPTOS = {"BTC", "ETH", "DOGE", "ADA", "SOL", "XRP", "BNB", "LTC"}

    # Cada intervalo del dominio se traduce a los parámetros que entiende yfinance.
    _MAPEO_TIEMPO = {
        IntervaloTiempo.UN_DIA: {"periodo": "1d", "intervalo": "2m"},
        IntervaloTiempo.UNA_SEMANA: {"periodo": "5d", "intervalo": "5m"},
        IntervaloTiempo.UN_MES: {"periodo": "1mo", "intervalo": "30m"},
        IntervaloTiempo.UN_ANIO: {"periodo": "1y", "intervalo": "1d"},
        IntervaloTiempo.CINCO_ANIOS: {"periodo": "max", "intervalo": "1d"},
    }

    def _a_simbolo_yf(self, simbolo: str) -> str:
        """Traduce el símbolo del dominio al formato de Yahoo Finance."""
        simbolo = simbolo.strip().upper()
        return f"{simbolo}-EUR" if simbolo in self._CRIPTOS else simbolo

    def obtener_precio_actual(self, simbolo: str) -> float:
        # Importación perezosa: el dominio puro no depende de yfinance/pandas;
        # solo se cargan cuando realmente se consulta el mercado real.
        import pandas as pd
        import yfinance as yf

        simbolo_yf = self._a_simbolo_yf(simbolo)
        try:
            datos = yf.download(
                simbolo_yf, period="1d", interval="2m", progress=False, auto_adjust=True
            )
            if datos.empty:
                return 0.0
            if isinstance(datos.columns, pd.MultiIndex):
                cierre = datos["Close"][simbolo_yf].dropna()
            else:
                cierre = datos["Close"].dropna()
            return float(cierre.iloc[-1]) if not cierre.empty else 0.0
        except Exception as e:
            print(f"[YahooFinanceProveedor] Error obteniendo precio de {simbolo_yf}: {e}")
            return 0.0

    def obtener_serie_de_tiempo(
        self, simbolo: str, intervalo: IntervaloTiempo
    ) -> List[CotizacionHistorica]:
        import pandas as pd
        import yfinance as yf

        simbolo_yf = self._a_simbolo_yf(simbolo)
        config = self._MAPEO_TIEMPO.get(intervalo, self._MAPEO_TIEMPO[IntervaloTiempo.UN_MES])
        try:
            datos = yf.download(
                simbolo_yf, period=config["periodo"], interval=config["intervalo"],
                progress=False, auto_adjust=True,
            )
            if datos.empty:
                return []
            if isinstance(datos.columns, pd.MultiIndex):
                cierres = datos["Close"][simbolo_yf]
            else:
                cierres = datos["Close"]
            cierres = cierres.dropna()
            cierres.index = cierres.index.tz_localize(None)
            return [
                CotizacionHistorica(fecha.to_pydatetime(), float(precio))
                for fecha, precio in cierres.items()
            ]
        except Exception as e:
            print(f"[YahooFinanceProveedor] Error obteniendo serie de {simbolo_yf}: {e}")
            return []
