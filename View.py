import tkinter as tk

from screens.home import HomeFrame
from screens.ahorros import AhorrosFrame
from screens.acciones import AccionesFrame
from screens.cuenta import CuentaFrame

class FinanceView(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Tracker Financiero Modular")
        self.geometry("900x500")
        self.configure(bg="#121212")

        self.color_menu = "#2D033B"
        self.color_btn = "#482673"
        self.frames = {}

        self.menu_lateral = tk.Frame(self, bg=self.color_menu, width=200, height=500)
        self.menu_lateral.pack(side="left", fill="y")
        self.menu_lateral.pack_propagate(False)

        self.contenedor_principal = tk.Frame(self, bg="#121212")
        self.contenedor_principal.pack(side="right", expand=True, fill="both")

        self.crear_menu_botones()

        # 2. MODIFICADO: Se eliminó CategoriasFrame de la lista
        for F in (HomeFrame, AhorrosFrame, AccionesFrame, CuentaFrame):
            frame_name = F.__name__.replace("Frame", "")
            frame = F(parent=self.contenedor_principal, controller=self)
            self.frames[frame_name] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.mostrar_frame("Home")

    def crear_menu_botones(self):
        # 3. MODIFICADO: Se eliminó "Categorias" de la lista de opciones
        opciones = [
            ("Home"),
            ("Ahorros"),
            ("Acciones"),
            ("Cuenta")]
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
        self.menu_lateral.configure(bg=fondo)
        for btn in self.botones_lista:
            btn.configure(bg=boton)

if __name__ == "__main__":
    app = FinanceView()
    app.mainloop()