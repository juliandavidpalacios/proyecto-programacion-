# Importamos la librería os para resolver rutas lógicas del sistema de archivos local
import os
# Importamos datetime para capturar instantáneas cronológicas del sistema local
from datetime import datetime
# Importamos el framework tkinter para instanciar avisos o subpaneles dinámicos de interfaz
import tkinter as tk
# Importamos messagebox de tkinter para emitir ventanas modales de confirmación o alerta
from tkinter import messagebox

# Definimos la clase del Presentador encargada de intermediar y gobernar la lógica entre la Vista y el Modelo
class HomePresenter:
    # Método inicializador que inyecta y asocia las interfaces de la vista y del modelo de datos
    def __init__(self, view, model):
        # Guardamos la referencia de la vista para poder actualizar sus componentes gráficos
        self.view = view
        # Guardamos la referencia del modelo para solicitar transacciones de datos u operaciones I/O
        self.model = model

    # Método principal que coordina el flujo secuencial de extracción y renderizado de la información del perfil
    def cargar_datos_usuario(self):
        # Consultamos la ruta del perfil del usuario actualmente autenticado mediante el controlador de la vista
        perfil_path = self.view.controller.usuario_logueado
        # Si no localizamos un perfil válido o activo, interrumpimos el flujo de ejecución inmediatamente
        if not perfil_path:
            return

        # Actualizamos de forma directa la etiqueta de fecha del sistema en la vista con el formato correspondiente
        self.view.lbl_fecha.config(text=datetime.now().strftime("%A, %d de %B de %Y").capitalize())
        # Solicitamos al modelo la extracción del nombre del usuario leyendo el archivo físico de perfil
        nombre = self.model.leer_nombre(perfil_path)
        # Seteamos el texto estructurado del saludo de bienvenida en el elemento visual de la vista
        self.view.lbl_saludo.config(text=f"Hola, {nombre} 👋")

        # Obtenemos la ruta del directorio base que aloja los ficheros de datos del usuario
        folder = os.path.dirname(perfil_path)

        # ── PROCESAMIENTO DE AHORROS ──────────────────────────────
        # Invocamos al modelo para extraer las métricas y la colección histórica de ahorros de la carpeta
        total_ahorrado, aportado_mes, ultimos_movs = self.model.leer_ahorros(folder)
        # Formateamos el string monetario y actualizamos la tarjeta visual de ahorro total en la vista
        self.view.card_ahorro.config(text=f"{total_ahorrado:,.2f} €")
        # Formateamos el string monetario y actualizamos la tarjeta visual de aportaciones mensuales en la vista
        self.view.card_mes.config(text=f"{aportado_mes:,.2f} €")
        # Ordenamos a la vista inyectar y poblar en pantalla la sub-lista con los movimientos financieros
        self.view.poblar_movimientos(ultimos_movs)

        # ── PROCESAMIENTO DE INVERSIONES ──────────────────────────
        # Requerimos al modelo procesar e informar la suma acumulada de capital total inyectado
        total_invertido = self.model.leer_total_invertido(folder)
        # Reflejamos el cómputo final formateado dentro de la tarjeta de inversiones de la vista
        self.view.card_invertido.config(text=f"{total_invertido:,.2f} €")

        # ── PORTAFOLIO EN TIEMPO REAL ─────────────────────────────
        # Extraemos la estructura asociativa de activos actuales llamando al método del modelo
        portafolio = self.model.leer_portafolio(perfil_path)
        # Evaluamos si el portafolio contiene activos listados para su cotización
        if portafolio:
            # Ejecutamos el método interno de valuación para refrescar filas y obtener el saldo actual total
            valor_actual = self.poblar_activos(portafolio, folder)
            # Actualizamos la tarjeta visual reflejando el valor de mercado totalizado del portafolio
            self.view.card_valor.config(text=f"{valor_actual:,.2f} €")
        else:
            # Fijamos en ceros el saldo monetario de la tarjeta en la vista al no existir inversiones
            self.view.card_valor.config(text="0.00 €")
            # Limpiamos remanentes gráficos del panel de filas de activos en la interfaz de la vista
            self.view.limpiar_frame(self.view.frame_filas)
            # Re-instanciamos de forma dinámica el mensaje indicativo de portafolio vacío en la vista
            self.view.lbl_sin_activos = tk.Label(
                self.view.frame_filas,
                text="Sin inversiones todavía.\nPulsa + Nueva Inversión para empezar.",
                font=("Arial", 10), fg="#444444", bg="#121212", justify="center"
            )
            # Acoplamos el mensaje centrándolo visualmente en la pantalla de la interfaz
            self.view.lbl_sin_activos.pack(expand=True, pady=20)

    # Método de negocio intermedio encargado de coordinar la tasación de activos financieros en tiempo real
    def poblar_activos(self, portafolio, folder):
        # Limpiamos el panel visual de filas en la vista antes de reconfigurar la nueva grilla
        self.view.limpiar_frame(self.view.frame_filas)

        # Definimos el conjunto explícito de criptoactivos que necesitan conversión al formato de Yahoo Finance
        criptos    = {"BTC", "ETH", "DOGE", "ADA", "SOL", "XRP", "BNB", "LTC"}
        # Estructuramos la lista de códigos bursátiles añadiendo el sufijo de euros en caso de ser criptomonedas
        tickers_yf = [f"{t}-EUR" if t in criptos else t for t in portafolio.keys()]

        # Extraemos la matriz de costos de adquisición reales directamente desde la capa del modelo
        coste_ticker = self.model.leer_coste_por_ticker(folder)

        # Inicializamos la variable acumuladora para determinar la valorización íntegra del portafolio
        valor_total = 0.0
        # Instanciamos un diccionario local de resolución de precios
        precios     = {}

        # Verificamos si poseemos elementos en la lista de tickers para proceder con la descarga
        if tickers_yf:
            # Solicitamos al modelo la ejecución de las descargas de cotizaciones concurrentes
            precios_descargados = self.model.descargar_precios(tickers_yf)
            # Cruzamos los símbolos originales con el mapa de cotizaciones de Yahoo Finance recolectadas
            for ticker_orig, ticker_yf_str in zip(portafolio.keys(), tickers_yf):
                # Asignamos el precio descargado al ticker original o colocamos cero por defecto si se omitió
                precios[ticker_orig] = precios_descargados.get(ticker_yf_str, 0.0)

        # Iteramos sistemáticamente sobre los activos y balances del portafolio del usuario
        for i, (ticker, cantidad) in enumerate(portafolio.items()):
            # Obtenemos la cotización unitaria resuelta para el activo analizado
            precio = precios.get(ticker, 0.0)
            # Computamos la valoración de mercado actual multiplicando la cantidad por su cotización unitaria
            valor  = cantidad * precio

            # Extraemos el coste monetario histórico de adquisición asociado a este activo
            coste  = coste_ticker.get(ticker, 0.0)
            # Validamos si existe un registro de costo mayor a cero para evitar divisiones inválidas
            if coste > 0:
                # Calculamos el porcentaje de rendimiento relativo contrastando el valor actual frente al coste
                pct = (valor - coste) / coste * 100
            else:
                # Seteamos el rendimiento porcentual en cero si no disponemos de un histórico de coste
                pct = 0.0

            # Acumulamos el valor actual del activo en la variable del balance generalizado de la cartera
            valor_total    += valor
            # Ordenamos a la vista renderizar la hilera del activo inyectando los cómputos procesados
            self.view.fila_activo(self.view.frame_filas, ticker, cantidad, precio, valor, pct, i)

        # Retornamos la valuación financiera total consolidada de los activos
        return valor_total

    # Método encargado de gobernar el flujo lógico y la desconexión del entorno del usuario
    def cerrar_sesion(self):
        def cerrar_sesion(self):
            # 1. Limpiamos los datos de los formularios recorriendo los frames de la MainView
            if hasattr(self.view, "controller") and hasattr(self.view.controller, "view"):
                for frame in self.view.controller.view.frames.values():
                    if hasattr(frame, "limpiar_formulario"):
                        frame.limpiar_formulario()
                    elif hasattr(frame, "limpiar_campos"):
                        frame.limpiar_campos()

            # 2. Le avisamos al presentador principal (MainPresenter) que ejecute la salida
            self.view.controller.ejecutar_cerrar_sesion()
        # Desplegamos un cuadro de diálogo de confirmación para validar el deseo explícito de salida
        if not messagebox.askyesno("Cerrar sesión", "¿Estás seguro de que quieres cerrar sesión?"):
            return

        # Evaluamos si el marco visual de Acciones se encuentra instanciado en el gestor de la aplicación
        if "Acciones" in self.view.controller.view.frames:
            # Obtenemos la referencia concreta del frame de Acciones desde el controlador
            acciones_frame = self.view.controller.view.frames["Acciones"]
            # Si el objeto gráfico dispone del método para interrumpir procesos de actualización asíncronos
            if hasattr(acciones_frame, "detener_refresco"):
                # Ejecutamos la desconexión del hilo de refresco para prevenir fugas de memoria o cuelgues
                acciones_frame.detener_refresco()

        # Iteramos destruyendo sistemáticamente cada ventana y contenedor de la sesión de usuario
        for frame in self.view.controller.view.frames.values():
            # Destruimos la instancia del frame actual liberando la jerarquía de widgets
            frame.destroy()
        # Vaciamos por completo el diccionario de almacenamiento de vistas del controlador
        self.view.controller.frames = {}

        # Si el controlador cuenta con una barra o menú lateral de navegación instanciado
        if hasattr(self.view.controller, "menu_lateral"):
            # Procedemos a purgar y destruir los recursos del menú lateral de la interfaz
            self.view.controller.menu_lateral.destroy()
        # Si el controlador cuenta con el panel contenedor principal del área de trabajo
        if hasattr(self.view.controller, "contenedor_principal"):
            # Destruimos el contenedor central remanente de la aplicación
            self.view.controller.contenedor_principal.destroy()

        # Reseteamos la propiedad del usuario autenticado colocándola en None
        self.view.controller.usuario_logueado = None
        # Re-instanciamos de manera limpia el contenedor raíz dedicado a los procesos de autenticación
        self.view.controller.view.contenedor_auth = tk.Frame(self.view.controller.view, bg="#121212")
        # Acoplamos el contenedor expandiéndolo de manera bidireccional en el canvas principal
        self.view.controller.view.contenedor_auth.pack(fill="both", expand=True)
        # Ordenamos al controlador general proyectar la pantalla de Login inicial
        self.view.controller.view.mostrar_login()