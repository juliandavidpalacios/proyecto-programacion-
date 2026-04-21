import tkinter as tk
from tkinter import messagebox
import requests
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from datetime import datetime


class MonitorBitcoin:
    def __init__(self, root):
        self.root = root
        self.root.title("Monitor de Bitcoin en Tiempo Real")

        # --- Configuración de Datos ---
        self.precios = []
        self.tiempos = []

        # --- Interfaz de Tkinter ---
        self.label_titulo = tk.Label(root, text="Precio BTC/USDT", font=("Arial", 16, "bold"))
        self.label_titulo.pack(pady=10)

        self.label_precio = tk.Label(root, text="Cargando...", font=("Arial", 24), fg="green")
        self.label_precio.pack(pady=5)

        # --- Configuración de la Gráfica ---
        self.figura = Figure(figsize=(6, 4), dpi=100)
        self.ax = self.figura.add_subplot(111)
        self.ax.set_title("Evolución del Precio (Últimos minutos)")
        self.ax.set_ylabel("USD")
        self.ax.grid(True)

        self.canvas = FigureCanvasTkAgg(self.figura, master=self.root)
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

        # Iniciar el ciclo de actualización automática
        self.actualizar_datos()

    def obtener_precio(self):
        """Hace la petición a la API de Binance"""
        try:
            url = "https://api.binance.com/api/v3/ticker/price?symbol=BTCUSDT"
            respuesta = requests.get(url, timeout=5)
            datos = respuesta.json()
            return float(datos['price'])
        except Exception as e:
            print(f"Error al obtener datos: {e}")
            return None

    def actualizar_datos(self):
        """Función principal que se repite cada 10 segundos"""
        precio = self.obtener_precio()

        if precio:
            ahora = datetime.now().strftime('%H:%M:%S')

            # Guardar datos para la gráfica (limitamos a los últimos 20 puntos)
            self.precios.append(precio)
            self.tiempos.append(ahora)

            if len(self.precios) > 20:
                self.precios.pop(0)
                self.tiempos.pop(0)

            # Actualizar etiquetas de texto
            self.label_precio.config(text=f"${precio:,.2f}")

            # Actualizar la gráfica
            self.ax.clear()
            self.ax.set_title("Evolución del Precio (Actualización: 10s)")
            self.ax.grid(True, linestyle='--', alpha=0.6)
            self.ax.plot(self.tiempos, self.precios, marker='o', color='orange', linewidth=2)

            # Rotar las etiquetas del tiempo para que se lean mejor
            self.figura.autofmt_xdate()
            self.canvas.draw()

        # --- EL TRUCO MÁGICO ---
        # Programar la función para que se ejecute de nuevo en 10,000 milisegundos (10 segundos)
        self.root.after(1000, self.actualizar_datos)


# Iniciar la aplicación
if __name__ == "__main__":
    ventana = tk.Tk()
    app = MonitorBitcoin(ventana)
    ventana.mainloop()