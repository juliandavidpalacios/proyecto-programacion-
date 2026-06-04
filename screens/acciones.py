import tkinter as tk
from tkinter import ttk, messagebox
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.dates as mdates
from datetime import datetime, timedelta
import random
import os

class AccionesFrame(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg="#121212")
        self.controller = controller
        self.modo_porcentaje = True  # True = Muestra %, False = Muestra €
        self.periodo_actual = "1M"   # Periodo por defecto
        self.filtro_activo = "Todo"  # NUEVO: Filtro por defecto

        self.crear_interfaz()

    def crear_interfaz(self):
        # --- HEADER PRINCIPAL ---
        frame_header = tk.Frame(self, bg="#121212")
        frame_header.pack(fill="x", padx=25, pady=(15, 5))

        tk.Label(frame_header, text="📈 PORTAFOLIO DE INVERSIONES", font=("Arial", 18, "bold"),
                 bg="#121212", fg="white").pack(side="left")

        tk.Button(frame_header, text="➕ Nueva Inversión", font=("Arial", 10, "bold"),
                  bg="#2ecc71", fg="black", bd=0, padx=15, pady=8, cursor="hand2",
                  command=lambda: self.controller.mostrar_frame("Invertir")).pack(side="right")

        # --- RESUMEN DE SALDO Y VARIACIÓN ---
        frame_resumen = tk.Frame(self, bg="#121212")
        frame_resumen.pack(fill="x", padx=25, pady=5)

        tk.Label(frame_resumen, text="Balance Total", font=("Arial", 11), fg="#b3b3b3", bg="#121212").pack(anchor="w")

        frame_valores = tk.Frame(frame_resumen, bg="#121212")
        frame_valores.pack(fill="x")

        self.lbl_total = tk.Label(frame_valores, text="0.00 €", font=("Arial", 28, "bold"), fg="white", bg="#121212")
        self.lbl_total.pack(side="left")

        self.lbl_variacion = tk.Label(frame_valores, text="+0.00%", font=("Arial", 14, "bold"), fg="#2ecc71", bg="#121212")
        self.lbl_variacion.pack(side="left", padx=(15, 10), pady=(10, 0))

        self.btn_toggle = tk.Button(frame_valores, text="🔄 % / €", font=("Arial", 9, "bold"), bg="#333333", fg="white",
                                    bd=0, padx=8, pady=4, cursor="hand2", command=self.toggle_variacion)
        self.btn_toggle.pack(side="left", pady=(10, 0))

        # --- CONTENEDOR CENTRAL (GRÁFICO Izquierda + FILTROS Derecha) ---
        frame_central = tk.Frame(self, bg="#121212")
        frame_central.pack(fill="both", expand=True, padx=25, pady=10)

        # 1. Zona Izquierda (Gráfico)
        frame_grafico = tk.Frame(frame_central, bg="#1e1e1e", bd=1, relief="flat")
        frame_grafico.pack(side="left", fill="both", expand=True)

        self.figura = Figure(figsize=(8, 4), dpi=100, facecolor="#1e1e1e")
        self.ax = self.figura.add_subplot(111)
        self.ax.set_facecolor("#1e1e1e")
        self.ax.tick_params(colors="white")
        
        for spine in self.ax.spines.values():
            spine.set_color("#333333")

        self.canvas = FigureCanvasTkAgg(self.figura, master=frame_grafico)
        self.canvas.get_tk_widget().pack(fill="both", expand=True, padx=10, pady=10)

        # 2. Zona Derecha (Botones de Filtro)
        frame_filtros = tk.Frame(frame_central, bg="#121212")
        frame_filtros.pack(side="right", fill="y", padx=(20, 0))

        tk.Label(frame_filtros, text="Filtrar Vista:", font=("Arial", 11, "bold"), fg="#b3b3b3", bg="#121212").pack(anchor="w", pady=(0, 10))

        self.botones_filtro = {}
        # Lista de filtros con iconos
        filtros = [("🌐 Ver Todo", "Todo"), ("🏢 Acciones", "Acciones"), ("🪙 Cripto", "Cripto")]

        for texto, valor in filtros:
            btn = tk.Button(frame_filtros, text=texto, font=("Arial", 10, "bold"), bg="#333333", fg="white",
                            bd=0, width=14, pady=10, cursor="hand2",
                            command=lambda v=valor: self.cambiar_filtro(v))
            btn.pack(pady=6)
            self.botones_filtro[valor] = btn

        # --- BOTONES DE TIEMPO (Debajo del Gráfico) ---
        frame_tiempos = tk.Frame(self, bg="#121212")
        frame_tiempos.pack(pady=(0, 20), anchor="w", padx=25)

        periodos = [("1 Día", "1D"), ("1 Sem", "1S"), ("1 Mes", "1M"), ("1 Año", "1A"), ("MAX", "MAX")]
        self.botones_tiempo = {}

        for texto, valor in periodos:
            btn = tk.Button(frame_tiempos, text=texto, font=("Arial", 10, "bold"), bg="#333333", fg="white",
                            bd=0, width=8, pady=5, cursor="hand2",
                            command=lambda v=valor: self.cambiar_periodo(v))
            btn.pack(side="left", padx=(0, 10))
            self.botones_tiempo[valor] = btn

    def cargar_datos_usuario(self):
        """Se ejecuta al entrar a la pestaña"""
        self.cambiar_filtro("Todo") # Inicializa el filtro
        self.cambiar_periodo("1M")  # Inicializa el tiempo

    def toggle_variacion(self):
        self.modo_porcentaje = not self.modo_porcentaje
        self.actualizar_textos_variacion()

    def cambiar_periodo(self, periodo):
        self.periodo_actual = periodo
        self.actualizar_estilo_botones_tiempo()
        self.generar_datos_y_graficar()

    def cambiar_filtro(self, filtro):
        self.filtro_activo = filtro
        self.actualizar_estilo_filtros()
        self.generar_datos_y_graficar()

    def actualizar_estilo_botones_tiempo(self):
        color_activo = self.controller.color_btn if hasattr(self.controller, 'color_btn') else "#482673"
        for valor, btn in self.botones_tiempo.items():
            if valor == self.periodo_actual:
                btn.config(bg=color_activo, fg="white")
            else:
                btn.config(bg="#333333", fg="#b3b3b3")

    def actualizar_estilo_filtros(self):
        color_activo = self.controller.color_btn if hasattr(self.controller, 'color_btn') else "#482673"
        for valor, btn in self.botones_filtro.items():
            if valor == self.filtro_activo:
                btn.config(bg=color_activo, fg="white")
            else:
                btn.config(bg="#333333", fg="#b3b3b3")

    def generar_datos_y_graficar(self):
        """ SIMULADOR DE MERCADO (Reacciona a los filtros y al tiempo) """
        ahora = datetime.now()
        fechas = []
        valores = []

        # Configuración de tiempo
        if self.periodo_actual == "1D":
            delta = timedelta(hours=1); puntos = 24
        elif self.periodo_actual == "1S":
            delta = timedelta(hours=6); puntos = 28
        elif self.periodo_actual == "1M":
            delta = timedelta(days=1); puntos = 30
        elif self.periodo_actual == "1A":
            delta = timedelta(days=12); puntos = 30
        else: # MAX
            delta = timedelta(days=30); puntos = 36

        # Configuración de simulador según el filtro elegido
        if self.filtro_activo == "Todo":
            valor_actual = 10000.0
            volatilidad = 0.02
        elif self.filtro_activo == "Acciones":
            valor_actual = 7500.0
            volatilidad = 0.012  # Las acciones son más estables
        else: # Cripto
            valor_actual = 2500.0
            volatilidad = 0.04   # Las criptos son muy volátiles

        # Generador de datos
        for i in range(puntos):
            fechas.insert(0, ahora - (i * delta))
            valores.insert(0, valor_actual)
            cambio = valor_actual * random.uniform(-volatilidad, volatilidad)
            valor_actual -= cambio 

        self.valor_inicial = valores[0]
        self.valor_final = valores[-1]

        # Actualizar Textos
        self.lbl_total.config(text=f"{self.valor_final:,.2f} €")
        self.actualizar_textos_variacion()

        # Dibujar gráfico
        self.ax.clear()
        self.ax.grid(True, linestyle='--', alpha=0.1, color="white")
        
        color_linea = "#2ecc71" if self.valor_final >= self.valor_inicial else "#ff4c4c"
        
        self.ax.plot(fechas, valores, color=color_linea, linewidth=2)
        self.ax.fill_between(fechas, valores, min(valores)*0.99, color=color_linea, alpha=0.1)

        if self.periodo_actual == "1D":
            self.ax.xaxis.set_major_formatter(mdates.DateFormatter('%H:%M'))
        elif self.periodo_actual in ["1S", "1M"]:
            self.ax.xaxis.set_major_formatter(mdates.DateFormatter('%d %b'))
        else:
            self.ax.xaxis.set_major_formatter(mdates.DateFormatter('%b %Y'))

        self.figura.autofmt_xdate()
        self.canvas.draw()

    def actualizar_textos_variacion(self):
        if not hasattr(self, 'valor_inicial'): return
        
        diferencia = self.valor_final - self.valor_inicial
        porcentaje = (diferencia / self.valor_inicial) * 100 if self.valor_inicial != 0 else 0

        color = "#2ecc71" if diferencia >= 0 else "#ff4c4c"
        signo = "+" if diferencia >= 0 else ""

        if self.modo_porcentaje:
            texto = f"{signo}{porcentaje:.2f}%"
        else:
            texto = f"{signo}{diferencia:,.2f} €"

        self.lbl_variacion.config(text=texto, fg=color)

    def abrir_ventana_invertir(self):
        ventana_inv = tk.Toplevel(self)
        ventana_inv.title("Mercado de Inversiones")
        ventana_inv.geometry("450x300")
        ventana_inv.configure(bg="#121212")
        ventana_inv.resizable(False, False)
        
        ventana_inv.transient(self)
        ventana_inv.grab_set()

        tk.Label(ventana_inv, text="🚀 Nueva Inversión", font=("Arial", 16, "bold"), fg="#00ffcc", bg="#121212").pack(pady=(30, 10))
        
        mensaje = "Aquí se listarán las acciones (AAPL, TSLA...)\ny criptomonedas (BTC, ETH...).\n\nPodrás comprar y se añadirán\na tu portafolio personal."
        tk.Label(ventana_inv, text=mensaje, font=("Arial", 11), fg="#b3b3b3", bg="#121212", justify="center").pack(pady=10)
        
        tk.Button(ventana_inv, text="Entendido", command=ventana_inv.destroy,
                  font=("Arial", 11, "bold"), bg="#482673", fg="white", bd=0, pady=8, width=15, cursor="hand2").pack(pady=20)