import tkinter as tk
import os
from screens.home import HomeFrame
from screens.ahorros import AhorrosFrame
from screens.acciones import AccionesFrame
from screens.cuenta import CuentaFrame
from screens.login import LoginFrame 
from screens.registro import RegistroFrame 
from screens.invertir import InvertirFrame


class FinanceView(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Tracker Financiero Modular - Banco Digital")
        self.geometry("900x500")
        self.configure(bg="#121212")

        self.usuario_logueado = None  # Guardará la ruta del archivo .txt del usuario actual

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

    def login_exitoso(self, ruta_archivo_usuario):
        self.usuario_logueado = ruta_archivo_usuario
        
        # 🎨 NUEVO: Cargar los colores personalizados guardados en el archivo .txt del usuario
        self.color_menu = "#2D033B"  # Tema por defecto si no encuentra nada
        self.color_btn = "#482673"   # Tema por defecto si no encuentra nada
        
        if os.path.exists(ruta_archivo_usuario):
            try:
                with open(ruta_archivo_usuario, "r", encoding="utf-8") as f:
                    lineas = f.readlines()
                for linea in lineas:
                    if linea.startswith("Color Fondo Menu:"):
                        self.color_menu = linea.split(":")[1].strip()
                    elif linea.startswith("Color Boton Menu:"):
                        self.color_btn = linea.split(":")[1].strip()
            except Exception as e:
                print(f"Error al cargar el tema del usuario: {e}")

        self.contenedor_auth.pack_forget()

        # El menú lateral ahora se creará automáticamente con los colores recuperados
        self.menu_lateral = tk.Frame(self, bg=self.color_menu, width=200, height=500)
        self.menu_lateral.pack(side="left", fill="y")
        self.menu_lateral.pack_propagate(False)

        self.contenedor_principal = tk.Frame(self, bg="#121212")
        self.contenedor_principal.pack(side="right", expand=True, fill="both")

        self.crear_menu_botones()

        # ✅ InvertirFrame TIENE que estar en esta lista entre los paréntesis:
        for F in (HomeFrame, AhorrosFrame, AccionesFrame, InvertirFrame, CuentaFrame): 
            frame_name = F.__name__.replace("Frame", "")
            frame = F(parent=self.contenedor_principal, controller=self)
            self.frames[frame_name] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.mostrar_frame("Home")

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
        # SI ENTRA A LA PANTALLA DE CUENTA, RECARGAMOS SUS DATOS
        if hasattr(frame, "cargar_datos_usuario"):
            frame.cargar_datos_usuario()

    def cambiar_color_global(self, fondo, boton):
        self.color_menu = fondo
        self.color_btn = boton

        if hasattr(self, 'menu_lateral'):
            self.menu_lateral.config(bg=fondo)

        if hasattr(self, 'botones_lista'):
            for btn in self.botones_lista:
                btn.config(bg=boton)
                
        # 💾 NUEVO: Guardar la nueva elección de color en el archivo .txt inmediatamente
        if self.usuario_logueado and os.path.exists(self.usuario_logueado):
            try:
                with open(self.usuario_logueado, "r", encoding="utf-8") as f:
                    lineas = f.readlines()
                
                nuevas_lineas = []
                tiene_fondo = False
                tiene_boton = False
                
                # Buscamos si ya existen las líneas de color para modificarlas
                for linea in lineas:
                    if linea.startswith("Color Fondo Menu:"):
                        nuevas_lineas.append(f"Color Fondo Menu:     {fondo}\n")
                        tiene_fondo = True
                    elif linea.startswith("Color Boton Menu:"):
                        nuevas_lineas.append(f"Color Boton Menu:     {boton}\n")
                        tiene_boton = True
                    else:
                        nuevas_lineas.append(linea)
                
                # Si es un archivo viejo o nuevo que no tenía estas líneas, las inyectamos ordenadamente
                if not tiene_fondo or not tiene_boton:
                    if nuevas_lineas and nuevas_lineas[-1].startswith("===="):
                        linea_final = nuevas_lineas.pop()
                        if not tiene_fondo: nuevas_lineas.append(f"Color Fondo Menu:     {fondo}\n")
                        if not tiene_boton: nuevas_lineas.append(f"Color Boton Menu:     {boton}\n")
                        nuevas_lineas.append(linea_final)
                    else:
                        if not tiene_fondo: nuevas_lineas.append(f"Color Fondo Menu:     {fondo}\n")
                        if not tiene_boton: nuevas_lineas.append(f"Color Boton Menu:     {boton}\n")
                        
                with open(self.usuario_logueado, "w", encoding="utf-8") as f:
                    f.writelines(nuevas_lineas)
            except Exception as e:
                print(f"Error al guardar preferencia de color: {e}")
if __name__ == "__main__":
    app = FinanceView()
    app.mainloop()