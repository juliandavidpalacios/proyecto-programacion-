# Importamos el módulo general de tkinter para el ensamblaje de componentes visuales de escritorio
import tkinter as tk


# Definimos la clase de la Vista extendiendo de tk.Frame para actuar como contenedor visual estructurado
class HomeFrame(tk.Frame):
    # Método constructor que inicializa la interfaz de usuario y vincula el controlador general
    def __init__(self, parent, controller):
        # Invocamos el inicializador de la clase base Frame aplicando el color de fondo oscuro de la app
        super().__init__(parent, bg="#121212")
        # Vinculamos la referencia de navegación general provista por el controller principal
        self.controller = controller

        # Importamos dinámicamente el Modelo para aislar responsabilidades de negocio
        from Models.home_m import HomeModel
        # Importamos dinámicamente el Presentador que actuará como intermediario de flujos
        from presenters.home_p import HomePresenter
        # Inicializamos el Presentador pasándole instancias correspondientes de la Vista y el Modelo
        self.presenter = HomePresenter(self, HomeModel())

        # Ordenamos la construcción y diagramación del árbol estático de la interfaz gráfica
        self._construir_ui()

    # Método privado encargado de orquestar la distribución espacial de los widgets estáticos en pantalla
    def _construir_ui(self):
        # Creamos el panel superior horizontal (Header) asignando el fondo oscuro corporativo
        frame_header = tk.Frame(self, bg="#121212")
        # Posicionamos el Header expandiéndolo horizontalmente con márgenes perimetrales controlados
        frame_header.pack(fill="x", padx=25, pady=(18, 6))

        # Inicializamos el widget de etiqueta para mostrar la bienvenida textual al usuario conectado
        self.lbl_saludo = tk.Label(
            frame_header, text="Bienvenido", font=("Arial", 20, "bold"),
            bg="#121212", fg="white"
        )
        # Alineamos la etiqueta de bienvenida hacia la izquierda dentro del bloque del Header
        self.lbl_saludo.pack(side="left")

        # Inicializamos el widget de etiqueta destinado a plasmar la fecha actual con tonalidad tenue
        self.lbl_fecha = tk.Label(
            frame_header, text="", font=("Arial", 10),
            bg="#121212", fg="#666666"
        )
        # Alineamos la fecha a la izquierda aplicando desplazamientos específicos para su separación visual
        self.lbl_fecha.pack(side="left", padx=(14, 0), pady=(6, 0))

        # Declaramos el botón interactivo configurado para gatillar el proceso de cierre de la sesión
        btn_signout = tk.Button(
            frame_header, text="⏻  Cerrar sesión",
            font=("Arial", 10, "bold"), bg="#1e1e1e", fg="#ff4c4c",
            bd=0, padx=12, pady=6, cursor="hand2",
            activebackground="#2a2a2a", activeforeground="#ff4c4c",
            command=self.presenter.cerrar_sesion
        )
        # Fijamos el botón de cierre de sesión alineándolo en el extremo derecho del Header superior
        btn_signout.pack(side="right")

        # Creamos el panel contenedor destinado a albergar horizontalmente las tarjetas de resumen numérico
        frame_cards = tk.Frame(self, bg="#121212")
        # Acoplamos el contenedor de tarjetas dándole expansión horizontal y márgenes superiores suaves
        frame_cards.pack(fill="x", padx=25, pady=(6, 0))

        # Instanciamos y asignamos las referencias a las tarjetas de métricas llamando al método helper interno
        self.card_ahorro = self._crear_card(frame_cards, "💰 Total Ahorrado", "—", "#2ecc71")
        self.card_mes = self._crear_card(frame_cards, "📅 Aportado este mes", "—", "#00ffcc")
        self.card_invertido = self._crear_card(frame_cards, "📈 Invertido", "—", "#ffcc00")
        self.card_valor = self._crear_card(frame_cards, "💹 Valor actual", "—", "#a78bfa")

        # Diseñamos el contenedor maestro inferior para los bloques de portafolio y movimientos recientes
        frame_inferior = tk.Frame(self, bg="#121212")
        # Forzamos su expansión bidireccional ocupando eficientemente el remanente de pantalla disponible
        frame_inferior.pack(fill="both", expand=True, padx=25, pady=12)

        # Estructuramos el panel izquierdo organizativo (LabelFrame) asignado a la sección de Activos Financieros
        frame_portafolio = tk.LabelFrame(
            frame_inferior, text=" Mis Activos ",
            font=("Arial", 10, "bold"), fg="#a78bfa",
            bg="#121212", bd=1, padx=10, pady=8
        )
        # Desplegamos el panel portafolio a la izquierda permitiendo crecimiento en ambas dimensiones
        frame_portafolio.pack(side="left", fill="both", expand=True, padx=(0, 8))

        # Diseñamos la barra de cabecera que rotulará las columnas informativas de las inversiones
        frame_cab = tk.Frame(frame_portafolio, bg="#1a1a1a")
        # Acoplamos la cabecera expandiendo horizontalmente y añadiendo un espaciado inferior
        frame_cab.pack(fill="x", pady=(0, 4))
        # Iteramos en una lista de tuplas para proyectar ordenadamente los títulos, anchos y alineaciones
        for txt, w, anc in [("Activo", 80, "w"), ("Cantidad", 90, "e"), ("Precio", 90, "e"), ("Valor", 90, "e"),
                            ("±%", 70, "e")]:
            # Creamos las etiquetas de columna escalando los anchos aproximados de los caracteres textuales
            tk.Label(frame_cab, text=txt, font=("Arial", 8, "bold"),
                     fg="#666666", bg="#1a1a1a", width=w // 8, anchor=anc).pack(side="left", padx=4)

        # Instanciamos el panel interno dinámico donde se inyectarán las tuplas de activos existentes
        self.frame_filas = tk.Frame(frame_portafolio, bg="#121212")
        # Fijamos el panel interno para abarcar la totalidad espacial remanente de su contenedor base
        self.frame_filas.pack(fill="both", expand=True)

        # Definimos la etiqueta placeholder por defecto en caso de no detectarse activos de inversión
        self.lbl_sin_activos = tk.Label(
            self.frame_filas, text="Sin inversiones todavía.\nPulsa + Nueva Inversión para empezar.",
            font=("Arial", 10), fg="#444444", bg="#121212", justify="center"
        )
        # Mostramos el aviso centrado rellenando el espacio vertical intermedio
        self.lbl_sin_activos.pack(expand=True, pady=20)

        # Estructuramos el panel derecho organizativo enfocado en el tracking de movimientos de capital
        frame_historial = tk.LabelFrame(
            frame_inferior, text=" Últimos movimientos ",
            font=("Arial", 10, "bold"), fg="#2ecc71",
            bg="#121212", bd=1, padx=10, pady=8
        )
        # Posicionamos el PC historial alineándolo en el sector derecho y permitiendo su auto-expansión
        frame_historial.pack(side="right", fill="both", expand=True, padx=(8, 0))

        # Inicializamos el sub-contenedor dinámico donde se dispondrán las filas de transacciones históricas
        self.frame_movimientos = tk.Frame(frame_historial, bg="#121212")
        # Ajustamos la maquetación del sub-contenedor ocupando la totalidad del espacio de su LabelFrame
        self.frame_movimientos.pack(fill="both", expand=True)

        # Definimos el rótulo alternativo en caso de carecer de movimientos de ahorro registrados
        self.lbl_sin_mov = tk.Label(
            self.frame_movimientos, text="Sin movimientos de ahorro.",
            font=("Arial", 10), fg="#444444", bg="#121212"
        )
        # Acoplamos el rótulo posicionándolo de manera centralizada mediante paddings controlados
        self.lbl_sin_mov.pack(expand=True, pady=20)

        # Declaramos el botón de acceso rápido para interactuar y redirigir al módulo de Inversión
        btn_invertir = tk.Button(
            self, text="➕  Nueva Inversión",
            font=("Arial", 10, "bold"), bg="#2ecc71", fg="black",
            bd=0, padx=16, pady=7, cursor="hand2",
            command=lambda: self.controller.mostrar_frame("Invertir")
        )
        # Posicionamos el botón en el extremo inferior derecho de la interfaz de la vista principal
        btn_invertir.pack(anchor="e", padx=25, pady=(0, 14))

    # Método helper para generar y estilizar tarjetas modulares de indicadores financieros
    def _crear_card(self, parent, titulo, valor, color):
        # Construimos el contenedor base de la tarjeta aplicando un borde sutil con el color temático
        card = tk.Frame(parent, bg="#1e1e1e", bd=0, highlightbackground=color, highlightthickness=1)
        # Fijamos la tarjeta distribuyéndola equitativamente en sentido horizontal e inyectando un padding interno
        card.pack(side="left", fill="both", expand=True, padx=(0, 8), ipady=8)
        # Maquetamos el texto descriptivo del título de la métrica con colores contrastantes atenuados
        tk.Label(card, text=titulo, font=("Arial", 9), fg="#888888", bg="#1e1e1e").pack(pady=(8, 2))
        # Maquetamos la etiqueta de texto que reflejará dinámicamente el valor numérico en tiempo real
        lbl = tk.Label(card, text=valor, font=("Arial", 16, "bold"), fg=color, bg="#1e1e1e")
        # Posicionamos la etiqueta del valor dentro del bloque de la tarjeta modular
        lbl.pack()
        # Retornamos la referencia de la etiqueta del valor para posibilitar su actualización futura
        return lbl

    # Método visual para renderizar una fila personalizada de información asociada a un activo financiero
    def fila_activo(self, parent, ticker, cantidad, precio, valor, pct, row):
        # Alternamos la tonalidad cromática de fondo basándonos en si el índice de la fila es par o impar
        bg = "#121212" if row % 2 == 0 else "#161616"
        # Instanciamos el contenedor horizontal para la fila del activo
        frame = tk.Frame(parent, bg=bg)
        # Fijamos la fila expandiéndola horizontalmente e inyectando un espaciado vertical ínfimo
        frame.pack(fill="x", pady=1)
        # Determinamos el color verde si el porcentaje es positivo/cero, o rojo en caso de minusvalía
        color_pct = "#2ecc71" if pct >= 0 else "#ff4c4c"
        # Anteponemos un signo de suma para retornos positivos o una cadena vacía para valores negativos
        signo = "+" if pct >= 0 else ""
        # Consolidamos la matriz estructurada con los datos específicos y formatos visuales correspondientes
        datos = [
            (ticker, 80, "w", "white"),
            (f"{cantidad:.5f}", 90, "e", "#b3b3b3"),
            (f"{precio:,.2f} €", 90, "e", "#b3b3b3"),
            (f"{valor:,.2f} €", 90, "e", "white"),
            (f"{signo}{pct:.2f}%", 70, "e", color_pct),
        ]
        # Iteramos secuencialmente sobre la matriz para inyectar cada celda de datos de manera organizada
        for txt, w, anc, fg in datos:
            # Instanciamos las celdas asignando tipografías, alineaciones y colores preestablecidos
            tk.Label(frame, text=txt, font=("Arial", 9), fg=fg, bg=bg, width=w // 8, anchor=anc).pack(side="left",
                                                                                                      padx=4)

    # Método visual dedicado a pintar una línea representativa de un movimiento de flujo monetario
    def fila_movimiento(self, parent, tipo, categoria, cantidad, row):
        # Alternamos la tonalidad del fondo según el índice secuencial para mejorar la legibilidad visual
        bg = "#121212" if row % 2 == 0 else "#161616"
        # Instanciamos la subestructura del contenedor de la fila de movimiento transaccional
        frame = tk.Frame(parent, bg=bg)
        # Fijamos el sub-contenedor expandiendo su espacio en sentido horizontal
        frame.pack(fill="x", pady=1)
        # Asignamos una flecha ascendente para ingresos de capital o descendente para egresos financieros
        icono = "▲" if tipo == "Ingreso" else "▼"
        # Seleccionamos tonalidad verde para representar entradas y tonalidad roja para salidas de caja
        color = "#2ecc71" if tipo == "Ingreso" else "#ff4c4c"
        # Prefijamos el operador algebraico de adición o sustracción de acuerdo a la naturaleza de la transacción
        signo = "+" if tipo == "Ingreso" else "-"
        # Instanciamos la etiqueta contenedora del icono representativo del flujo
        tk.Label(frame, text=icono, font=("Arial", 10, "bold"), fg=color, bg=bg, width=2).pack(side="left", padx=(2, 4))
        # Instanciamos la etiqueta con la categoría textual del movimiento alineándola al sector izquierdo
        tk.Label(frame, text=categoria, font=("Arial", 9), fg="#b3b3b3", bg=bg, anchor="w", width=22).pack(side="left")
        # Instanciamos la etiqueta con el importe monetario formateado vinculándola al extremo derecho
        tk.Label(frame, text=f"{signo}{cantidad:.2f} €", font=("Arial", 9, "bold"), fg=color, bg=bg, anchor="e").pack(
            side="right", padx=6)

    # Método gatillo que invoca el refresco de los datos del usuario delegando en el Presentador
    def cargar_datos_usuario(self):
        # Redirigimos la ejecución de la carga de información hacia el presentador asignado
        self.presenter.cargar_datos_usuario()

    # =================================================================
    # MÉTODOS DE RENDERIZADO (la Vista solo pinta lo que el Presentador le ordena)
    # =================================================================
    def mostrar_fecha(self, texto):
        self.lbl_fecha.config(text=texto)

    def mostrar_saludo(self, texto):
        self.lbl_saludo.config(text=texto)

    def actualizar_resumen(self, texto_ahorro, texto_mes):
        self.card_ahorro.config(text=texto_ahorro)
        self.card_mes.config(text=texto_mes)

    def actualizar_invertido(self, texto):
        self.card_invertido.config(text=texto)

    def actualizar_valor_portafolio(self, texto):
        self.card_valor.config(text=texto)

    def limpiar_portafolio(self):
        self.limpiar_frame(self.frame_filas)

    def pintar_activo(self, ticker, cantidad, precio, valor, pct, row):
        self.fila_activo(self.frame_filas, ticker, cantidad, precio, valor, pct, row)

    def mostrar_portafolio_vacio(self):
        self.limpiar_frame(self.frame_filas)
        self.lbl_sin_activos = tk.Label(
            self.frame_filas,
            text="Sin inversiones todavía.\nPulsa + Nueva Inversión para empezar.",
            font=("Arial", 10), fg="#444444", bg="#121212", justify="center",
        )
        self.lbl_sin_activos.pack(expand=True, pady=20)

    def confirmar_cierre_sesion(self):
        """La Vista decide CÓMO confirmar (popup) y devuelve la decisión al Presentador."""
        from tkinter import messagebox
        return messagebox.askyesno("Cerrar sesión", "¿Estás seguro de que quieres cerrar sesión?")

    # Método visual para renderizar en pantalla la lista secuencial de transacciones provistas
    def poblar_movimientos(self, movs):
        # Vaciamos por completo el frame contenedor de transacciones previas
        self.limpiar_frame(self.frame_movimientos)
        # Evaluamos si la estructura de transacciones está vacía
        if not movs:
            # Desplegamos la etiqueta informativa de ausencia de registros financieros
            tk.Label(self.frame_movimientos, text="Sin movimientos de ahorro.",
                     font=("Arial", 10), fg="#444444", bg="#121212").pack(expand=True, pady=20)
            return
        # Iteramos sobre el listado indexando secuencialmente cada uno de los movimientos
        for i, (tipo, cat, cantidad) in enumerate(movs):
            # Invocamos la renderización visual de la transacción pasándole la fila correspondiente
            self.fila_movimiento(self.frame_movimientos, tipo, cat, cantidad, i)

    # Método de saneamiento visual encargado de destruir los widgets huérfanos dentro de un contenedor
    def limpiar_frame(self, frame):
        # Recorremos todos los elementos e hilos gráficos hijos indexados en el widget contenedor
        for w in frame.winfo_children():
            # Invocamos el método de destrucción interna para liberar los recursos de memoria del widget
            w.destroy()