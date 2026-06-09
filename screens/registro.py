# Importamos la librería nativa tkinter bajo el alias abreviado de tk para construir las ventanas
import tkinter as tk
# Importamos el submódulo ttk para tener acceso a componentes específicos modernos como el Combobox
from tkinter import ttk


# Definimos la clase RegistroView que hereda directamente de la infraestructura de un tk.Frame
class RegistroView(tk.Frame):
    # Constructor de la interfaz gráfica que recibe el contenedor de origen y el controlador de navegación
    def __init__(self, parent, controller):
        # Invocamos formalmente al constructor de la clase superior configurando el color de fondo oscuro de tu app
        super().__init__(parent, bg="#121212")
        # Enlazamos la referencia del controlador global de la aplicación a una variable interna de control
        self.controller = controller
        # Inicializamos la propiedad del presentador en vacío; se inyectará externamente tras instanciarlo
        self.presenter = None

    # Método encargado de inyectar la dependencia del presentador y disparar la maquetación visual de la interfaz
    def set_presenter(self, presenter):
        # Guardamos la instancia del presentador asignado en la variable interna de la vista
        self.presenter = presenter
        # Ejecutamos de forma inmediata la rutina constructora de los elementos gráficos de la pantalla
        self.crear_interfaz()

    # Método centralizado para inicializar y acomodar todos los campos y botones del formulario de registro
    def crear_interfaz(self):
        # Instanciamos el contenedor interno que agrupará de forma centralizada todas las columnas de la vista
        container = tk.Frame(self, bg="#121212")
        # Posicionamos el contenedor al 50% de los ejes X e Y de la pantalla fijando su punto de anclaje al centro
        container.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

        # Colocamos la etiqueta del título principal ocupando un espacio expandido de dos columnas en el grid
        tk.Label(container, text="🏦 Apertura de Cuenta Bancaria", font=("Arial", 18, "bold"),
                 fg="white", bg="#121212").grid(row=0, column=0, columnspan=2, pady=(0, 15))

        # --- COLUMNA 1 (Información Personal) ---
        # Invocamos la función constructora para situar el texto indicativo del campo Nombre
        self.crear_campo(container, "Nombre:", 1, 0)
        # Instanciamos el widget de entrada de texto para el nombre en la fila y columna deseadas
        self.entry_nombre = self.crear_entry(container, 2, 0)

        # Situamos el texto indicativo del campo Apellidos en la fila correspondiente
        self.crear_campo(container, "Apellidos:", 3, 0)
        # Instanciamos el entry destinado a recuperar los apellidos del cliente
        self.entry_apellidos = self.crear_entry(container, 4, 0)

        # Colocamos el texto descriptivo del documento nacional de identidad en la primera columna
        self.crear_campo(container, "DNI / NIE / Pasaporte:", 5, 0)
        # Inicializamos la caja de texto para la clave del documento de identidad
        self.entry_dni = self.crear_entry(container, 6, 0)

        # Ubicamos la etiqueta del campo de fecha de nacimiento en el grid lateral izquierdo
        self.crear_campo(container, "Fecha de Nacimiento:", 7, 0)
        # Creamos la caja de texto asignada a la fecha pasándole sus coordenadas en el layout
        self.entry_fecha = self.crear_entry(container, 8, 0)
        # Insertamos de forma inicial el texto de la máscara de guía o placeholder en la entrada de datos
        self.entry_fecha.insert(0, "DD/MM/AAAA")
        # Configuramos de forma temporal el color de las letras del placeholder a un gris opaco
        self.entry_fecha.config(fg="#555555")
        # Vinculamos el evento de entrada de foco de selección para borrar la máscara guiada mediante el presentador
        self.entry_fecha.bind("<FocusIn>", lambda e: self.presenter.fecha_focus_in(e))
        # Vinculamos el evento de pérdida de foco para restaurar la máscara si el campo quedó vacío
        self.entry_fecha.bind("<FocusOut>", lambda e: self.presenter.fecha_focus_out(e))
        # Conectamos el evento de liberación de tecla para delegar el formateo dinámico al presentador
        self.entry_fecha.bind("<KeyRelease>", lambda e: self.presenter.formatear_fecha(e))

        # --- COLUMNA 2 (Contacto y Seguridad) ---
        # Colocamos el texto indicativo del correo electrónico abriendo la segunda columna del layout
        self.crear_campo(container, "Correo Electrónico:", 1, 1)
        # Inicializamos el entry destinado a capturar la dirección de email del usuario
        self.entry_email = self.crear_entry(container, 2, 1)

        # Colocamos la etiqueta explicativa para el número telefónico en la parte superior derecha
        self.crear_campo(container, "Teléfono de contacto (9 dígitos):", 3, 1)

        # Instanciamos un subframe para acoplar de forma horizontal el combobox y el campo numérico del teléfono
        frame_tel = tk.Frame(container, bg="#121212")
        # Posicionamos el subframe en la cuadrícula con márgenes y alineación fija hacia el oeste (izquierda)
        frame_tel.grid(row=4, column=1, padx=20, pady=5, sticky="w")

        # Solicitamos al presentador mapear los datos del modelo para generar las opciones de la lista desplegable
        opciones_paises = [f"{info['bandera']} {info['prefijo']} ({pais})" for pais, info in self.presenter.obtener_paises().items()]

        # Instanciamos el selector desplegable Combobox limitando su estado a solo lectura y definiendo sus dimensiones
        self.combo_pais = ttk.Combobox(frame_tel, values=opciones_paises, state="readonly", width=16,
                                       font=("Arial", 11))
        # Establecemos de forma explícita el país España como la opción seleccionada por defecto del control
        self.combo_pais.set("🇪🇸 +34 (España)")
        # Empaquetamos el Combobox alineándolo a la izquierda del subframe telefónico
        self.combo_pais.pack(side="left")

        # Registramos el validador de caracteres en la ventana tkinter enlazándolo a la lógica del presentador
        validador_num = self.register(lambda texto: self.presenter.limitar_telefono(texto))
        # Instanciamos la entrada de texto del teléfono inyectándole la instrucción de validación de teclas activa
        self.entry_tel = tk.Entry(frame_tel, font=("Arial", 12), width=15, bg="#1e1e1e",
                                  fg="white", insertbackground="white", bd=0,
                                  validate="key", validatecommand=(validador_num, '%P'))
        # Empaquetamos la entrada del número telefónico a un costado del combobox agregando una separación lateral
        self.entry_tel.pack(side="left", padx=(5, 0))
        # Conectamos la liberación de teclas de este entry al método de conteo de dígitos alojado en el presentador
        self.entry_tel.bind("<KeyRelease>", lambda e: self.presenter.verificar_9_digitos(e))

        # Dibujamos una línea estética inferior de color morado debajo del layout del bloque de teléfono
        tk.Frame(container, bg="#482673", height=2).grid(row=4, column=1, sticky="swe", padx=20)

        # Instanciamos la etiqueta de error destinada a proyectar los mensajes de advertencia del teléfono
        self.lbl_error_tel = tk.Label(container, text="", font=("Arial", 8), fg="#ff4c4c", bg="#121212")
        # Ubicamos la etiqueta de error telefónico justo debajo del control con márgenes de alineación
        self.lbl_error_tel.grid(row=5, column=1, sticky="w", padx=20)

        # Creamos la etiqueta descriptiva para el campo de creación de contraseña en la columna derecha
        self.crear_campo(container, "Definir Contraseña:", 5, 1)
        # Instanciamos la caja de texto cifrando los caracteres mediante el parámetro show de asterisco
        self.entry_pass = self.crear_entry(container, 6, 1, show="*")

        # Colocamos la etiqueta destinada a solicitar la confirmación idéntica de la clave de acceso
        self.crear_campo(container, "Repetir Contraseña:", 7, 1)
        # Instanciamos el último entry cifrado del formulario de datos
        self.entry_pass_confirm = self.crear_entry(container, 8, 1, show="*")

        # --- BOTONES ---
        # Instanciamos un frame horizontal inferior encargado de albergar la botonera del formulario
        btn_frame = tk.Frame(container, bg="#121212")
        # Posicionamos el contenedor de botones abarcando el ancho de ambas columnas en la fila inferior
        btn_frame.grid(row=9, column=0, columnspan=2, pady=20)

        # Creamos el botón de Confirmar Registro asociando de forma estricta su comando hacia el presentador
        tk.Button(btn_frame, text="Confirmar Registro", command=lambda: self.presenter.ejecutar_registro(),
                  font=("Arial", 11, "bold"), bg="#482673", fg="white",
                  width=20, bd=0, pady=10, cursor="hand2").pack(side="left", padx=10)

        # Creamos el botón de Cancelar cuya instrucción lambda redirige al método de retorno del controlador global
        tk.Button(btn_frame, text="Cancelar", command=lambda: self.controller.regresar_al_login(),
                  font=("Arial", 11, "bold"), bg="#333333", fg="white",
                  width=20, bd=0, pady=10, cursor="hand2").pack(side="left", padx=10)

    # Método de utilidad interno para estandarizar el pintado de las etiquetas informativas del formulario
    def crear_campo(self, parent, texto, row, col):
        # Instancia la etiqueta con color gris claro y la empaqueta en la rejilla con márgenes superiores fijos
        tk.Label(parent, text=texto, font=("Arial", 10), fg="#b3b3b3", bg="#121212").grid(row=row, column=col,
                                                                                          sticky="w", padx=20,
                                                                                          pady=(6, 0))

    # Método utilitario encargado de automatizar el diseño unificado de las cajas de texto con borde inferior morado
    def crear_entry(self, parent, row, col, show=""):
        # Instancia un entry plano sin bordes nativos aplicando el fondo oscuro e inyectando el color del cursor
        entry = tk.Entry(parent, font=("Arial", 12), width=30, bg="#1e1e1e", fg="white", insertbackground="white", bd=0,
                         show=show)
        # Ubica la caja de texto dentro de la coordenada asignada en la cuadrícula del panel principal
        entry.grid(row=row, column=col, padx=20, pady=5)
        # Instancia un frame de 2 píxeles de alto pintado de morado y lo acopla al borde inferior de la entrada de datos
        tk.Frame(parent, bg="#482673", height=2).grid(row=row, column=col, sticky="swe", padx=20)
        # Devuelve la referencia del widget Entry creado para poder enlazarlo en las variables globales de la vista
        return entry