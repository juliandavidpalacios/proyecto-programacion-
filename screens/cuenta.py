import tkinter as tk # Importa la librería base de Tkinter para la creación de interfaces gráficas

class CuentaFrame(tk.Frame): # Define el componente de interfaz CuentaFrame derivando de la clase tk.Frame de Tkinter
    def __init__(self, parent, controller): # Método constructor inicial de la vista que recibe el componente contenedor y el controlador global
        super().__init__(parent, bg="#121212") # Ejecuta el inicializador del Frame base asignándole un tono oscuro de fondo de pantalla
        self.controller = controller # Almacena de forma interna la referencia de navegación del controlador general de la aplicación
        self.archivo_actual = None # Inicializa la variable de control que guardará la ruta física del archivo del cliente activo
        self.presenter = None # Crea el atributo destinado a almacenar la instancia del objeto Presentador de la arquitectura MVP
        tk.Label(self, text="⚙️ CONFIGURACIÓN DE CUENTA", font=("Arial", 20, "bold"), bg="#121212", fg="white").pack(pady=(20, 10)) # Diseña y empaqueta el título principal superior de la interfaz de configuración en negrita
        main_container = tk.Frame(self, bg="#121212") # Instancia una caja estructural intermedia para organizar la pantalla en un sistema de columnas horizontales
        main_container.pack(fill="both", expand=True, padx=20, pady=10) # Acopla el contenedor intermedio forzando su expansión integral en todo el espacio disponible
        frame_info = tk.LabelFrame(main_container, text=" Información Personal ", font=("Arial", 11, "bold"), fg="#00ffcc", bg="#121212", bd=1) # Construye un marco perimetral con título decorativo turquesa para la sección de los datos personales
        frame_info.pack(side="left", fill="both", expand=True, padx=(0, 10)) # Posiciona el marco de información personal fijándolo al extremo izquierdo con expansión elástica total
        self.campos = {} # Inicializa un diccionario vacío de instancia para mapear las etiquetas con sus correspondientes widgets de entrada
        labels = ["Nombre Completo:", "DNI / NIE:", "Fecha de Nac.:", "Correo:", "Teléfono:"] # Define la colección de cadenas textuales fijas para rotular secuencialmente las cajas de entrada de datos
        for i, texto in enumerate(labels): # Inicia un lazo iterativo para construir ordenadamente cada fila del formulario de información personal
            tk.Label(frame_info, text=texto, font=("Arial", 10), fg="#b3b3b3", bg="#121212").grid(row=i*2, column=0, sticky="w", padx=15, pady=(5, 0)) # Instancia el rótulo de guía para el campo alineándolo hacia el extremo izquierdo mediante una rejilla grid
            entry = tk.Entry(frame_info, font=("Arial", 11), bg="#1e1e1e", fg="white", insertbackground="white", bd=0, width=35) # Crea la caja de entrada de texto estilizada con fondo gris oscuro y cursor blanco parpadeante
            entry.grid(row=i*2+1, column=0, sticky="w", padx=15, pady=2) # Ubica físicamente el cuadro de captura de texto en la fila impar consecutiva de la cuadrícula grid
            self.campos[texto] = entry # Almacena la referencia directa del widget de entrada dentro del diccionario usando el texto como clave de acceso
        frame_botones_perfil = tk.Frame(frame_info, bg="#121212") # Crea un pequeño submódulo interno para alinear horizontalmente los botones de acción del perfil
        frame_botones_perfil.grid(row=len(labels)*2, column=0, sticky="w", padx=15, pady=20) # Posiciona el submódulo al final del formulario alineándolo con márgenes inferiores amplios
        btn_guardar = tk.Button(frame_botones_perfil, text="💾 Guardar Cambios", command=lambda: self.presenter.guardar_cambios(), font=("Arial", 10, "bold"), bg="#482673", fg="white", bd=0, padx=12, pady=6, cursor="hand2") # Crea el botón de guardar cambios enlazado a la acción correspondiente dentro de la lógica del presentador
        btn_guardar.pack(side="left", padx=(0, 10)) # Acopla el botón de guardado hacia la izquierda aplicando un espaciado de holgura con el siguiente componente
        btn_pass = tk.Button(frame_botones_perfil, text="🔒 Cambiar Contraseña", command=self.abrir_ventana_cambiar_password, font=("Arial", 10, "bold"), bg="#333333", fg="#00ffcc", bd=0, padx=12, pady=6, cursor="hand2") # Define el botón de cambio de clave configurado para invocar la subventana modal de seguridad
        btn_pass.pack(side="left") # Acopla el botón de contraseña de manera lineal al lado del botón de guardado en el submódulo horizontal
        frame_colores = tk.LabelFrame(main_container, text=" Personalización de Colores ", font=("Arial", 11, "bold"), fg="#00ffcc", bg="#121212", bd=1) # Instancia el panel perimetral derecho con marco decorativo turquesa para la sección estética de temas visuales
        frame_colores.pack(side="right", fill="both", expand=True, padx=(10, 0)) # Fija la columna de configuración de temas estéticos en el extremo derecho absorbiendo espacio disponible
        tk.Label(frame_colores, text="Selecciona el tema de la aplicación:", font=("Arial", 10), fg="#b3b3b3", bg="#121212").pack(pady=10) # Añade un rótulo descriptivo para orientar al usuario en la selección cromática de la interfaz
        colores = [("Morado Imperial", "#2D033B", "#482673"), ("Azul Eléctrico", "#0D47A1", "#1976D2"), ("Naranja Atardecer", "#E65100", "#F57C00"), ("Verde Selva", "#1B5E20", "#2E7D32")] # Estructura el catálogo de tuplas conteniendo el nombre descriptivo, color base de fondo y color para botones
        for nombre, c_fondo, c_btn in colores: # Inicia el lazo cíclico para autogenerar la botonera de preajustes cromáticos globales para el sistema
            tk.Button(frame_colores, text=nombre, bg=c_fondo, fg="white", width=22, font=("Arial", 10), bd=0, pady=8, cursor="hand2", command=lambda f=c_fondo, b=c_btn: self.controller.cambiar_color_global(f, b)).pack(pady=6) # Genera cada botón de tema mapeando dinámicamente su evento de clic al método del controlador global de la aplicación
    def set_presenter(self, presenter): # Método de configuración para registrar e inyectar el presentador asociado dentro de la vista
        self.presenter = presenter # Vincula el objeto presentador recibido a la variable interna de instancia de este componente gráfico
    def cargar_datos_usuario(self): # Intercepta la llamada de activación de la pestaña delegando la lógica de negocio al presentador
        if self.presenter: # Evalúa si la referencia al presentador se encuentra correctamente enlazada y lista en la vista
            self.presenter.cargar_datos_usuario() # Delega formalmente la rutina de lectura y carga de datos de perfil al objeto presentador de la app
    def abrir_ventana_cambiar_password(self): # Método dedicado a construir, estructurar y desplegar la ventana emergente modal de contraseñas
        ventana_pass = tk.Toplevel(self) # Inicializa la ventana flotante secundaria independiente de nivel superior heredada del marco de la vista
        ventana_pass.title("Cambiar Contraseña") # Establece el encabezado textual identificador en la barra de tareas de la ventana emergente modal
        ventana_pass.geometry("360x380") # Define los valores fijos para el dimensionamiento geométrico de ancho y alto de la ventana modal
        ventana_pass.configure(bg="#121212") # Sobrescribe el color de fondo estructural de la nueva interfaz emergente aplicando el tono oscuro
        ventana_pass.resizable(False, False) # Restringe por completo cualquier manipulación o cambio de tamaño horizontal y vertical en el panel flotante
        ventana_pass.transient(self) # Subordina la existencia de la ventana emergente haciéndola dependiente directa de este panel de vista principal
        ventana_pass.grab_set() # Captura el foco y bloquea el uso de la ventana subyacente forzando la resolución prioritaria del modal externo
        tk.Label(ventana_pass, text="🔒 Actualizar Contraseña", font=("Arial", 14, "bold"), fg="#00ffcc", bg="#121212").pack(pady=15) # Renderiza el rótulo de cabecera en negrita con el tono turquesa característico dentro del modal
        tk.Label(ventana_pass, text="Contraseña Actual:", font=("Arial", 10), fg="#b3b3b3", bg="#121212").pack(anchor="w", padx=30, pady=(5,0)) # Agrega la etiqueta indicativa alineada a la izquierda para guiar en la entrada de la credencial actual
        entry_actual = tk.Entry(ventana_pass, font=("Arial", 11), bg="#1e1e1e", fg="white", insertbackground="white", bd=0, show="*", width=30) # Crea la caja de entrada de texto ocultando los caracteres ingresados mediante el uso de asteriscos de enmascaramiento
        entry_actual.pack(padx=30, pady=5) # Empaqueta el widget de entrada aplicando márgenes laterales uniformes para conservar el centrado estético
        tk.Label(ventana_pass, text="Nueva Contraseña:", font=("Arial", 10), fg="#b3b3b3", bg="#121212").pack(anchor="w", padx=30, pady=(5,0)) # Crea el rótulo guía para orientar al usuario en el ingreso de su nuevo código de seguridad secreto
        entry_nueva = tk.Entry(ventana_pass, font=("Arial", 11), bg="#1e1e1e", fg="white", insertbackground="white", bd=0, show="*", width=30) # Instancia el campo de texto enmascarado destinado a recibir la nueva clave secreta que se desea configurar
        entry_nueva.pack(padx=30, pady=5) # Agrega la caja de texto al contenedor aplicando espaciados verticales limpios para el diseño visual
        tk.Label(ventana_pass, text="Repetir Nueva Contraseña:", font=("Arial", 10), fg="#b3b3b3", bg="#121212").pack(anchor="w", padx=30, pady=(5,0)) # Añade la etiqueta explicativa de verificación obligatoria de la nueva clave de seguridad ingresada
        entry_repetir = tk.Entry(ventana_pass, font=("Arial", 11), bg="#1e1e1e", fg="white", insertbackground="white", bd=0, show="*", width=30) # Crea el último cuadro de entrada de texto enmascarado para realizar el cotejo final de las nuevas claves
        entry_repetir.pack(padx=30, pady=5) # Posiciona el componente entry aplicando márgenes para mantener la simetría gráfica de toda la ventana modal
        btn_confirmar = tk.Button(ventana_pass, text="Confirmar Cambio", command=lambda: self._confirmar_password(ventana_pass, entry_actual, entry_nueva, entry_repetir), font=("Arial", 11, "bold"), bg=self.controller.color_btn, fg="white", bd=0, pady=8, cursor="hand2") # Instancia el botón de confirmación delegando la lógica al presentador mediante un manejador interno de la vista
        btn_confirmar.pack(fill="x", padx=30, pady=25) # Empaqueta el botón final expandiéndolo por completo horizontalmente con márgenes perimetrales holgados

    # =================================================================
    # MÉTODOS DE LA VISTA (poblar campos, leer formulario y mostrar diálogos)
    # =================================================================
    def poblar_campos(self, datos): # Recibe un diccionario del presentador y rellena las cajas de texto del formulario
        mapeo = { # Traduce las claves canónicas del modelo a las claves de los widgets de esta vista
            "nombre": "Nombre Completo:",
            "dni": "DNI / NIE:",
            "fecha": "Fecha de Nac.:",
            "correo": "Correo:",
            "telefono": "Teléfono:",
        }
        for clave_dato, clave_widget in mapeo.items(): # Recorre cada par de claves a poblar
            entry = self.campos.get(clave_widget) # Localiza el widget de entrada correspondiente
            if entry is not None: # Solo actúa si el widget existe
                entry.delete(0, tk.END) # Limpia el contenido previo de la caja
                entry.insert(0, datos.get(clave_dato, "")) # Inserta el valor recibido del presentador

    def obtener_datos_formulario(self): # Lee las cajas de texto y devuelve un diccionario limpio para el presentador
        return {
            "nombre": self.campos["Nombre Completo:"].get().strip(),
            "dni": self.campos["DNI / NIE:"].get().strip(),
            "fecha": self.campos["Fecha de Nac.:"].get().strip(),
            "correo": self.campos["Correo:"].get().strip(),
            "telefono": self.campos["Teléfono:"].get().strip(),
        }

    def _confirmar_password(self, ventana_pass, entry_actual, entry_nueva, entry_repetir): # Manejador interno: lee los entries, consulta al presentador y muestra el resultado
        from tkinter import messagebox # Importación local: la Vista es la única que conoce los popups
        exito, titulo, mensaje = self.presenter.confirmar_cambio_password( # Delega la validación pasando STRINGS, no widgets
            entry_actual.get(), entry_nueva.get(), entry_repetir.get()
        )
        if exito: # Si la operación fue válida según el presentador
            messagebox.showinfo(titulo, mensaje, parent=ventana_pass) # Informa del éxito sobre la ventana modal
            ventana_pass.destroy() # Cierra la ventana modal de cambio de contraseña
        else: # Si hubo algún problema de validación
            messagebox.showerror(titulo, mensaje, parent=ventana_pass) # Muestra el error sin cerrar el modal

    def mostrar_error(self, titulo, mensaje): # Diálogo de error genérico solicitado por el presentador
        from tkinter import messagebox
        messagebox.showerror(titulo, mensaje)

    def mostrar_exito(self, titulo, mensaje): # Diálogo informativo genérico solicitado por el presentador
        from tkinter import messagebox
        messagebox.showinfo(titulo, mensaje)