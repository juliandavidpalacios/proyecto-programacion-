import tkinter as tk

class CuentaFrame(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg="#121212")
        self.controller = controller # Referencia a FinanceView para pedirle cambios

        tk.Label(self, text="CONFIGURACIÓN DE CUENTA", font=("Arial", 24, "bold"),
                 bg="#121212", fg="white").pack(pady=20)

        colores = [
            ("Morado", "#2D033B", "#482673"),
            ("Azul", "#0D47A1", "#1976D2"),
            ("Naranja", "#E65100", "#F57C00"),
            ("Verde Selva", "#1B5E20", "#2E7D32")
        ]

        for nombre, c_fondo, c_btn in colores:
            tk.Button(self, text=nombre, bg=c_fondo, fg="white", width=20,
                      command=lambda f=c_fondo, b=c_btn: self.controller.cambiar_color_global(f, b)).pack(pady=5)