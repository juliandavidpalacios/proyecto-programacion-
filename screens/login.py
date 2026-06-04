import tkinter as tk
from tkinter import messagebox
import os

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

        # Botón de Iniciar Sesión
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

    # CORREGIDO: Ahora busca y valida las credenciales escaneando los archivos .txt reales
    def verificar_login(self):
        correo_ingresado = self.entry_usuario.get().strip()
        pass_ingresada = self.entry_password.get().strip()

        if not correo_ingresado or not pass_ingresada:
            messagebox.showerror("Error", "Por favor, rellena todos los campos.")
            return

        carpeta = "informacion_cliente"
        if not os.path.exists(carpeta) or not os.listdir(carpeta):
            messagebox.showerror("Error", "No hay usuarios registrados en el sistema.")
            return

        usuario_valido = False
        ruta_usuario = None

        # 📂 NUEVO: Escanear las subcarpetas de cada usuario
        for subcarpeta in os.listdir(carpeta):
            ruta_subcarpeta = os.path.join(carpeta, subcarpeta)
            
            # Verificamos que sea un directorio y que contenga el archivo 'perfil.txt'
            if os.path.isdir(ruta_subcarpeta):
                ruta_completa = os.path.join(ruta_subcarpeta, "perfil.txt")
                
                if os.path.exists(ruta_completa):
                    try:
                        with open(ruta_completa, "r", encoding="utf-8") as f:
                            lineas = f.readlines()
                        
                        email_ok = False
                        pass_ok = False
                        for linea in lineas:
                            if linea.startswith("Correo Electrónico:"):
                                if linea.split(":")[1].strip() == correo_ingresado:
                                    email_ok = True
                            elif linea.startswith("Contraseña:"):
                                if linea.split(":")[1].strip() == pass_ingresada:
                                    pass_ok = True
                        
                        if email_ok and pass_ok:
                            usuario_valido = True
                            ruta_usuario = ruta_completa # Le pasamos el perfil.txt a View.py
                            break
                    except Exception as e:
                        print(f"Error leyendo {ruta_completa}: {e}")

        if usuario_valido:
            self.controller.login_exitoso(ruta_usuario)
        else:
            messagebox.showerror("Error", "El correo o la contraseña son incorrectos.")