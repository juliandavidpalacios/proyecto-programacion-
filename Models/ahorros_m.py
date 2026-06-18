import os

# El modelo se apoya en el dominio orientado a objetos (diagram.puml) en lugar de
# manipular yfinance y diccionarios sueltos a mano.
from domain.portafolio import Portafolio
from domain.proveedor_api import ProveedorAPI
from domain.yahoo_finance import YahooFinanceProveedor
from domain.cuenta_bancaria import CuentaBancaria


class AhorrosModel:
    def __init__(self, proveedor: ProveedorAPI = None):
        # Almacena la ruta del archivo de texto donde se registran los movimientos de ahorro.
        self.archivo_ahorros = None
        # Ruta del perfil del usuario logueado (para localizar su portafolio).
        self.perfil_txt = None
        # Inyección de dependencias: el proveedor de precios es una abstracción.
        # Por defecto usamos Yahoo Finance, pero podría ser un mock en tests.
        self._proveedor = proveedor or YahooFinanceProveedor()

    # Prepara y resuelve las rutas de archivos asignadas al usuario logueado.
    def establecer_ruta_usuario(self, perfil_txt):
        self.perfil_txt = perfil_txt
        carpeta_usuario = os.path.dirname(perfil_txt)
        # Combina la ruta de la carpeta con el nombre estándar del archivo de ahorros.
        self.archivo_ahorros = os.path.join(carpeta_usuario, "ahorros.txt")
        if not os.path.exists(self.archivo_ahorros):
            with open(self.archivo_ahorros, "w", encoding="utf-8"):
                pass
        return self.archivo_ahorros

    def _ruta_portafolio(self):
        """Resuelve la ruta del fichero de portafolio del usuario activo."""
        if not self.perfil_txt:
            return None
        carpeta = os.path.dirname(self.perfil_txt)
        nombre_base = os.path.splitext(os.path.basename(self.perfil_txt))[0]
        return os.path.join(carpeta, f"{nombre_base}_portafolio.txt")

    def _cargar_portafolio_dominio(self):
        """Lee el fichero de posiciones y construye un objeto de dominio `Portafolio`.

        El `Portafolio` recibe el `ProveedorAPI` por constructor, de modo que él
        mismo sabe refrescar sus precios y calcular su valor total (encapsulamiento
        del comportamiento financiero dentro del dominio)."""
        portafolio = Portafolio(proveedor=self._proveedor)
        ruta = self._ruta_portafolio()
        if not ruta or not os.path.exists(ruta):
            return portafolio
        try:
            with open(ruta, "r", encoding="utf-8") as f:
                for linea in f:
                    linea = linea.strip()
                    if not linea or ":" not in linea:
                        continue
                    ticker, cant = linea.split(":", 1)
                    cantidad = float(cant.strip())
                    if cantidad > 0:
                        # El precio se rellenará luego con actualizar_precios().
                        portafolio.comprar_accion(ticker.strip(), cantidad, 0.0)
        except Exception as e:
            print(f"[AhorrosModel] Error leyendo portafolio: {e}")
        return portafolio

    # Consulta los precios actuales de los activos y calcula su valor de mercado total.
    def obtener_valor_portafolio(self):
        portafolio = self._cargar_portafolio_dominio()
        if not portafolio.posiciones:
            return 0.0
        # El dominio se encarga de consultar el proveedor y sumar el valor.
        portafolio.actualizar_precios()
        return portafolio.obtener_valor_total()

    # Calcula el resumen de saldos reproduciendo los movimientos sobre una
    # CuentaBancaria de dominio (que impide que el ahorro quede en negativo).
    def calcular_resumen(self, lineas):
        cuenta = CuentaBancaria()
        aportado_mes = 0.0
        for linea in lineas:
            linea = linea.strip()
            if not linea:
                continue
            partes = linea.split(",")
            if len(partes) != 3:
                continue
            tipo, _categoria, cant_str = partes
            try:
                cantidad = float(cant_str)
            except ValueError:
                continue
            if tipo == "Ingreso":
                cuenta.depositar(cantidad)
                aportado_mes += cantidad
            else:
                cuenta.retirar(cantidad)
        # El total ahorrado es el saldo disponible de la cuenta de dominio.
        return cuenta.saldo_disponible, aportado_mes

    # Lee las líneas del historial de ahorros almacenadas localmente.
    def leer_lineas_ahorros(self):
        if not self.archivo_ahorros or not os.path.exists(self.archivo_ahorros):
            return []
        with open(self.archivo_ahorros, "r", encoding="utf-8") as f:
            return f.readlines()

    # Escribe una nueva transacción o movimiento financiero en el archivo.
    def guardar_movimiento(self, tipo, categoria, cantidad):
        # Modo "append" ('a') para añadir contenido al final sin borrar lo previo.
        with open(self.archivo_ahorros, "a", encoding="utf-8") as f:
            f.write(f"{tipo},{categoria},{cantidad:.2f}\n")
