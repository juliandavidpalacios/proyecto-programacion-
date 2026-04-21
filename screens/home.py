import tkinter as tk

class HomeFrame(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg="#121212")
        tk.Label(self, text="PANTALLA INICIAL", font=("Arial", 24, "bold"),
                 bg="#121212", fg="white").pack(pady=40)
        tk.Label(self, text="Bienvenido a tu resumen financiero mensual.",
                 bg="#121212", fg="#A0A0A0").pack()