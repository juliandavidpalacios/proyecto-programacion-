# Importamos el paquete de desarrollo de interfaces gráficas tkinter
import tkinter as tk
# Importamos los componentes modernos con estilos ttk de tkinter
from tkinter import ttk
# Importamos el contenedor de figuras vectoriales de matplotlib
from matplotlib.figure import Figure
# Importamos el conector especializado para incrustar gráficos de matplotlib dentro de ventanas tkinter
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


# Definimos la clase del Frame visual que hereda todas las propiedades de un tk.Frame
class InvertirView(tk.Frame):
    # Constructor de la interfaz gráfica que recibe el contenedor de origen y el controlador principal
    def __init__(self, parent, controller):
        # Invoca al constructor de la clase superior tk.Frame configurando el color de fondo oscuro de fondo
        super().__init__(parent, bg="#121212")
        # Enlaza la referencia del controlador global de la aplicación a una variable interna
        self.controller = controller
        # Inicializa una propiedad vacía que guardará la referencia de su objeto Presentador asignado
        self.presenter = None

    # Método público para vincular el presentador correspondiente a esta vista (Inyección de dependencias)
    def set_presenter(self, presenter):
        # Asigna la instancia del presentador a la variable de control local de la vista
        self.presenter = presenter
        # Lanza el método de dibujo para renderizar la interfaz en pantalla una vez conectado el presentador
        self.crear_interfaz()

    # Método encargado del diseño, empaquetado y maquetación de todos los widgets visuales de la pantalla
    def crear_interfaz(self):
        # Crea un subcontenedor superior para almacenar el título y el botón de navegación hacia atrás
        frame_top = tk.Frame(self, bg="#121212")
        # Empaqueta el contenedor superior expandiéndolo horizontalmente con márgenes definidos
        frame_top.pack(fill="x", padx=25, pady=(15, 5))

        # Crea el botón de retorno estilizado con un comando lambda que ejecuta el retorno al portafolio
        tk.Button(frame_top, text="⬅ Volver a Portafolio", font=("Arial", 10, "bold"),
                  bg="#333333", fg="white", bd=0, padx=10, cursor="hand2",
                  command=lambda: self.controller.mostrar_frame("Acciones")).pack(side="left", padx=(0, 15))

        # Crea la etiqueta de texto fija del encabezado con tipografía grande y llamativa en color blanco
        tk.Label(frame_top, text="🛒 MERCADO DE INVERSIONES", font=("Arial", 18, "bold"), bg="#121212", fg="white").pack(
            side="left")

        # Crea el contenedor general para albergar las dos columnas principales (Explorador y Detalle)
        main_container = tk.Frame(self, bg="#121212")
        # Distribuye el contenedor principal llenando todo el espacio disponible en ambos ejes de la app
        main_container.pack(fill="both", expand=True, padx=25, pady=10)

        # 1. PANEL IZQUIERDO: LISTA DE MERCADO
        # Instancia un contenedor con borde decorativo y título integrado para explorar el mercado
        frame_lista = tk.LabelFrame(main_container, text=" Explorador ", font=("Arial", 11, "bold"), fg="#00ffcc",
                                    bg="#121212", bd=1)
        # Lo posiciona alineado a la izquierda estirándose verticalmente en su totalidad
        frame_lista.pack(side="left", fill="y", ipadx=10)

        # Instancia la clase Style para modificar los aspectos nativos de los componentes ttk
        estilo = ttk.Style()
        # Selecciona el tema 'clam' como base para poder redefinir los colores de las pestañas
        estilo.theme_use('clam')
        # Configura el color de fondo general del contenedor Notebook a tono negro oscuro
        estilo.configure("TNotebook", background="#121212", borderwidth=0)
        # Configura las pestañas inactivas con fondo grisáceo, letras blancas y relleno interno simétrico
        estilo.configure("TNotebook.Tab", background="#333333", foreground="white", padding=[10, 5])
        # Define una regla de mapeo dinámico para cambiar el fondo de la pestaña activa a morado intenso
        estilo.map("TNotebook.Tab", background=[("selected", "#482673")])

        # Instancia el control Notebook (pestañas) y le asocia el estilo personalizado creado antes
        self.notebook = ttk.Notebook(frame_lista, style="TNotebook")
        # Empaqueta el control de pestañas expandiéndolo para ocupar todo el espacio del menú lateral
        self.notebook.pack(fill="both", expand=True, padx=5, pady=5)

        # Instancia un frame oscuro que servirá como cuerpo de la pestaña de Acciones Tradicionales
        tab_acciones = tk.Frame(self.notebook, bg="#1e1e1e")
        # Añade de forma oficial el frame al panel de pestañas con su respectivo título e ícono decorativo
        self.notebook.add(tab_acciones, text="🏢 Acciones")
        # Solicita al presentador la lista de activos de la categoría Acciones para generar los botones
        for ticker in self.presenter.obtener_activos_por_categoria("Acciones"):
            # Llama a la función constructora de botones pasando los parámetros del activo
            self.crear_boton_activo(tab_acciones, "Acciones", ticker)

        # Instancia otro frame oscuro que servirá como cuerpo de la pestaña del mercado Crypto
        tab_cripto = tk.Frame(self.notebook, bg="#1e1e1e")
        # Integra el frame al Notebook bajo la pestaña identificada como Cripto
        self.notebook.add(tab_cripto, text="🪙 Cripto")
        # Recorre los tickers de criptomonedas disponibles suministrados por el presentador
        for ticker in self.presenter.obtener_activos_por_categoria("Cripto"):
            # Genera de forma dinámica los botones interactivos dentro del panel de criptomonedas
            self.crear_boton_activo(tab_cripto, "Cripto", ticker)

        # 2. PANEL DERECHO: DETALLES Y COMPRA
        # Instancia el panel derecho general que alojará la información analítica y el formulario de compra
        self.frame_detalles = tk.Frame(main_container, bg="#121212")
        # Empaqueta el panel a la derecha rellenando el espacio sobrante de la aplicación
        self.frame_detalles.pack(side="right", fill="both", expand=True, padx=(20, 0))

        # -- A. Cabecera del Activo --
        # Crea la etiqueta principal que mostrará el nombre completo del activo financiero seleccionado
        self.lbl_nombre_activo = tk.Label(self.frame_detalles, text="Selecciona un activo...",
                                          font=("Arial", 22, "bold"), bg="#121212", fg="white")
        # Alinea el título al extremo izquierdo del panel superior de detalles
        self.lbl_nombre_activo.pack(anchor="w")

        # Crea la etiqueta dedicada a proyectar el precio de mercado actual teñido de verde esmeralda
        self.lbl_precio_activo = tk.Label(self.frame_detalles, text="0.00 €", font=("Arial", 16, "bold"), bg="#121212",
                                          fg="#2ecc71")
        # Posiciona la etiqueta del precio debajo del título guardando una holgura inferior
        self.lbl_precio_activo.pack(anchor="w", pady=(0, 10))

        # -- B. Gráfico Interactivo Real --
        # Crea un frame específico para enmarcar el lienzo interactivo de la gráfica
        self.frame_grafico = tk.Frame(self.frame_detalles, bg="#1e1e1e")
        # Lo empaqueta dándole la propiedad de expansión total para la visualización gráfica
        self.frame_grafico.pack(fill="both", expand=True, pady=5)

        # Instancia el objeto base Figure definiendo proporciones, resolución interna y fondo oscuro
        self.figura = Figure(figsize=(6, 3), dpi=100, facecolor="#1e1e1e")
        # Añade un único conjunto de ejes coordenados (Subplot 1x1 en posición 1) a la figura
        self.ax = self.figura.add_subplot(111)
        # Modifica el color de fondo interno de los ejes para unificarse con el color oscuro del panel
        self.ax.set_facecolor("#1e1e1e")
        # Configura las marcas y las etiquetas de texto de ambos ejes con tamaño reducido y color blanco
        self.ax.tick_params(colors="white", labelsize=9)
        # Recorre los cuatro bordes (spines) del recuadro del gráfico matemático
        for spine in self.ax.spines.values():
            # Pinta cada línea limítrofe del gráfico con un tono gris oscuro suavizado
            spine.set_color("#333333")

        # Vincula la figura matemática de Matplotlib con el contenedor de la librería tkinter
        self.canvas = FigureCanvasTkAgg(self.figura, master=self.frame_grafico)
        # Empaqueta y despliega el widget del lienzo final ajustándolo por completo dentro de su marco
        self.canvas.get_tk_widget().pack(fill="both", expand=True, padx=5, pady=5)

        # Botones de Tiempo
        # Instancia un pequeño frame horizontal para agrupar los botones selectores de rango temporal
        frame_tiempos = tk.Frame(self.frame_detalles, bg="#121212")
        # Lo empaqueta alineándolo a la izquierda con separación vertical
        frame_tiempos.pack(anchor="w", pady=5)

        # Inicializa un diccionario vacío para guardar las referencias de cada botón de tiempo creado
        self.botones_tiempo = {}
        # Itera por el listado de rangos temporales estándares admitidos por el sistema financiero
        for t in ["1D", "1S", "1M", "1A", "MAX"]:
            # Crea un botón plano con tipografía negrita, fondo gris, cursor de mano y evento conectado al presentador
            btn = tk.Button(frame_tiempos, text=t, font=("Arial", 9, "bold"), bg="#333333", fg="white", bd=0, width=5,
                            cursor="hand2",
                            command=lambda valor=t: self.presenter.cambiar_periodo(valor))
            # Empaqueta el botón de forma secuencial a la izquierda con separación lateral mínima
            btn.pack(side="left", padx=2)
            # Almacena la referencia del botón en el diccionario usando el identificador de tiempo como clave
            self.botones_tiempo[t] = btn

        # -- C. Panel de Información (Resumen) --
        # Crea un contenedor con recuadro perimetral para mostrar la descripción fundamental del activo
        frame_info = tk.LabelFrame(self.frame_detalles, text=" Sobre este activo ", font=("Arial", 10, "bold"),
                                   fg="#b3b3b3", bg="#121212", bd=1)
        # Lo empaqueta expandiéndolo a lo ancho e inyectando márgenes y rellenos internos
        frame_info.pack(fill="x", pady=10, ipadx=10, ipady=5)

        # Crea la etiqueta informativa destinada a proyectar la industria o sector empresarial del activo
        self.lbl_sector = tk.Label(frame_info, text="Sector: -", font=("Arial", 9, "bold"), bg="#121212", fg="#00ffcc")
        # Fija la etiqueta al costado izquierdo del recuadro informativo
        self.lbl_sector.pack(anchor="w")

        # Crea un widget de tipo Message apto para autoajustar y justificar textos largos de descripción comercial
        self.txt_resumen = tk.Message(frame_info,
                                      text="Haz clic en una acción o criptomoneda en el menú lateral para ver su gráfica y resumen.",
                                      font=("Arial", 10), bg="#121212", fg="white", width=450, justify="left")
        # Despliega el bloque de texto descriptivo con alineación izquierda y margen superior
        self.txt_resumen.pack(anchor="w", pady=5)

        # -- D. Panel de Operación (Comprar) --
        # Crea la barra inferior de transacciones comerciales con fondo claro diferenciado y rellenos
        frame_comprar = tk.Frame(self.frame_detalles, bg="#1e1e1e", padx=15, pady=10)
        # Posiciona de forma estricta la barra anclada en el borde inferior de la columna de detalles
        frame_comprar.pack(fill="x", side="bottom")

        # Coloca un texto explicativo fijo pidiendo al usuario ingresar el capital a invertir
        tk.Label(frame_comprar, text="Invertir cantidad (€):", font=("Arial", 11), bg="#1e1e1e", fg="white").pack(
            side="left")
        # Crea la caja de entrada de texto nativa donde el usuario digita los fondos numéricos
        self.entry_inversion = tk.Entry(frame_comprar, font=("Arial", 12), width=15, bg="#121212", fg="white", bd=0,
                                        insertbackground="white")
        # Empaqueta la entrada de texto junto a la etiqueta previa dejando un espaciado intermedio
        self.entry_inversion.pack(side="left", padx=10)

        # Crea el botón de compra final de color verde brillante que activa la orden a través del presentador
        tk.Button(frame_comprar, text="🛒 COMPRAR", font=("Arial", 11, "bold"), bg="#2ecc71", fg="black", bd=0, padx=20,
                  cursor="hand2",
                  command=lambda: self.presenter.ejecutar_compra()).pack(side="right")

    # Método para instanciar botones individuales dentro de las pestañas de selección de mercado
    def crear_boton_activo(self, parent, categoria, ticker):
        # Solicita al presentador la información de precio asociada al ticker de la iteración
        precio = self.presenter.obtener_precio_inicial(categoria, ticker)
        # Crea un botón ancho y plano que proyecta el identificador resumido y el valor monetario base
        btn = tk.Button(parent, text=f"{ticker}  -  {precio}€", font=("Arial", 10, "bold"),
                        bg="#333333", fg="white", bd=0, pady=10, cursor="hand2", anchor="w", padx=15,
                        command=lambda c=categoria, t=ticker: self.presenter.seleccionar_activo(c, t))
        # Empaqueta el botón expandiéndolo horizontalmente en su panel con pequeños espaciados de separación
        btn.pack(fill="x", pady=2, padx=5)