import tkinter as tk

class AhorrosFrame(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg="#121212")
        tk.Label(self, text="MIS AHORROS", font=("Arial", 24, "bold"),
                 bg="#121212", fg="#2ecc71").pack(pady=40)
        # Aquí podrías agregar campos para ingresar montos
