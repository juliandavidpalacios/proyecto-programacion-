# Importamos el módulo os para manejar rutas y verificar la existencia de archivos
import os
# Importamos yfinance para descargar datos financieros reales del mercado
import yfinance as yf
# datetime y uuid para timbrar e identificar la transacción de dominio.
from datetime import datetime
import uuid

# Entidades de dominio (diagram.puml) para representar la operación de compra.
from domain.transaccion import Transaccion
from domain.enums import TipoTransaccion


class InvertirModel:
    def __init__(self):
        # Base de datos interna encapsulada
        self._base_datos = {
            "Acciones": {
                "AAPL": {"nombre": "Apple Inc.", "precio": 165.20, "sector": "Tecnología",
                         "resumen": "Líder global en hardware, software y servicios. Creadores del iPhone, Mac y iPad. Considerada una de las empresas más valiosas del mundo."},
                "TSLA": {"nombre": "Tesla Inc.", "precio": 210.50, "sector": "Automoción",
                         "resumen": "Empresa enfocada en la transición a energía sostenible. Fabrica vehículos eléctricos, paneles solares y baterías gigantes."},
                "AMZN": {"nombre": "Amazon.com", "precio": 140.00, "sector": "E-commerce",
                         "resumen": "El gigante del comercio electrónico y proveedor líder de servicios en la nube (AWS)."}
            },
            "Cripto": {
                "BTC": {"nombre": "Bitcoin", "precio": 58000.00, "sector": "Criptomoneda",
                        "resumen": "La primera criptomoneda descentralizada. Creada como reserva de valor y alternativa digital al oro. Alta volatilidad."},
                "ETH": {"nombre": "Ethereum", "precio": 3100.00, "sector": "Criptomoneda",
                        "resumen": "Plataforma de código abierto basada en blockchain. Permite la creación de contratos inteligentes y aplicaciones descentralizadas (dApps)."}
            }
        }

    # --- NUEVOS MÉTODOS DE ENCAPSULAMIENTO (GETTERS) ---
    def obtener_tickers_por_categoria(self, categoria):
        """Retorna los tickers disponibles en una categoría dada."""
        if categoria in self._base_datos:
            return list(self._base_datos[categoria].keys())
        return []

    def obtener_precio_inicial(self, categoria, ticker):
        """Retorna el precio base estático de un activo."""
        if categoria in self._base_datos and ticker in self._base_datos[categoria]:
            return self._base_datos[categoria][ticker]["precio"]
        return 0.0

    def obtener_detalle_activo(self, categoria, ticker):
        """Retorna una copia segura con la información descriptiva del activo."""
        if categoria in self._base_datos and ticker in self._base_datos[categoria]:
            return self._base_datos[categoria][ticker].copy()
        return None

    # --- MÉTODOS DE PERSISTENCIA Y API ---
    def obtener_datos_api(self, ticker_real, periodo, intervalo):
        activo_api = yf.Ticker(ticker_real)
        return activo_api.history(period=periodo, interval=intervalo)

    def calcular_saldo_ahorros(self, usuario_logueado):
        perfil_path = usuario_logueado
        folder = os.path.dirname(perfil_path)
        archivo_ahorros = os.path.join(folder, "ahorros.txt")
        saldo = 0.0

        if os.path.exists(archivo_ahorros):
            try:
                with open(archivo_ahorros, "r", encoding="utf-8") as f:
                    for linea in f:
                        partes = linea.strip().split(",")
                        if len(partes) == 3:
                            tipo, _, cant_str = partes
                            cantidad = float(cant_str)
                            if tipo in ["Depósito", "Ingreso"]:
                                saldo += cantidad
                            elif tipo == "Retiro":
                                saldo -= cantidad
            except Exception as e:
                # Propagamos el error de manera controlada para que el presentador decida qué mostrar
                raise RuntimeError(f"No se pudo leer el archivo de ahorros de forma correcta: {e}")
                
        return saldo, archivo_ahorros

    def leer_portafolio_activos(self, usuario_logueado):
        perfil_path = usuario_logueado
        folder = os.path.dirname(perfil_path)
        nombre_base = os.path.splitext(os.path.basename(perfil_path))[0]
        archivo_portafolio = os.path.join(folder, f"{nombre_base}_portafolio.txt")
        portafolio = {}

        if os.path.exists(archivo_portafolio):
            try:
                with open(archivo_portafolio, "r", encoding="utf-8") as f:
                    for linea in f:
                        linea = linea.strip()
                        if ":" in linea:
                            ticker, cant = linea.split(":")
                            portafolio[ticker.strip()] = float(cant.strip())
            except Exception as e:
                raise RuntimeError(f"Fallo crítico al acceder al portafolio de activos: {e}")
                
        return portafolio, archivo_portafolio

    def guardar_portafolio_activos(self, path, portafolio):
        try:
            with open(path, "w", encoding="utf-8") as f:
                for ticker, cant in portafolio.items():
                    if cant > 0:
                        f.write(f"{ticker}: {cant:.6f}\n")
        except Exception as e:
            raise RuntimeError(f"Error de escritura en el disco para guardar el portafolio: {e}")

    def registrar_compra(self, usuario_logueado, categoria, ticker, cantidad_euros):
        """Orquesta TODA la operación de compra (regla de negocio + persistencia).

        Antes esta lógica (y la escritura de ficheros) vivía en el Presentador,
        lo que violaba el patrón MVP. Ahora el Presentador solo pide "compra esto"
        y el Modelo decide y persiste, devolviendo datos puros para mostrar.

        Devuelve: (exito: bool, datos: dict | None, mensaje_error: str | None)
        """
        # 1. Validación de fondos contra el saldo de ahorros.
        saldo_ahorros, archivo_ahorros = self.calcular_saldo_ahorros(usuario_logueado)
        if cantidad_euros > saldo_ahorros:
            return False, None, (
                f"No dispones de capital suficiente para completar el trade.\n\n"
                f"💰 Saldo Actual: {saldo_ahorros:,.2f} €\n"
                f"🛒 Intento de compra: {cantidad_euros:,.2f} €"
            )

        # 2. Cálculo de fracciones adquiridas según el precio del activo.
        precio_actual = float(self.obtener_precio_inicial(categoria, ticker))
        if precio_actual <= 0:
            return False, None, "No se pudo determinar el precio del activo."
        acciones_adquiridas = cantidad_euros / precio_actual

        # 3. Actualizamos el portafolio del usuario.
        portafolio, archivo_portafolio = self.leer_portafolio_activos(usuario_logueado)
        portafolio[ticker] = portafolio.get(ticker, 0.0) + acciones_adquiridas
        self.guardar_portafolio_activos(archivo_portafolio, portafolio)

        # 4. Registramos el retiro en la hucha de ahorros.
        with open(archivo_ahorros, "a", encoding="utf-8") as f:
            f.write(f"Retiro,Inversión en {ticker},{cantidad_euros:.2f}\n")

        # 5. Creamos una Transaccion de dominio y la persistimos usando SU propio
        #    método de serialización (generar_recibo / a_linea_historial).
        transaccion = Transaccion(
            id_transaccion=str(uuid.uuid4()),
            tipo=TipoTransaccion.COMPRA,
            monto_total=cantidad_euros,
            fecha_hora=datetime.now(),
            simbolo_accion=ticker,
            cantidad_acciones=acciones_adquiridas,
        )
        carpeta = os.path.dirname(usuario_logueado)
        archivo_historial = os.path.join(carpeta, "historial_inversiones.txt")
        with open(archivo_historial, "a", encoding="utf-8") as f:
            f.write(transaccion.a_linea_historial())

        # 6. Devolvemos datos PUROS (sin tocar la interfaz) para que la vista pinte.
        datos = {
            "ticker": ticker,
            "acciones_adquiridas": acciones_adquiridas,
            "precio_actual": precio_actual,
            "cantidad": cantidad_euros,
            "nuevo_saldo": saldo_ahorros - cantidad_euros,
            "inventario_total": portafolio[ticker],
            "recibo": transaccion.generar_recibo(),
        }
        return True, datos, None