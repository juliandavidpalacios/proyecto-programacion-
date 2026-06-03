import tkinter as tk
from tkinter import ttk
import requests
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from datetime import datetime
import matplotlib.dates as mdates

# Heredamos de tk.Frame para que View.py lo pueda meter en su cuadrícula (grid)
class AccionesFrame(tk.Frame):
    def __init__(self, parent, controller):
        # Inicializamos el Frame con el fondo oscuro de la app principal
        super().__init__(parent, bg="#121212")
        self.controller = controller

        # Creamos dos sub-contenedores internos para cambiar de vista sin salir de este Frame
        self.vista_selector = tk.Frame(self, bg="#121212")
        self.vista_grafico = tk.Frame(self, bg="#121212")

        # Por defecto, mostramos la pantalla de selección
        self.vista_selector.pack(fill="both", expand=True)
        self.crear_vista_selector()

    def crear_vista_selector(self):
        """Diseña la interfaz de selección (Buscador/Dropdown)"""
        frame_centro = tk.Frame(self.vista_selector, bg="#121212")
        frame_centro.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

        tk.Label(frame_centro, text="📊 Selecciona una Moneda", font=("Arial", 16, "bold"), fg="white", bg="#121212").pack(pady=20)

        opciones = ["BTCUSDT", "ETHUSDT", "SOLUSDT", "BNBUSDT", "ADAUSDT", "DOGEUSDT", "XRPUSDT"]
        
        self.combo_busqueda = ttk.Combobox(frame_centro, values=opciones, font=("Arial", 14), state="readonly", justify="center")
        self.combo_busqueda.set(opciones[0]) 
        self.combo_busqueda.pack(pady=10)

        # Usamos el color de botón de la app principal (#482673)
        btn_buscar = tk.Button(frame_centro, text="Ver Gráfico", command=self.abrir_grafico, 
                               font=("Arial", 12, "bold"), bg="#482673", fg="white", 
                               width=15, bd=0, pady=10, cursor="hand2")
        btn_buscar.pack(pady=20)

    def abrir_grafico(self):
        """Oculta el selector y construye la pantalla de la gráfica"""
        self.symbol = self.combo_busqueda.get().upper()
        self.periodo_actual = "Hoy"

        # Ocultamos el selector y mostramos el contenedor del gráfico
        self.vista_selector.pack_forget()
        self.vista_grafico.pack(fill="both", expand=True)

        # Limpiamos cualquier gráfico anterior para evitar duplicados si regresamos y entramos de nuevo
        for widget in self.vista_grafico.winfo_children():
            widget.destroy()

        # --- Reconstrucción de tu interfaz gráfica dentro del frame ---
        top_frame = tk.Frame(self.vista_grafico, bg="#121212")
        top_frame.pack(fill=tk.X, pady=10, padx=10)

        # Botón Volver modificado para regresar al selector interno
        tk.Button(top_frame, text="⬅ Volver", command=self.volver_al_selector, 
                  bg="#ff4c4c", fg="white", font=("Arial", 10, "bold"), bd=0, padx=10, pady=5, cursor="hand2").pack(side=tk.LEFT)

        self.label_titulo = tk.Label(top_frame, text=f"Precio {self.symbol}", font=("Arial", 16, "bold"), fg="white", bg="#121212")
        self.label_titulo.pack(side=tk.LEFT, expand=True)

        self.label_precio = tk.Label(self.vista_grafico, text="Cargando...", font=("Arial", 24), fg="#00ffcc", bg="#121212")
        self.label_precio.pack(pady=5)

        # Botones de Temporalidad
        frame_botones = tk.Frame(self.vista_grafico, bg="#121212")
        frame_botones.pack(pady=5)

        self.botones = {}
        temporadas = [("Hoy", "Today"), ("Semana", "Week"), ("Mes", "Month"), ("Año", "Year")]
        for col, (id_per, texto) in enumerate(temporadas):
            btn = tk.Button(frame_botones, text=texto, command=lambda p=id_per: self.cambiar_vista(p), width=10, bd=0, pady=5, cursor="hand2")
            btn.grid(row=0, column=col, padx=5)
            self.botones[id_per] = btn

        # Configuración de la Gráfica (Adaptada a Modo Oscuro para que se vea increíble)
        self.figura = Figure(figsize=(7, 3.8), dpi=100, facecolor="#121212")
        self.ax = self.figura.add_subplot(111)
        self.ax.set_facecolor("#1e1e1e")
        self.ax.spines['bottom'].set_color('white')
        self.ax.spines['top'].set_color('white')
        self.ax.spines['left'].set_color('white')
        self.ax.spines['right'].set_color('white')
        self.ax.tick_params(colors='white')
        self.ax.yaxis.label.set_color('white')
        self.ax.set_ylabel("USD")
        
        self.canvas = FigureCanvasTkAgg(self.figura, master=self.vista_grafico)
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True, padx=10, pady=5)

        self.actualizar_colores_botones()
        self.actualizar_datos()

    def volver_al_selector(self):
        """Regresa a la vista del buscador de monedas"""
        self.vista_grafico.pack_forget()
        self.vista_selector.pack(fill="both", expand=True)

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
                boton.config(bg="#482673", fg="white", font=("Arial", 10, "normal"))

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
            self.ax.set_title(f"Histórico de Precio: {self.periodo_actual}", color="white")
            self.ax.grid(True, linestyle='--', alpha=0.3, color="white")
            self.ax.plot(tiempos_hist, precios_hist, marker='.', color='#00ffcc', linewidth=2, markersize=6)
            
            formato_fecha = '%H:%M' if self.periodo_actual == "Hoy" else '%Y-%m-%d'
            self.ax.xaxis.set_major_formatter(mdates.DateFormatter(formato_fecha))
            
            self.figura.autofmt_xdate()
            self.canvas.draw()

        except Exception as e:
            print(f"Error gráfico: {e}")

    def actualizar_datos(self):
        # Control de seguridad: Si el usuario regresó al selector o cambió de menú lateral, detenemos el bucle loop
        if not hasattr(self, 'label_precio') or not self.label_precio.winfo_exists():
            return

        precio = self.obtener_precio_actual()
        if precio:
            self.label_precio.config(text=f"${precio:,.2f}")

        self.mostrar_historico()
        # Volvemos a ejecutar en 10 segundos usando el método del frame
        self.after(10000, self.actualizar_datos)