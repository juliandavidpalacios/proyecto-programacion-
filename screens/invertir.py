import tkinter as tk
from tkinter import ttk, messagebox
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import random

class InvertirFrame(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg="#121212")
        self.controller = controller

        # --- BASE DE DATOS SIMULADA DE ACTIVOS ---
        self.base_datos = {
            "Acciones": {
                "AAPL": {"nombre": "Apple Inc.", "precio": 165.20, "sector": "Tecnología", "resumen": "Líder global en hardware, software y servicios. Creadores del iPhone, Mac y iPad. Considerada una de las empresas más valiosas del mundo."},
                "TSLA": {"nombre": "Tesla Inc.", "precio": 210.50, "sector": "Automoción", "resumen": "Empresa enfocada en la transición a energía sostenible. Fabrica vehículos eléctricos, paneles solares y baterías gigantes."},
                "AMZN": {"nombre": "Amazon.com", "precio": 140.00, "sector": "E-commerce", "resumen": "El gigante del comercio electrónico y proveedor líder de servicios en la nube (AWS)."}
            },
            "Cripto": {
                "BTC": {"nombre": "Bitcoin", "precio": 58000.00, "sector": "Criptomoneda", "resumen": "La primera criptomoneda descentralizada. Creada como reserva de valor y alternativa digital al oro. Alta volatilidad."},
                "ETH": {"nombre": "Ethereum", "precio": 3100.00, "sector": "Criptomoneda", "resumen": "Plataforma de código abierto basada en blockchain. Permite la creación de contratos inteligentes y aplicaciones descentralizadas (dApps)."}
            }
        }
        self.activo_seleccionado = None

        self.crear_interfaz()

    def crear_interfaz(self):
        # Título
        tk.Label(self, text="🛒 MERCADO DE INVERSIONES", font=("Arial", 18, "bold"), bg="#121212", fg="white").pack(anchor="w", padx=25, pady=(15, 5))

        # --- CONTENEDOR PRINCIPAL DIVIDIDO ---
        main_container = tk.Frame(self, bg="#121212")
        main_container.pack(fill="both", expand=True, padx=25, pady=10)

        # ---------------------------------------------------------
        # 1. PANEL IZQUIERDO: LISTA DE MERCADO (30%)
        # ---------------------------------------------------------
        frame_lista = tk.LabelFrame(main_container, text=" Explorador ", font=("Arial", 11, "bold"), fg="#00ffcc", bg="#121212", bd=1)
        frame_lista.pack(side="left", fill="y", ipadx=10)

        # Notebook (Pestañas) para separar Acciones y Criptos
        estilo = ttk.Style()
        estilo.theme_use('clam')
        estilo.configure("TNotebook", background="#121212", borderwidth=0)
        estilo.configure("TNotebook.Tab", background="#333333", foreground="white", padding=[10, 5])
        estilo.map("TNotebook.Tab", background=[("selected", "#482673")])

        self.notebook = ttk.Notebook(frame_lista, style="TNotebook")
        self.notebook.pack(fill="both", expand=True, padx=5, pady=5)

        # Pestaña Acciones
        tab_acciones = tk.Frame(self.notebook, bg="#1e1e1e")
        self.notebook.add(tab_acciones, text="🏢 Acciones")
        for ticker in self.base_datos["Acciones"]:
            self.crear_boton_activo(tab_acciones, "Acciones", ticker)

        # Pestaña Cripto
        tab_cripto = tk.Frame(self.notebook, bg="#1e1e1e")
        self.notebook.add(tab_cripto, text="🪙 Cripto")
        for ticker in self.base_datos["Cripto"]:
            self.crear_boton_activo(tab_cripto, "Cripto", ticker)

        # ---------------------------------------------------------
        # 2. PANEL DERECHO: DETALLES Y COMPRA (70%)
        # ---------------------------------------------------------
        self.frame_detalles = tk.Frame(main_container, bg="#121212")
        self.frame_detalles.pack(side="right", fill="both", expand=True, padx=(20, 0))

        # -- A. Cabecera del Activo --
        self.lbl_nombre_activo = tk.Label(self.frame_detalles, text="Selecciona un activo...", font=("Arial", 22, "bold"), bg="#121212", fg="white")
        self.lbl_nombre_activo.pack(anchor="w")

        self.lbl_precio_activo = tk.Label(self.frame_detalles, text="0.00 €", font=("Arial", 16, "bold"), bg="#121212", fg="#2ecc71")
        self.lbl_precio_activo.pack(anchor="w", pady=(0, 10))

        # -- B. Gráfico Interactivo (Espacio Reservado) --
        frame_grafico = tk.Frame(self.frame_detalles, bg="#1e1e1e", height=200)
        frame_grafico.pack(fill="x", pady=5)
        # Aquí irá el canvas de matplotlib igual que en acciones.py
        tk.Label(frame_grafico, text="[Gráfico Interactivo de Precios Aquí]", bg="#1e1e1e", fg="#b3b3b3", height=8).pack(expand=True)

        # Título y botón de volver
        frame_top = tk.Frame(self, bg="#121212")
        frame_top.pack(fill="x", padx=25, pady=(15, 5))
        
        tk.Button(frame_top, text="⬅ Volver a Portafolio", font=("Arial", 10, "bold"), 
                  bg="#333333", fg="white", bd=0, padx=10, cursor="hand2",
                  # ✅ CORREGIDO: Usamos padx=(0, 15) en lugar de mr=15
                  command=lambda: self.controller.mostrar_frame("Acciones")).pack(side="left", padx=(0, 15))

        tk.Label(frame_top, text="🛒 MERCADO DE INVERSIONES", font=("Arial", 18, "bold"), bg="#121212", fg="white").pack(side="left")
        # Botones de Tiempo
        frame_tiempos = tk.Frame(self.frame_detalles, bg="#121212")
        frame_tiempos.pack(anchor="w", pady=5)
        for t in ["1D", "1S", "1M", "1A", "MAX"]:
            tk.Button(frame_tiempos, text=t, font=("Arial", 9), bg="#333333", fg="white", bd=0, width=5).pack(side="left", padx=2)

        # -- C. Panel de Información (Resumen) --
        frame_info = tk.LabelFrame(self.frame_detalles, text=" Sobre este activo ", font=("Arial", 10, "bold"), fg="#b3b3b3", bg="#121212", bd=1)
        frame_info.pack(fill="x", pady=10, ipadx=10, ipady=5)

        self.lbl_sector = tk.Label(frame_info, text="Sector: -", font=("Arial", 9, "bold"), bg="#121212", fg="#00ffcc")
        self.lbl_sector.pack(anchor="w")
        
        self.txt_resumen = tk.Message(frame_info, text="Haz clic en una acción o criptomoneda en el menú lateral para ver su información comercial.", 
                                      font=("Arial", 10), bg="#121212", fg="white", width=450, justify="left")
        self.txt_resumen.pack(anchor="w", pady=5)

        # -- D. Panel de Operación (Comprar) --
        frame_comprar = tk.Frame(self.frame_detalles, bg="#1e1e1e", padx=15, pady=10)
        frame_comprar.pack(fill="x", side="bottom")

        tk.Label(frame_comprar, text="Invertir cantidad (€):", font=("Arial", 11), bg="#1e1e1e", fg="white").pack(side="left")
        self.entry_inversion = tk.Entry(frame_comprar, font=("Arial", 12), width=15, bg="#121212", fg="white", bd=0, insertbackground="white")
        self.entry_inversion.pack(side="left", padx=10)

        tk.Button(frame_comprar, text="🛒 COMPRAR", font=("Arial", 11, "bold"), bg="#2ecc71", fg="black", bd=0, padx=20, cursor="hand2", command=self.ejecutar_compra).pack(side="right")

    def crear_boton_activo(self, parent, categoria, ticker):
        datos = self.base_datos[categoria][ticker]
        btn = tk.Button(parent, text=f"{ticker}  -  {datos['precio']}€", font=("Arial", 10, "bold"),
                        bg="#333333", fg="white", bd=0, pady=10, cursor="hand2", anchor="w", padx=15,
                        command=lambda c=categoria, t=ticker: self.seleccionar_activo(c, t))
        btn.pack(fill="x", pady=2, padx=5)

    def seleccionar_activo(self, categoria, ticker):
        """Actualiza la columna derecha cuando haces clic en una acción o cripto"""
        self.activo_seleccionado = self.base_datos[categoria][ticker]
        self.activo_seleccionado['ticker'] = ticker
        
        # Actualizar textos
        self.lbl_nombre_activo.config(text=f"{self.activo_seleccionado['nombre']} ({ticker})")
        self.lbl_precio_activo.config(text=f"{self.activo_seleccionado['precio']:,.2f} €")
        self.lbl_sector.config(text=f"Sector: {self.activo_seleccionado['sector']}")
        self.txt_resumen.config(text=self.activo_seleccionado['resumen'])

    def ejecutar_compra(self):
        if not self.activo_seleccionado:
            messagebox.showerror("Error", "Primero debes seleccionar un activo del explorador.")
            return
            
        cantidad = self.entry_inversion.get()
        # Aquí en el futuro programaremos la escritura en tu archivo JSON
        messagebox.showinfo("Éxito", f"Has simulado la compra de {cantidad}€ en {self.activo_seleccionado['nombre']}.")