import tkinter as tk
from tkinter import ttk
from monitor import MonitorCripto


class SelectorCripto:
    def __init__(self, parent):
        # 'parent' es la ventana principal real que tu compañero y tú tendrán al final.
        self.parent = parent

        # 1. Creamos NUESTRA ventana como un Toplevel (ventana hija)
        self.ventana_selector = tk.Toplevel(self.parent)
        self.ventana_selector.title("Selector de Mercados")
        self.ventana_selector.geometry("750x600")
        self.ventana_selector.configure(bg="#f0f0f0")

        # Si cierran tu selector con la 'X', destruimos solo tu ventana, no toda la app
        self.ventana_selector.protocol("WM_DELETE_WINDOW", self.ventana_selector.destroy)

        # Centramos el contenido
        frame_centro = tk.Frame(self.ventana_selector, bg="#f0f0f0")
        frame_centro.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

        tk.Label(frame_centro, text="📊 Selecciona una Moneda", font=("Arial", 16, "bold"), bg="#f0f0f0").pack(pady=20)

        opciones = ["BTCUSDT", "ETHUSDT", "SOLUSDT", "BNBUSDT", "ADAUSDT", "DOGEUSDT", "XRPUSDT"]

        self.combo_busqueda = ttk.Combobox(frame_centro, values=opciones, font=("Arial", 14), state="readonly",
                                           justify="center")
        self.combo_busqueda.set(opciones[0])
        self.combo_busqueda.pack(pady=10)

        btn_buscar = tk.Button(frame_centro, text="Abrir Gráfico", command=self.abrir_grafico,
                               font=("Arial", 12, "bold"), bg="#4CAF50", fg="white", width=15)
        btn_buscar.pack(pady=20)

    def abrir_grafico(self):
        simbolo_buscado = self.combo_busqueda.get()

        # Ocultamos el selector, ¡pero NO tocamos el programa principal del compañero!
        self.ventana_selector.withdraw()

        # Creamos la ventana de la gráfica
        self.ventana_grafico = tk.Toplevel(self.parent)
        self.ventana_grafico.geometry("750x600")

        self.ventana_grafico.protocol("WM_DELETE_WINDOW", self.mostrar_menu)

        # Llamamos a tu código de la gráfica (monitor.py se queda exactamente igual)
        self.app = MonitorCripto(self.ventana_grafico, simbolo_buscado, self.mostrar_menu)

    def mostrar_menu(self):
        # Volvemos a mostrar el selector
        self.ventana_selector.deiconify()

        if self.ventana_grafico.winfo_exists():
            self.ventana_grafico.destroy()


# --- BLOQUE DE PRUEBA ---
# Esto solo se ejecuta si corres este archivo directamente para probar tu parte.
# Cuando tu compañero importe este archivo, esto se ignorará.
if __name__ == "__main__":
    raiz_falsa = tk.Tk()
    raiz_falsa.withdraw()  # Ocultamos la raíz falsa para no molestar
    app = SelectorCripto(raiz_falsa)
    raiz_falsa.mainloop()