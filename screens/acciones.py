import tkinter as tk # Importa la librería base de Tkinter para la construcción de interfaces gráficas
from tkinter import ttk, messagebox # Importa componentes temáticos de control avanzado y ventanas de alerta flotantes
from matplotlib.figure import Figure # Importa el objeto estructural de Figura de Matplotlib para renderizar gráficos
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg # Importa el componente puente para incrustar gráficos en Tkinter

class AccionesFrame(tk.Frame): # Declara el contenedor de la interfaz gráfica derivando de un Frame estándar de Tkinter
    def __init__(self, parent, controller): # Constructor inicial de la interfaz que recibe el marco padre y el orquestador global
        super().__init__(parent, bg="#121212") # Invoca el inicializador del Frame base forzando un tono oscuro de fondo de pantalla
        self.controller = controller # Almacena de forma interna la referencia de navegación del controlador general de la app
        self.presenter = None # Inicializa una propiedad vacía para inyectar y enlazar el Presentador correspondiente más adelante
        self.crear_interfaz() # Ejecuta el método interno encargado de estructurar y empaquetar todos los widgets del panel

    def set_presenter(self, presenter): # Método de enlace utilizado por la arquitectura para registrar la lógica de control externa
        self.presenter = presenter # Asocia la instancia del objeto Presentador recibido a la propiedad interna del Frame

    def crear_interfaz(self): # Método nuclear para el modelado, empaquetado y diseño estético de los componentes visuales
        frame_header = tk.Frame(self, bg="#121212") # Instancia una sección de cabecera superior con fondo oscuro para títulos y acciones
        frame_header.pack(fill="x", padx=25, pady=(15, 5)) # Acopla la cabecera forzando expansión horizontal con márgenes perimetrales
        tk.Label(frame_header, text="📈 PORTAFOLIO DE INVERSIONES", font=("Arial", 18, "bold"), bg="#121212", fg="white").pack(side="left") # Inserta el título en negrita alineado a la izquierda
        tk.Button(frame_header, text="➕ Nueva Inversión", font=("Arial", 10, "bold"), bg="#2ecc71", fg="black", bd=0, padx=15, pady=8, cursor="hand2", command=lambda: self.controller.mostrar_frame("Invertir")).pack(side="right") # Botón de compras enlazado a la navegación del controlador
        frame_resumen = tk.Frame(self, bg="#121212") # Instancia un contenedor intermedio para el balance monetario y sus fluctuaciones
        frame_resumen.pack(fill="x", padx=25, pady=5) # Posiciona el área de resúmenes con expansión horizontal y márgenes estables
        tk.Label(frame_resumen, text="Balance Total", font=("Arial", 11), fg="#b3b3b3", bg="#121212").pack(anchor="w") # Añade un rótulo descriptivo en color gris claro para el balance
        frame_valores = tk.Frame(frame_resumen, bg="#121212") # Crea un sub-marco horizontal para empaquetar de forma lineal las cifras dinámicas
        frame_valores.pack(fill="x") # Expande el sub-marco horizontalmente cubriendo toda la extensión del contenedor
        self.lbl_total = tk.Label(frame_valores, text="0.00 €", font=("Arial", 28, "bold"), fg="white", bg="#121212") # Inicializa la etiqueta gigante para el saldo monetario actual del usuario
        self.lbl_total.pack(side="left") # Alinea la cifra de balance hacia el extremo izquierdo del sub-marco
        self.lbl_variacion = tk.Label(frame_valores, text="+0.00%", font=("Arial", 14, "bold"), fg="#2ecc71", bg="#121212") # Crea la etiqueta para la métrica porcentual o absoluta de rendimiento
        self.lbl_variacion.pack(side="left", padx=(15, 10), pady=(10, 0)) # Posiciona el indicador de fluctuación aplicando un pequeño desfase vertical
        self.btn_toggle = tk.Button(frame_valores, text="🔄 % / €", font=("Arial", 9, "bold"), bg="#333333", fg="white", bd=0, padx=8, pady=4, cursor="hand2", command=lambda: self.presenter.toggle_variacion()) # Botón de alternancia enlazado de forma directa a la lógica del presentador
        self.btn_toggle.pack(side="left", pady=(10, 0)) # Ubica el botón de cambio junto a las métricas del portafolio con desfase inferior
        frame_central = tk.Frame(self, bg="#121212") # Instancia el núcleo estructural inferior dividiendo el gráfico del bloque de filtros
        frame_central.pack(fill="both", expand=True, padx=25, pady=10) # Fija la región central absorbiendo el espacio disponible de pantalla
        frame_grafico = tk.Frame(frame_central, bg="#1e1e1e", bd=1, relief="flat") # Crea la caja contenedora de fondo gris oscuro para alojar el gráfico lineal
        frame_grafico.pack(side="left", fill="both", expand=True) # Posiciona la caja del gráfico a la izquierda dándole prioridad elástica total
        self.figura = Figure(figsize=(8, 4), dpi=100, facecolor="#1e1e1e") # Inicializa la estructura de Figura de Matplotlib mimetizando los tonos de la app
        self.ax = self.figura.add_subplot(111) # Acopla un único sistema de ejes coordenados bidimensionales a la figura de Matplotlib
        self.ax.set_facecolor("#1e1e1e") # Sobrescribe el color del fondo interno de la cuadrícula del gráfico a gris oscuro
        self.ax.tick_params(colors="white") # Fuerza a las marcas numéricas de los ejes X e Y a renderizarse en color blanco puro
        for spine in self.ax.spines.values(): # Bucle perimetral encargado de recorrer las líneas de contorno del gráfico de Matplotlib
            spine.set_color("#333333") # Modifica el color de los bordes o espinas del gráfico para usar un gris tenue integrado
        self.canvas = FigureCanvasTkAgg(self.figura, master=frame_grafico) # Instancia el motor interactivo que convierte el gráfico en un widget operable por Tkinter
        self.canvas.get_tk_widget().pack(fill="both", expand=True, padx=10, pady=10) # Empaqueta el widget físico del lienzo cubriendo el interior de la caja contenedora
        frame_filtros = tk.Frame(frame_central, bg="#121212") # Crea la columna lateral derecha destinada a agrupar los botones de segregación de activos
        frame_filtros.pack(side="right", fill="y", padx=(20, 0)) # Ubica la columna de filtros a la derecha limitando su expansión solo al eje vertical
        tk.Label(frame_filtros, text="Filtrar Vista:", font=("Arial", 11, "bold"), fg="#b3b3b3", bg="#121212").pack(anchor="w", pady=(0, 10)) # Añade un encabezado de sección para el panel derecho de control
        self.botones_filtro = {} # Declara el diccionario vacío encargado de mapear los accesos directos a los objetos botones de filtrado
        filtros = [("🌐 Ver Todo", "Todo"), ("🏢 Acciones", "Acciones"), ("🪙 Cripto", "Cripto")] # Colección de tuplas que define las etiquetas de interfaz y los identificadores de tipo
        for texto, valor in filtros: # Bucle de instanciación iterativa para autogenerar el menú vertical de filtrado de portafolio
            btn = tk.Button(frame_filtros, text=texto, font=("Arial", 10, "bold"), bg="#333333", fg="white", bd=0, width=14, pady=10, cursor="hand2", command=lambda v=valor: self.presenter.cambiar_filtro(v)) # Instancia el botón apuntando al presentador
            btn.pack(pady=6) # Fija el botón del menú vertical aplicando una separación uniforme entre componentes
            self.botones_filtro[valor] = btn # Guarda la referencia física del botón en el diccionario asociándolo a su clave identificadora
        frame_tiempos = tk.Frame(self, bg="#121212") # Instancia la fila inferior horizontal de control temporal posicionada debajo de la gráfica
        frame_tiempos.pack(pady=(0, 20), anchor="w", padx=25) # Fija la barra temporal alineada a la izquierda con un espaciado inferior holgado
        periodos = [("1 Día", "1D"), ("1 Sem", "1S"), ("1 Mes", "1M"), ("1 Año", "1A"), ("MAX", "MAX")] # Colección de tuplas reguladoras para el alcance cronológico del eje horizontal
        self.botones_tiempo = {} # Inicializa el diccionario de control destinado a almacenar los botones selectores de escala temporal
        for texto, valor in periodos: # Bucle iterativo de dibujo y empaquetado para la botonera de horizontes de tiempo de inversión
            btn = tk.Button(frame_tiempos, text=texto, font=("Arial", 10, "bold"), bg="#333333", fg="white", bd=0, width=8, pady=5, cursor="hand2", command=lambda v=valor: self.presenter.cambiar_periodo(v)) # Crea el botón mapeado a la escala cronológica
            btn.pack(side="left", padx=(0, 10)) # Empaqueta horizontalmente el botón alineándolo a la izquierda con holgura lateral derecha
            self.botones_tiempo[valor] = btn # Registra la referencia del botón en el almacén de objetos usando su clave periódica

    def cargar_datos_usuario(self): # Intercepta la llamada de activación de pestaña disparada por el controlador general
        if self.presenter: # Evalúa si el objeto del presentador ha sido inyectado correctamente en el frame
            self.presenter.cargar_datos_usuario() # Delega formalmente la rutina de arranque e inicio de flujos de datos al presentador

    def actualizar_estilo_botones_tiempo(self): # Redibuja el relieve visual de los botones de tiempo basándose en la configuración activa del presentador
        color_activo = self.controller.color_btn if hasattr(self.controller, 'color_btn') else "#482673" # Determina el color institucional de resalte o usa uno violeta por defecto
        for valor, btn in self.botones_tiempo.items(): # Recorre el catálogo completo de botones de tiempo indexados
            if valor == self.presenter.periodo_actual: # Compara si la clave del botón iterado equivale al periodo seleccionado en el presentador
                btn.config(bg=color_activo, fg="white") # Aplica los colores de resalte al botón activo para denotar su selección
            else: # Para todos los botones restantes que se encuentren en estado inactivo o de reposo
                btn.config(bg="#333333", fg="#b3b3b3") # Restaura los tonos apagados neutros en los fondos del componente visual

    def actualizar_estilo_filtros(self): # Sincroniza la apariencia cromática de los botones de filtrado sectorial según el estado lógico actual
        color_activo = self.controller.color_btn if hasattr(self.controller, 'color_btn') else "#482673" # Recupera el color dinámico de enfoque desde el objeto controlador principal
        for valor, btn in self.botones_filtro.items(): # Recorre de forma secuencial las referencias de los botones almacenadas en el mapa
            if valor == self.presenter.filtro_activo: # Evalúa si el identificador coincide con la categoría activa del presentador
                btn.config(bg=color_activo, fg="white") # Destaca el botón asignándole el fondo de contraste cromático
            else: # Si el elemento iterado no coincide con el filtro activo del flujo del programa
                btn.config(bg="#333333", fg="#b3b3b3") # Devuelve las propiedades estéticas estándar de reposo oscuras al botón

    def abrir_ventana_invertir(self): # Renderiza un cuadro modal descriptivo secundario superpuesto a la aplicación principal
        ventana_inv = tk.Toplevel(self) # Instancia una ventana independiente de nivel superior heredera del marco de la aplicación
        ventana_inv.title("Mercado de Inversiones") # Establece el encabezado textual identificador en la barra del sistema del modal
        ventana_inv.geometry("450x300") # Configura las proporciones de dimensionamiento fijas de la nueva ventana flotante
        ventana_inv.configure(bg="#121212") # Fuerza al fondo estructural del modal a aplicar el esquema cromático oscuro
        ventana_inv.resizable(False, False) # Desactiva de forma estricta los controles de redimensionamiento horizontal y vertical
        ventana_inv.transient(self) # Vincula la ventana flotante como subordinada directa de este contenedor visual principal
        ventana_inv.grab_set() # Captura y bloquea el enfoque de eventos del sistema forzando al usuario a interactuar con el modal
        tk.Label(ventana_inv, text="🚀 Nueva Inversión", font=("Arial", 16, "bold"), fg="#00ffcc", bg="#121212").pack(pady=(30, 10)) # Agrega un encabezado informativo estilizado con tono turquesa
        mensaje = "Aquí se listarán las acciones (AAPL, TSLA...)\ny criptomonedas (BTC, ETH...).\n\nPodrás comprar y se añadirán\na tu portafolio personal." # Declara el bloque explicativo de texto simulado
        tk.Label(ventana_inv, text=mensaje, font=("Arial", 11), fg="#b3b3b3", bg="#121212", justify="center").pack(pady=10) # Renderiza el bloque de texto con alineación centralizada
        tk.Button(ventana_inv, text="Entendido", command=ventana_inv.destroy, font=("Arial", 11, "bold"), bg="#482673", fg="white", bd=0, pady=8, width=15, cursor="hand2").pack(pady=20) # Botón de cierre para destruir la ventana modal