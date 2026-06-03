import tkinter as tk
from screens.home import HomeFrame
from screens.ahorros import AhorrosFrame
from screens.acciones import AccionesFrame
from screens.cuenta import CuentaFrame
from screens.login import LoginFrame 
# 1. Importamos la nueva pantalla
from screens.registro import RegistroFrame 

class FinanceView(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Tracker Financiero Modular - Banco Digital")
        self.geometry("900x500")
        self.configure(bg="#121212")

        self.color_menu = "#2D033B"
        self.color_btn = "#482673"
        self.frames = {}

        # Contenedor raíz para login y registro (ocupa toda la ventana)
        self.contenedor_auth = tk.Frame(self, bg="#121212")
        self.contenedor_auth.pack(fill="both", expand=True)

        self.mostrar_login()

    def mostrar_login(self):
        self.limpiar_auth()
        self.frame_login = LoginFrame(parent=self.contenedor_auth, controller=self)
        self.frame_login.pack(fill="both", expand=True)

    def mostrar_registro(self):
        self.limpiar_auth()
        self.frame_registro = RegistroFrame(parent=self.contenedor_auth, controller=self)
        self.frame_registro.pack(fill="both", expand=True)

    def regresar_al_login(self):
        self.mostrar_login()

    def limpiar_auth(self):
        for widget in self.contenedor_auth.winfo_children():
            widget.destroy()

    def login_exitoso(self):
        # Destruimos el contenedor de autenticación completo
        self.contenedor_auth.destroy()

        # Construimos el entorno principal (Menú + Contenedor de Apps)
        self.menu_lateral = tk.Frame(self, bg=self.color_menu, width=200, height=500)
        self.menu_lateral.pack(side="left", fill="y")
        self.menu_lateral.pack_propagate(False)

        self.contenedor_principal = tk.Frame(self, bg="#121212")
        self.contenedor_principal.pack(side="right", expand=True, fill="both")

        self.crear_menu_botones()

        for F in (HomeFrame, AhorrosFrame, AccionesFrame, CuentaFrame):
            frame_name = F.__name__.replace("Frame", "")
            frame = F(parent=self.contenedor_principal, controller=self)
            self.frames[frame_name] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.mostrar_frame("Home")

    # ... (el resto de tus funciones mostrar_frame y crear_menu_botones siguen igual)

    def crear_menu_botones(self):
        opciones = ["Home", "Ahorros", "Acciones", "Cuenta"]
        self.botones_lista = []
        for texto in opciones:
            btn = tk.Button(self.menu_lateral, text=texto, bg=self.color_btn, fg="white",
                            font=("Arial", 11), bd=0, pady=15, cursor="hand2",
                            command=lambda t=texto: self.mostrar_frame(t))
            btn.pack(fill="x", pady=2)
            self.botones_lista.append(btn)

    def mostrar_frame(self, nombre):
        frame = self.frames[nombre]
        frame.tkraise()

    def cambiar_color_global(self, fondo, boton):
        # Validamos que el menú exista antes de cambiar el color por si acaso
        if hasattr(self, 'menu_lateral'):
            self.menu_lateral.configure(bg=fondo)
        if hasattr(self, 'botones_lista'):
            for btn in self.botones_lista:
                btn.configure(bg=boton)

if __name__ == "__main__":
    app = FinanceView()
    app.mainloop()