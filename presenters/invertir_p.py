import os
from datetime import datetime


class InvertirPresenter:
    def __init__(self, view, model):
        self.view = view
        self.model = model

        self.periodo_actual = "1M"
        self.activo_seleccionado = None
        self.categoria_seleccionada = None

    def obtener_activos_por_categoria(self, categoria):
        # Consume el método encapsulado del modelo de manera segura
        return self.model.get_tickers_por_categoria(categoria) if hasattr(self.model, 'get_tickers_por_categoria') else self.model.obtener_tickers_por_categoria(categoria)

    def obtener_precio_inicial(self, categoria, ticker):
        return self.model.obtener_precio_inicial(categoria, ticker)

    def seleccionar_activo(self, categoria, ticker):
        self.activo_seleccionado = self.model.obtener_detalle_activo(categoria, ticker)
        self.activo_seleccionado['ticker'] = ticker
        self.categoria_seleccionada = categoria

        # Ordenamos a la vista actualizarse pasándole datos ya tratados
        self.view.actualizar_datos_visuales(
            nombre=self.activo_seleccionado['nombre'],
            ticker=ticker,
            precio_formateado=f"{self.activo_seleccionado['precio']:,.2f}",
            sector=self.activo_seleccionado['sector'],
            resumen=self.activo_seleccionado['resumen']
        )
        self.cambiar_periodo("1M")

    def cambiar_periodo(self, periodo):
        if not self.activo_seleccionado:
            self.view.mostrar_advertencia("Aviso", "Por favor, selecciona un activo de la lista primero.")
            return

        self.periodo_actual = periodo
        self.view.iluminar_boton_periodo(periodo)
        self.generar_grafico_activo()

    def generar_grafico_activo(self):
        if not self.activo_seleccionado:
            return

        ticker = self.activo_seleccionado['ticker']
        ticker_real = f"{ticker}-EUR" if self.categoria_seleccionada == "Cripto" else ticker

        mapeo_tiempo = {
            "1D": {"periodo": "1d", "intervalo": "2m"},
            "1S": {"periodo": "5d", "intervalo": "5m"},
            "1M": {"periodo": "1mo", "intervalo": "30m"},
            "1A": {"periodo": "1y", "intervalo": "1h"},
            "MAX": {"periodo": "max", "intervalo": "1d"}
        }
        config = mapeo_tiempo.get(self.periodo_actual, {"periodo": "1mo", "intervalo": "1d"})

        try:
            datos = self.model.obtener_datos_api(ticker_real, config["periodo"], config["intervalo"])

            if datos.empty:
                self.view.mostrar_error("Error", f"No se encontraron datos en tiempo real para {ticker_real}")
                return

            datos.index = datos.index.tz_localize(None)
            fechas = datos.index
            valores = datos['Close'].values

            precio_real_actual = float(valores[-1])
            self.view.refrescar_precio_cabecera(precio_real_actual)

            # Lógica matemática de negocio en el presentador
            color_linea = "#2ecc71" if valores[-1] >= valores[0] else "#ff4c4c"
            
            # Delegamos por completo el dibujado a la infraestructura de la vista
            self.view.dibujar_grafica(fechas, valores, self.periodo_actual, color_linea)

        except Exception as e:
            self.view.mostrar_error("Error", f"Error de conexión con el mercado: {e}")

    def ejecutar_compra(self):
        if not self.activo_seleccionado:
            self.view.mostrar_advertencia("Operación Inválida", "Primero debes seleccionar qué activo deseas comprar.")
            return

        usuario_logueado = getattr(self.view.controller, 'usuario_logueado', None)
        if not usuario_logueado:
            self.view.mostrar_error("Error de Autenticación", "No se detectó ningún usuario activo en el sistema.")
            return

        entrada = self.view.obtener_cantidad_ingresada()
        try:
            cantidad = float(entrada)
            if cantidad <= 0:
                self.view.mostrar_error("Cantidad Incorrecta", "Por favor, introduce un número que sea superior a 0 €.")
                return
        except ValueError:
            self.view.mostrar_error("Formato Inválido", "Por favor, escribe un valor numérico válido.")
            return

        ticker = self.activo_seleccionado['ticker']

        try:
            saldo_ahorros, archivo_ahorros = self.model.calcular_saldo_ahorros(usuario_logueado)
            
            if cantidad > saldo_ahorros:
                self.view.mostrar_error(
                    "Fondos Insuficientes",
                    f"No dispones de capital suficiente para completar el trade.\n\n"
                    f"💰 Saldo Actual: {saldo_ahorros:,.2f} €\n"
                    f"🛒 Intento de compra: {cantidad:,.2f} €"
                )
                return

            precio_actual = float(self.model.obtener_precio_inicial(self.categoria_seleccionada, ticker))
            acciones_adquiridas = cantidad / precio_actual

            portafolio, archivo_portafolio = self.model.leer_portafolio_activos(usuario_logueado)
            portafolio[ticker] = portafolio.get(ticker, 0.0) + acciones_adquiridas

            with open(archivo_ahorros, "a", encoding="utf-8") as f:
                f.write(f"Retiro,Inversión en {ticker},{cantidad:.2f}\n")

            self.model.guardar_portafolio_activos(archivo_portafolio, portafolio)

            # Historial general
            folder = os.path.dirname(usuario_logueado)
            archivo_historial = os.path.join(folder, "historial_inversiones.txt")
            
            # 1. Corregimos el formato de fecha al estándar internacional (YYYY-MM-DD)
            ahora = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            
            with open(archivo_historial, "a", encoding="utf-8") as f:
                # 2. Corregimos la estructura con los separadores "|" exactos que espera el modelo
                f.write(f"[{ahora}] COMPRA | Activo: {ticker} | Dinero usado: {cantidad:.2f} € | Acciones obtenidas: +{acciones_adquiridas:.6f} | Precio de mercado: {precio_actual:.2f} €\n")
            
            
            nuevo_saldo_simulado = saldo_ahorros - cantidad
            self.view.limpiar_campo_inversion()
            
            self.view.mostrar_exito(
                "¡Compra Realizada con Éxito!",
                f"El importe ha sido retirado de tu hucha general de ahorros.\n\n"
                f"🏢 Activo comprado: {ticker} ({self.activo_seleccionado['nombre']})\n"
                f"🛒 Fracciones adquiridas: +{acciones_adquiridas:.6f}\n"
                f"📉 Precio de mercado: {precio_actual:,.2f} €\n"
                f"💸 Fondos retirados de Ahorros: -{cantidad:,.2f} €\n"
                f"----------------------------------------\n"
                f"💰 Nuevo Saldo en Ahorros: {nuevo_saldo_simulado:,.2f} €\n"
                f"📊 Inventario total de {ticker}: {portafolio[ticker]:.6f} unidades"
            )

        except Exception as e:
            self.view.mostrar_error("Fallo del Sistema", f"No se pudo completar la transacción debido a un error: {e}")