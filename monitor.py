import tkinter as tk
import requests
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from datetime import datetime
import matplotlib.dates as mdates


class MonitorCripto:
    # We added 'funcion_volver' here so the graph knows how to go back!
    def __init__(self, root, symbol, funcion_volver):
        self.root = root
        self.symbol = symbol.upper()
        self.root.title(f"Monitor Histórico - {self.symbol}")
        self.funcion_volver = funcion_volver

        self.periodo_actual = "Hoy"

        # --- Top Bar (Back Button + Title) ---
        top_frame = tk.Frame(root)
        top_frame.pack(fill=tk.X, pady=5, padx=10)

        # The Back Button!
        tk.Button(top_frame, text="⬅ Volver", command=self.volver_al_menu, bg="#ff4c4c", fg="white",
                  font=("Arial", 10, "bold")).pack(side=tk.LEFT)

        self.label_titulo = tk.Label(top_frame, text=f"Precio {self.symbol}", font=("Arial", 16, "bold"))
        self.label_titulo.pack(side=tk.LEFT, expand=True)

        self.label_precio = tk.Label(root, text="Cargando...", font=("Arial", 24), fg="green")
        self.label_precio.pack(pady=5)

        # --- Botones de Temporalidad ---
        frame_botones = tk.Frame(root)
        frame_botones.pack(pady=5)

        self.botones = {}
        self.botones["Hoy"] = tk.Button(frame_botones, text="Today", command=lambda: self.cambiar_vista("Hoy"),
                                        width=10)
        self.botones["Hoy"].grid(row=0, column=0, padx=5)
        self.botones["Semana"] = tk.Button(frame_botones, text="Week", command=lambda: self.cambiar_vista("Semana"),
                                           width=10)
        self.botones["Semana"].grid(row=0, column=1, padx=5)
        self.botones["Mes"] = tk.Button(frame_botones, text="Month", command=lambda: self.cambiar_vista("Mes"),
                                        width=10)
        self.botones["Mes"].grid(row=0, column=2, padx=5)
        self.botones["Año"] = tk.Button(frame_botones, text="Year", command=lambda: self.cambiar_vista("Año"), width=10)
        self.botones["Año"].grid(row=0, column=3, padx=5)

        # --- Configuración de la Gráfica ---
        self.figura = Figure(figsize=(8, 4.5), dpi=100)
        self.ax = self.figura.add_subplot(111)
        self.ax.set_ylabel("USD")

        self.canvas = FigureCanvasTkAgg(self.figura, master=self.root)
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        self.actualizar_colores_botones()
        self.actualizar_datos()

    def volver_al_menu(self):
        """Destroys the current graph window and triggers the un-hide function from selector_cripto.py"""
        self.root.destroy()
        self.funcion_volver()

    def obtener_precio_actual(self):
        try:
            url = f"https://api.binance.com/api/v3/ticker/price?symbol={self.symbol}"
            respuesta = requests.get(url, timeout=5)
            return float(respuesta.json()['price'])
        except Exception:
            return None

    def actualizar_colores_botones(self):
        for periodo, boton in self.botones.items():
            if periodo == self.periodo_actual:
                boton.config(bg="#f2a900", fg="black", font=("Arial", 10, "bold"))
            else:
                boton.config(bg="#e0e0e0", fg="black", font=("Arial", 10, "normal"))

    def cambiar_vista(self, nuevo_periodo):
        self.periodo_actual = nuevo_periodo
        self.actualizar_colores_botones()
        self.mostrar_historico()

    def mostrar_historico(self):
        configuracion = {
            "Hoy": ("15m", 96),
            "Semana": ("2h", 84),
            "Mes": ("12h", 60),
            "Año": ("1d", 365)
        }
        intervalo, limite = configuracion[self.periodo_actual]

        try:
            url = f"https://api.binance.com/api/v3/klines?symbol={self.symbol}&interval={intervalo}&limit={limite}"
            respuesta = requests.get(url, timeout=5)
            datos = respuesta.json()

            tiempos_hist = []
            precios_hist = []

            for vela in datos:
                timestamp = vela[0] / 1000
                dt_obj = datetime.fromtimestamp(timestamp)
                tiempos_hist.append(dt_obj)
                precios_hist.append(float(vela[4]))

            self.ax.clear()
            self.ax.set_title(f"Histórico de Precio: {self.periodo_actual}")
            self.ax.grid(True, linestyle='--', alpha=0.6)
            self.ax.plot(tiempos_hist, precios_hist, marker='.', color='purple', linewidth=2, markersize=8)

            formato_fecha = '%H:%M' if self.periodo_actual == "Hoy" else '%Y-%m-%d'
            self.ax.xaxis.set_major_formatter(mdates.DateFormatter(formato_fecha))

            self.figura.autofmt_xdate()
            self.canvas.draw()

        except Exception as e:
            print(f"Error gráfico: {e}")

    def actualizar_datos(self):
        # SAFETY CHECK: If the window was closed, stop the loop so it doesn't crash
        if not self.label_precio.winfo_exists():
            return

        precio = self.obtener_precio_actual()
        if precio:
            self.label_precio.config(text=f"${precio:,.2f}", fg="green")

        self.mostrar_historico()
        self.root.after(10000, self.actualizar_datos)