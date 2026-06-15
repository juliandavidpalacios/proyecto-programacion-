# Importamos os para resolver rutas y datetime para la fecha (NO se importa tkinter:
# el presentador es lógica pura y nunca toca la interfaz gráfica directamente).
import os
from datetime import datetime


class HomePresenter:
    """Presentador del panel de inicio. Coordina Modelo y Vista sin conocer Tkinter."""

    def __init__(self, view, model):
        self.view = view
        self.model = model

    # Coordina la extracción y el renderizado de la información del perfil.
    def cargar_datos_usuario(self):
        perfil_path = self.view.controller.usuario_logueado
        if not perfil_path:
            return

        # La fecha y el saludo se calculan aquí y se ENVÍAN ya formateados a la vista.
        self.view.mostrar_fecha(datetime.now().strftime("%A, %d de %B de %Y").capitalize())
        nombre = self.model.leer_nombre(perfil_path)
        self.view.mostrar_saludo(f"Hola, {nombre} 👋")

        folder = os.path.dirname(perfil_path)

        # ── AHORROS ──
        total_ahorrado, aportado_mes, ultimos_movs = self.model.leer_ahorros(folder)
        self.view.actualizar_resumen(
            f"{total_ahorrado:,.2f} €", f"{aportado_mes:,.2f} €"
        )
        self.view.poblar_movimientos(ultimos_movs)

        # ── INVERSIONES ──
        total_invertido = self.model.leer_total_invertido(folder)
        self.view.actualizar_invertido(f"{total_invertido:,.2f} €")

        # ── PORTAFOLIO EN TIEMPO REAL ──
        portafolio = self.model.leer_portafolio(perfil_path)
        if portafolio:
            valor_actual = self.poblar_activos(portafolio, folder)
            self.view.actualizar_valor_portafolio(f"{valor_actual:,.2f} €")
        else:
            self.view.actualizar_valor_portafolio("0.00 €")
            self.view.mostrar_portafolio_vacio()

    # Coordina la tasación de los activos en tiempo real (lógica de negocio pura).
    def poblar_activos(self, portafolio, folder):
        self.view.limpiar_portafolio()

        criptos = {"BTC", "ETH", "DOGE", "ADA", "SOL", "XRP", "BNB", "LTC"}
        tickers_yf = [f"{t}-EUR" if t in criptos else t for t in portafolio.keys()]
        coste_ticker = self.model.leer_coste_por_ticker(folder)

        valor_total = 0.0
        precios = {}
        if tickers_yf:
            precios_descargados = self.model.descargar_precios(tickers_yf)
            for ticker_orig, ticker_yf_str in zip(portafolio.keys(), tickers_yf):
                precios[ticker_orig] = precios_descargados.get(ticker_yf_str, 0.0)

        for i, (ticker, cantidad) in enumerate(portafolio.items()):
            precio = precios.get(ticker, 0.0)
            valor = cantidad * precio
            coste = coste_ticker.get(ticker, 0.0)
            pct = (valor - coste) / coste * 100 if coste > 0 else 0.0
            valor_total += valor
            # La vista solo pinta la fila con los datos ya calculados.
            self.view.pintar_activo(ticker, cantidad, precio, valor, pct, i)

        return valor_total

    # Gobierna el cierre de sesión: pide confirmación A LA VISTA y delega el desmontaje.
    def cerrar_sesion(self):
        if not self.view.confirmar_cierre_sesion():
            return
        # El desmontaje de la interfaz lo realiza el presentador/vista principal.
        self.view.controller.ejecutar_cerrar_sesion()
