# Importamos la librería de interfaces gráficas nativa de Python
import tkinter as tk
# Importamos submódulos específicos para componentes avanzados y cuadros de diálogo
from tkinter import ttk, messagebox


class AhorrosFrame(tk.Frame):
    # Constructor de la interfaz gráfica que recibe el contenedor padre y el controlador del sistema
    def __init__(self, parent, controller):
        # Inicializa la clase base tk.Frame asignando el contenedor y un fondo de pantalla oscuro fijo
        super().__init__(parent, bg="#121212")
        # Guarda la referencia al objeto del controlador global para gestionar navegación
        self.controller = controller
        # Define una propiedad vacía destinada a alojar el enlace con su respectivo Presentador
        self.presenter = None

        from Models.ahorros_m import AhorrosModel
        from presenters.ahorros_p import AhorrosPresenter

        # --- TÍTULO PRINCIPAL ---
        # Crea una etiqueta de texto estática para el encabezado visual del módulo
        tk.Label(self, text="💰 PANEL DE AHORROS", font=("Arial", 18, "bold"),
                 bg="#121212", fg="white").pack(anchor="w", padx=25, pady=(15, 10))

        # --- CONTENEDOR SUPERIOR: TARJETAS DE MÉTRICAS ---
        # Crea un contenedor intermedio para alinear horizontalmente los bloques de métricas
        frame_tarjetas = tk.Frame(self, bg="#121212")
        # Posiciona el contenedor expandiéndolo horizontalmente con márgenes laterales y verticales
        frame_tarjetas.pack(fill="x", padx=25, pady=5)

        # Tarjeta 1: Total Ahorrado
        # Instancia un subframe con bordes planos y un contorno verde personalizado para el balance total
        self.card_total = tk.Frame(frame_tarjetas, bg="#1e1e1e", bd=1, relief="flat", highlightbackground="#2ecc71",
                                   highlightthickness=1)
        # Empaqueta el componente alineado a la izquierda, expandiéndose proporcionalmente con relleno interno
        self.card_total.pack(side="left", fill="both", expand=True, padx=(0, 10), ipady=10)
        # Añade la etiqueta descriptiva superior dentro de la tarjeta de balance total
        tk.Label(self.card_total, text="Total Ahorrado", font=("Arial", 10), fg="#b3b3b3", bg="#1e1e1e").pack(
            pady=(8, 2))
        # Inicializa el elemento de texto que mostrará de forma dinámica el saldo monetario acumulado
        self.lbl_total = tk.Label(self.card_total, text="0.00 €", font=("Arial", 18, "bold"), fg="#2ecc71",
                                  bg="#1e1e1e")
        # Empaqueta la etiqueta del saldo numérico en la tarjeta
        self.lbl_total.pack()

        # Tarjeta 2: Guardado este mes
        # Instancia un frame intermedio para contener los valores del rendimiento mensual de aportaciones
        self.card_mes = tk.Frame(frame_tarjetas, bg="#1e1e1e", bd=0)
        # Lo posiciona junto a la primera tarjeta distribuyendo el espacio de pantalla disponible
        self.card_mes.pack(side="left", fill="both", expand=True, padx=10, ipady=10)
        # Añade el rótulo descriptivo para identificar los aportes económicos del mes en curso
        tk.Label(self.card_mes, text="Aportado este mes", font=("Arial", 10), fg="#b3b3b3", bg="#1e1e1e").pack(
            pady=(8, 2))
        # Inicializa el widget de texto dinámico para mostrar la cifra acumulada mensual en color celeste
        self.lbl_mes = tk.Label(self.card_mes, text="0.00 €", font=("Arial", 18, "bold"), fg="#00ffcc", bg="#1e1e1e")
        # Empaqueta el widget indicador mensual dentro de su respectivo bloque contenedor
        self.lbl_mes.pack()

        # Tarjeta 3: MODIFICADO -> Dinero Invertido
        # Instancia el frame para la sección de inversiones externas recuperadas vía red
        self.card_inversiones = tk.Frame(frame_tarjetas, bg="#1e1e1e", bd=0)
        # Posiciona el elemento al final de la fila de tarjetas aplicando espaciados específicos
        self.card_inversiones.pack(side="left", fill="both", expand=True, padx=(10, 0), ipady=10)
        # Genera el texto estático indicativo para el dinero colocado en carteras de inversión
        tk.Label(self.card_inversiones, text="Dinero Invertido", font=("Arial", 10), fg="#b3b3b3", bg="#1e1e1e").pack(
            pady=(8, 2))
        # Declara la etiqueta dinámica encargada de reflejar las valoraciones financieras en color amarillo
        self.lbl_inversiones = tk.Label(self.card_inversiones, text="0.00 €", font=("Arial", 18, "bold"), fg="#ffcc00",
                                        bg="#1e1e1e")
        # Integra el elemento dinámico dentro del flujo visual de la tarjeta de inversiones
        self.lbl_inversiones.pack()

        # --- CONTENEDOR INFERIOR (FORMULARIO E HISTORIAL) ---
        # Crea la región estructurada inferior que dividirá el formulario operativo de la tabla de datos
        main_inferior = tk.Frame(self, bg="#121212")
        # Distribuye el marco ocupando toda el área inferior estirándose en ambas dimensiones
        main_inferior.pack(fill="both", expand=True, padx=25, pady=15)

        # - COLUMNA IZQUIERDA: ACCIONES / OPERACIONES -
        # Instancia un marco con título perimetral decorativo para agrupar campos de datos de aportes
        frame_acciones = tk.LabelFrame(main_inferior, text=" Nueva Aportación ", font=("Arial", 11, "bold"),
                                       fg="#2ecc71", bg="#121212", bd=1, padx=15, pady=10)
        # Fija el bloque de acciones hacia el extremo izquierdo impidiendo su deformación elástica
        frame_acciones.pack(side="left", fill="both", expand=False)

        # Genera la etiqueta para la entrada de texto de las cantidades numéricas introducidas
        tk.Label(frame_acciones, text="Cantidad (€):", font=("Arial", 10), fg="#b3b3b3", bg="#121212").pack(anchor="w",
                                                                                                            pady=(5, 2))
        # Define el campo de texto interactivo donde el usuario digitará los montos financieros
        self.entry_cantidad = tk.Entry(frame_acciones, font=("Arial", 11), bg="#1e1e1e", fg="white", bd=0,
                                       insertbackground="white")
        # Posiciona la entrada de texto configurando espaciados internos verticales para mejorar legibilidad
        self.entry_cantidad.pack(fill="x", ipady=4, pady=(0, 10))

        # Genera la etiqueta indicadora para la selección de la hucha o categoría de destino
        tk.Label(frame_acciones, text="Categoría / Hucha:", font=("Arial", 10), fg="#b3b3b3", bg="#121212").pack(
            anchor="w", pady=(5, 2))

        # Obtiene una referencia global del gestor de estilos para modificar componentes temáticos de ttk
        estilo_combo = ttk.Style()
        # Selecciona el motor gráfico nativo 'clam' para permitir la personalización avanzada del combo
        estilo_combo.theme_use('clam')
        # Aplica una configuración cromática oscura a los campos de fondo y primer plano del Combobox
        estilo_combo.configure("TCombobox", fieldbackground="#1e1e1e", background="#1e1e1e", foreground="black")

        # Instancia el widget selector de opciones con restricciones de edición manual directa
        self.combo_categoria = ttk.Combobox(frame_acciones, font=("Arial", 10), state="readonly", style="TCombobox")
        # Define la tupla estática con los nombres de las categorías de ahorro disponibles
        self.combo_categoria["values"] = ("Fondo de Emergencia", "Vacaciones ✈️", "Coche Nuevo 🚗", "Inversiones 📈",
                                          "Otros", "Cuenta")
        # Configura la primera opción del listado como la selección predeterminada de la interfaz
        self.combo_categoria.current(0)
        # Integra el menú de opciones desplegable estirándolo para cubrir el ancho de su panel
        self.combo_categoria.pack(fill="x", ipady=2, pady=(0, 15))

        # Botones de Acción
        # Crea el botón interactivo de aportes en color verde enlazado directamente a su lógica
        btn_ingresar = tk.Button(frame_acciones, text="➕ Añadir al Ahorro", font=("Arial", 10, "bold"),
                                 bg="#2ecc71", fg="black", bd=0, pady=6, cursor="hand2",
                                 command=lambda: self.presenter.ejecutar_movimiento("Ingreso"))
        # Fija el botón de ingresos expandiendo su alcance horizontal dentro del menú lateral
        btn_ingresar.pack(fill="x", pady=5)

        # Crea el botón interactivo para el retiro de fondos con advertencia en color rojo
        btn_retirar = tk.Button(frame_acciones, text="➖ Retirar Fondos", font=("Arial", 10, "bold"),
                                bg="#333333", fg="#ff4444", bd=0, pady=6, cursor="hand2",
                                command=lambda: self.presenter.ejecutar_movimiento("Retiro"))
        # Posiciona el botón de retiros de capital con márgenes estándar de separación
        btn_retirar.pack(fill="x", pady=5)

        # - COLUMNA DERECHA: TABLA DE HISTORIAL -
        # Instancia un marco perimetral con título enfocado al despliegue cronológico de operaciones
        frame_historial = tk.LabelFrame(main_inferior, text=" Historial Reciente de Ahorro ",
                                        font=("Arial", 11, "bold"),
                                        fg="#2ecc71", bg="#121212", bd=1, padx=10, pady=10)
        # Posiciona el panel hacia la derecha permitiendo su redimensionamiento elástico total
        frame_historial.pack(side="right", fill="both", expand=True, padx=(15, 0))

        # Instancia una clase de estilo exclusiva para configurar la rejilla tabular de datos de ttk
        estilo_tabla = ttk.Style()
        # Modifica la paleta cromática global del widget de tipo Treeview adaptándolo al modo oscuro
        estilo_tabla.configure("Treeview", background="#1e1e1e", foreground="white", fieldbackground="#1e1e1e",
                               rowheight=25, borderwidth=0)
        # Establece un formato plano y tipografía en negrita exclusiva para las cabeceras de columnas
        estilo_tabla.configure("Treeview.Heading", background="#2a2a2a", foreground="white", relief="flat",
                               font=("Arial", 9, "bold"))
        # Diseña la regla de contraste visual aplicada cuando el usuario selecciona filas de la rejilla
        estilo_tabla.map("Treeview", background=[('selected', '#2ecc71')], foreground=[('selected', 'black')])

        # Instancia la rejilla tabular estructurada asignándole tres columnas identificadoras únicas
        self.tabla = ttk.Treeview(frame_historial, columns=("Tipo", "Categoría", "Cantidad"), show="headings",
                                  style="Treeview")
        # Asigna el texto de visualización para la cabecera de la primera columna
        self.tabla.heading("Tipo", text="Operación")
        # Asigna el texto descriptivo expuesto para la cabecera de la segunda columna
        self.tabla.heading("Categoría", text="Categoría / Destino")
        # Configura el encabezado visible correspondiente a la tercera columna del elemento tabular
        self.tabla.heading("Cantidad", text="Monto")

        # Ajusta las dimensiones de ancho y define una alineación centrada para el tipo de operación
        self.tabla.column("Tipo", width=90, anchor="center")
        # Ajusta las dimensiones espaciales y alinea los textos de huchas hacia el extremo izquierdo
        self.tabla.column("Categoría", width=160, anchor="w")
        # Establece el ancho y fuerza la alineación contable a la derecha para las expresiones numéricas
        self.tabla.column("Cantidad", width=90, anchor="e")
        # Integra la rejilla de historial expandiéndola para abarcar toda la superficie del marco contenedor
        self.tabla.pack(fill="both", expand=True)

    # Método de enlace ejecutado por el controlador para enlazar formalmente la vista con su presentador
    def set_presenter(self, presenter):
        # Asigna el objeto presentador recibido a la propiedad interna de control
        self.presenter = presenter

    # Método desencadenador que notifica la carga inicial del cuadro una vez activado en pantalla
    def cargar_datos_usuario(self):
        # Comprueba si existe un presentador debidamente registrado en el componente de vista
        if self.presenter:
            # Delega la responsabilidad de inicialización de datos hacia el objeto presentador
            self.presenter.inicializar_sesion()

