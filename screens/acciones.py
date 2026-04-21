import tkinter as tk


# Asegúrate de que el nombre sea exactamente AccionesFrame (con la A y F mayúsculas)
class AccionesFrame(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg="#121212")

        tk.Label(self, text="ACCIONES", font=("Arial", 24, "bold"),
                 bg="#121212", fg="white").pack(pady=40)

        tk.Label(self, text="Aquí podrás gestionar tus acciones financieras.",
                 bg="#121212", fg="#A0A0A0").pack()