import tkinter as tk

class LoginFrame(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg="#121212")
        self.controller = controller

        # Contenedor centrado en la pantalla
        frame_centro = tk.Frame(self, bg="#121212")
        frame_centro.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

        tk.Label(frame_centro, text="🔐 Acceso al Sistema", font=("Arial", 22, "bold"), fg="white", bg="#121212").pack(pady=20)

        # Campos de entrada
        tk.Label(frame_centro, text="Usuario / Correo", font=("Arial", 11), fg="#b3b3b3", bg="#121212").pack(anchor="w", pady=2)
        self.entry_usuario = tk.Entry(frame_centro, font=("Arial", 12), width=28, bg="#1e1e1e", fg="white", insertbackground="white", bd=1)
        self.entry_usuario.pack(pady=5)

        tk.Label(frame_centro, text="Contraseña", font=("Arial", 11), fg="#b3b3b3", bg="#121212").pack(anchor="w", pady=2)
        self.entry_password = tk.Entry(frame_centro, font=("Arial", 12), width=28, bg="#1e1e1e", fg="white", insertbackground="white", bd=1, show="*")
        self.entry_password.pack(pady=5)

        # Botón de Iniciar Sesión (Usa el color morado de su app)
        btn_login = tk.Button(frame_centro, text="Iniciar Sesión", command=self.verificar_login,
                              font=("Arial", 11, "bold"), bg="#482673", fg="white", 
                              width=22, bd=0, pady=8, cursor="hand2")
        btn_login.pack(pady=20)

        # Botón de Crear Cuenta
        btn_registro = tk.Button(frame_centro, text="¿No tienes cuenta? Regístrate", command=self.crear_cuenta,
                                 font=("Arial", 10, "underline"), bg="#121212", fg="#00ffcc", 
                                 bd=0, cursor="hand2", activebackground="#121212", activeforeground="#00ffcc")
        btn_registro.pack()
    
    def crear_cuenta(self):
        self.controller.mostrar_registro()

    def verificar_login(self):
        # Aquí más adelante conectarán su base de datos o lógica con archivos.
        # Por ahora, cualquier intento dará acceso para que puedan probar el flujo.
        self.controller.login_exitoso()
