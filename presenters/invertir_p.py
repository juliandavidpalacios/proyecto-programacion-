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
            # Toda la regla de negocio y la persistencia las resuelve el MODELO.
            # El presentador solo coordina y traduce el resultado a la vista.
            exito, datos, error = self.model.registrar_compra(
                usuario_logueado, self.categoria_seleccionada, ticker, cantidad
            )

            if not exito:
                self.view.mostrar_error("Fondos Insuficientes", error)
                return

            self.view.limpiar_campo_inversion()
            self.view.mostrar_exito(
                "¡Compra Realizada con Éxito!",
                f"El importe ha sido retirado de tu hucha general de ahorros.\n\n"
                f"🏢 Activo comprado: {datos['ticker']} ({self.activo_seleccionado['nombre']})\n"
                f"🛒 Fracciones adquiridas: +{datos['acciones_adquiridas']:.6f}\n"
                f"📉 Precio de mercado: {datos['precio_actual']:,.2f} €\n"
                f"💸 Fondos retirados de Ahorros: -{datos['cantidad']:,.2f} €\n"
                f"----------------------------------------\n"
                f"💰 Nuevo Saldo en Ahorros: {datos['nuevo_saldo']:,.2f} €\n"
                f"📊 Inventario total de {datos['ticker']}: {datos['inventario_total']:.6f} unidades"
            )

        except Exception as e:
            self.view.mostrar_error("Fallo del Sistema", f"No se pudo completar la transacción debido a un error: {e}")