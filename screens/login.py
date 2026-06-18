# Importamos la librería nativa tkinter bajo el alias abreviado de tk para construir las ventanas
import tkinter as tk

# Definimos la clase LoginView que hereda directamente del contenedor gráfico tk.Frame
class LoginView(tk.Frame):
    # Definimos el constructor de la interfaz que recibe el objeto contenedor padre y el controlador de navegación
    def __init__(self, parent, controller):
        # Invocamos formalmente al constructor de la clase superior tk.Frame aplicando tu fondo oscuro personalizado
        super().__init__(parent, bg="#121212")
        # Guardamos la referencia de tu controlador global en una variable de instancia interna
        self.controller = controller
        # Inicializamos la variable del presentador en None; se inyectará de forma externa tras instanciarlo
        self.presenter = None

    # Método público diseñado para enlazar dinámicamente el presentador con su correspondiente pantalla visual
    def set_presenter(self, presenter):
        # Asignamos el objeto presentador recibido por parámetro a la propiedad local de la vista
        self.presenter = presenter
        # Ejecutamos de manera interna el método de construcción de widgets una vez establecida la conexión MVP
        self.crear_interfaz()

    # Método encargado exclusivo del diseño, empaquetado y maquetación de los elementos en la ventana
    def crear_interfaz(self):
        # Instanciamos un Frame secundario que agrupará de manera centralizada todos los campos del login
        frame_centro = tk.Frame(self, bg="#121212")
        # Posicionamos el contenedor al 50% de la pantalla en X y Y, fijando su anclaje en el centro exacto
        frame_centro.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

        # Creamos la etiqueta de encabezado principal con el ícono del candado y tipografía estilizada en negrita
        tk.Label(frame_centro, text="🔐 Acceso al Sistema", font=("Arial", 22, "bold"), fg="white", bg="#121212").pack(pady=20)

        # Creamos el texto de guía para la caja de texto del usuario o correo electrónico alineado a la izquierda
        tk.Label(frame_centro, text="Usuario / Correo", font=("Arial", 11), fg="#b3b3b3", bg="#121212").pack(anchor="w", pady=2)
        # Instanciamos la caja de entrada de texto utilizando tus variables exactas de configuración de colores oscuros
        self.entry_usuario = tk.Entry(frame_centro, font=("Arial", 12), width=28, bg="#1e1e1e", fg="white", insertbackground="white", bd=1)
        # Empaquetamos la caja de texto de usuario dentro del frame aplicando márgenes verticales simétricos
        self.entry_usuario.pack(pady=5)

        # Diseñamos el rotulo indicativo para el campo de contraseña alineándolo al costado izquierdo del layout
        tk.Label(frame_centro, text="Contraseña", font=("Arial", 11), fg="#b3b3b3", bg="#121212").pack(anchor="w", pady=2)
        # Instanciamos la caja de entrada de contraseña ocultando los caracteres reales bajo el símbolo de asterisco
        self.entry_password = tk.Entry(frame_centro, font=("Arial", 12), width=28, bg="#1e1e1e", fg="white", insertbackground="white", bd=1, show="*")
        # Empaquetamos la caja de texto de la contraseña dándole un espaciado inferior adecuado
        self.entry_password.pack(pady=5)

        # Creamos el botón de Iniciar Sesión enlazando su comando de activación directamente al presentador
        #screens/login.py (Modificación interna en btn_login)
        # ... tu código anterior de las cajas de texto ...

        # Modificamos el comando para extraer los textos y pasárselos limpios al presentador
        btn_login = tk.Button(frame_centro, text="Iniciar Sesión", 
                            command=lambda: self.presenter.verificar_login(
                                self.entry_usuario.get(), 
                                self.entry_password.get()
                            ),
                            font=("Arial", 11, "bold"), bg="#482673", fg="white",
                            width=22, bd=0, pady=8, cursor="hand2")
        btn_login.pack(pady=20)

        # ... tu código del botón de registro ...

        # Creamos tu botón plano con estilo de subrayado que invoca la función de registro en el presentador
        btn_registro = tk.Button(frame_centro, text="¿No tienes cuenta? Regístrate", command=lambda: self.presenter.crear_cuenta(),
                                 font=("Arial", 10, "underline"), bg="#121212", fg="#00ffcc",
                                 bd=0, cursor="hand2", activebackground="#121212", activeforeground="#00ffcc")
        # Empaquetamos el botón de registro al fondo del layout centrado por defecto
        btn_registro.pack()
    
    # Añade esto al final de la clase LoginView
    def mostrar_error(self, titulo, mensaje):
        """Método que el presentador llamará para indicarle a la vista que muestre un error"""
        from tkinter import messagebox
        messagebox.showerror(titulo, mensaje)