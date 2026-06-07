import tkinter as tk
from tkinter import ttk, messagebox
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.dates as mdates
from datetime import datetime, timedelta
import random
import yfinance as yf
import os

class InvertirFrame(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg="#121212")
        self.controller = controller
        
        self.periodo_actual = "1M"

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
        self.categoria_seleccionada = None

        self.crear_interfaz()

    def crear_interfaz(self):
        # Título y botón de volver
        frame_top = tk.Frame(self, bg="#121212")
        frame_top.pack(fill="x", padx=25, pady=(15, 5))
        
        tk.Button(frame_top, text="⬅ Volver a Portafolio", font=("Arial", 10, "bold"), 
                  bg="#333333", fg="white", bd=0, padx=10, cursor="hand2",
                  command=lambda: self.controller.mostrar_frame("Acciones")).pack(side="left", padx=(0, 15))

        tk.Label(frame_top, text="🛒 MERCADO DE INVERSIONES", font=("Arial", 18, "bold"), bg="#121212", fg="white").pack(side="left")

        # --- CONTENEDOR PRINCIPAL DIVIDIDO ---
        main_container = tk.Frame(self, bg="#121212")
        main_container.pack(fill="both", expand=True, padx=25, pady=10)

        # 1. PANEL IZQUIERDO: LISTA DE MERCADO
        frame_lista = tk.LabelFrame(main_container, text=" Explorador ", font=("Arial", 11, "bold"), fg="#00ffcc", bg="#121212", bd=1)
        frame_lista.pack(side="left", fill="y", ipadx=10)

        estilo = ttk.Style()
        estilo.theme_use('clam')
        estilo.configure("TNotebook", background="#121212", borderwidth=0)
        estilo.configure("TNotebook.Tab", background="#333333", foreground="white", padding=[10, 5])
        estilo.map("TNotebook.Tab", background=[("selected", "#482673")])

        self.notebook = ttk.Notebook(frame_lista, style="TNotebook")
        self.notebook.pack(fill="both", expand=True, padx=5, pady=5)

        tab_acciones = tk.Frame(self.notebook, bg="#1e1e1e")
        self.notebook.add(tab_acciones, text="🏢 Acciones")
        for ticker in self.base_datos["Acciones"]:
            self.crear_boton_activo(tab_acciones, "Acciones", ticker)

        tab_cripto = tk.Frame(self.notebook, bg="#1e1e1e")
        self.notebook.add(tab_cripto, text="🪙 Cripto")
        for ticker in self.base_datos["Cripto"]:
            self.crear_boton_activo(tab_cripto, "Cripto", ticker)

        # 2. PANEL DERECHO: DETALLES Y COMPRA
        self.frame_detalles = tk.Frame(main_container, bg="#121212")
        self.frame_detalles.pack(side="right", fill="both", expand=True, padx=(20, 0))

        # -- A. Cabecera del Activo --
        self.lbl_nombre_activo = tk.Label(self.frame_detalles, text="Selecciona un activo...", font=("Arial", 22, "bold"), bg="#121212", fg="white")
        self.lbl_nombre_activo.pack(anchor="w")

        self.lbl_precio_activo = tk.Label(self.frame_detalles, text="0.00 €", font=("Arial", 16, "bold"), bg="#121212", fg="#2ecc71")
        self.lbl_precio_activo.pack(anchor="w", pady=(0, 10))

        # -- B. Gráfico Interactivo Real --
        self.frame_grafico = tk.Frame(self.frame_detalles, bg="#1e1e1e")
        self.frame_grafico.pack(fill="both", expand=True, pady=5)

        self.figura = Figure(figsize=(6, 3), dpi=100, facecolor="#1e1e1e")
        self.ax = self.figura.add_subplot(111)
        self.ax.set_facecolor("#1e1e1e")
        self.ax.tick_params(colors="white", labelsize=9)
        for spine in self.ax.spines.values():
            spine.set_color("#333333")

        self.canvas = FigureCanvasTkAgg(self.figura, master=self.frame_grafico)
        self.canvas.get_tk_widget().pack(fill="both", expand=True, padx=5, pady=5)

        # Botones de Tiempo
        frame_tiempos = tk.Frame(self.frame_detalles, bg="#121212")
        frame_tiempos.pack(anchor="w", pady=5)
        
        self.botones_tiempo = {}
        for t in ["1D", "1S", "1M", "1A", "MAX"]:
            btn = tk.Button(frame_tiempos, text=t, font=("Arial", 9, "bold"), bg="#333333", fg="white", bd=0, width=5, cursor="hand2",
                            command=lambda valor=t: self.cambiar_periodo(valor))
            btn.pack(side="left", padx=2)
            self.botones_tiempo[t] = btn

        # -- C. Panel de Información (Resumen) --
        frame_info = tk.LabelFrame(self.frame_detalles, text=" Sobre este activo ", font=("Arial", 10, "bold"), fg="#b3b3b3", bg="#121212", bd=1)
        frame_info.pack(fill="x", pady=10, ipadx=10, ipady=5)

        self.lbl_sector = tk.Label(frame_info, text="Sector: -", font=("Arial", 9, "bold"), bg="#121212", fg="#00ffcc")
        self.lbl_sector.pack(anchor="w")
        
        self.txt_resumen = tk.Message(frame_info, text="Haz clic en una acción o criptomoneda en el menú lateral para ver su gráfica y resumen.", 
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
        self.categoria_seleccionada = categoria
        
        # Actualizar textos
        self.lbl_nombre_activo.config(text=f"{self.activo_seleccionado['nombre']} ({ticker})")
        self.lbl_precio_activo.config(text=f"{self.activo_seleccionado['precio']:,.2f} €")
        self.lbl_sector.config(text=f"Sector: {self.activo_seleccionado['sector']}")
        self.txt_resumen.config(text=self.activo_seleccionado['resumen'])
        
        # Generar gráfica inicial (Por defecto 1 Mes)
        self.cambiar_periodo("1M")

    def cambiar_periodo(self, periodo):
        """Cambia el marco de tiempo y regenera la gráfica"""
        if not self.activo_seleccionado:
            messagebox.showwarning("Aviso", "Por favor, selecciona un activo de la lista primero.")
            return

        self.periodo_actual = periodo
        
        # Iluminar el botón seleccionado
        color_activo = self.controller.color_btn if hasattr(self.controller, 'color_btn') else "#482673"
        for p, btn in self.botones_tiempo.items():
            if p == periodo:
                btn.config(bg=color_activo, fg="white")
            else:
                btn.config(bg="#333333", fg="white")
                
        self.generar_grafico_activo()

    def generar_grafico_activo(self):
        """Genera el gráfico del activo actual con datos REALES, MÁXIMA SUAVIDAD y SIN HUECOS"""
        if not self.activo_seleccionado:
            return

        ticker = self.activo_seleccionado['ticker']
        
        # 🌐 Adaptar tickers para Yahoo Finance
        ticker_real = f"{ticker}-EUR" if self.categoria_seleccionada == "Cripto" else ticker

        # 📅 Configuración de Alta Resolución
        mapeo_tiempo = {
            "1D": {"periodo": "1d", "intervalo": "2m"},   
            "1S": {"periodo": "5d", "intervalo": "5m"},   
            "1M": {"periodo": "1mo", "intervalo": "30m"}, 
            "1A": {"periodo": "1y", "intervalo": "1h"},   
            "MAX": {"periodo": "max", "intervalo": "1d"}  
        }
        
        config = mapeo_tiempo.get(self.periodo_actual, {"periodo": "1mo", "intervalo": "1d"})

        try:
            # 📥 Descargar datos reales
            activo_api = yf.Ticker(ticker_real)
            datos = activo_api.history(period=config["periodo"], interval=config["intervalo"])

            if datos.empty:
                messagebox.showerror("Error", f"No se encontraron datos en tiempo real para {ticker_real}")
                return

            datos.index = datos.index.tz_localize(None)
            fechas = datos.index
            valores = datos['Close'].values

            # 💰 ACTUALIZACIÓN EN VIVO del precio
            precio_real_actual = float(valores[-1])
            self.lbl_precio_activo.config(text=f"{precio_real_actual:,.2f} €")

        except Exception as e:
            messagebox.showerror("Error", f"Error de conexión con el mercado: {e}")
            return

        # 🎨 Dibujar gráfico (Táctica limpia sin huecos ni solapamientos)
        self.ax.clear()
        self.ax.grid(True, linestyle='--', alpha=0.1, color="white")
        
        color_linea = "#2ecc71" if valores[-1] >= valores[0] else "#ff4c4c"
        
        # 1. Graficamos usando Índices (0, 1, 2...) para eliminar líneas rectas de fines de semana
        indices = list(range(len(valores)))
        self.ax.plot(indices, valores, color=color_linea, linewidth=2)
        self.ax.fill_between(indices, valores, min(valores)*0.99, color=color_linea, alpha=0.1)

        # 2. DISTRIBUCIÓN GEOMÉTRICA PERFECTA (4 etiquetas fijas para evitar solapamientos)
        num_ticks = 4
        indices_ticks = [int(i * (len(valores) - 1) / (num_ticks - 1)) for i in range(num_ticks)]

        # 3. Traducimos esos puntos clave a sus fechas reales formateadas
        if self.periodo_actual == "1D":
            etiquetas_ticks = [fechas[idx].strftime('%H:%M') for idx in indices_ticks]
        elif self.periodo_actual in ["1S", "1M"]:
            etiquetas_ticks = [fechas[idx].strftime('%d %b') for idx in indices_ticks]
        else:
            etiquetas_ticks = [fechas[idx].strftime('%b %Y') for idx in indices_ticks]

       # Aplicamos las posiciones y los textos al eje X
        self.ax.set_xticks(indices_ticks)
        self.ax.set_xticklabels(etiquetas_ticks)

        # --- 🖱️ NUEVO: CONFIGURACIÓN DEL CURSOR INTERACTIVO ---
        # Guardamos los datos en variables de clase para poder leerlos al mover el ratón
        self.valores_grafico = valores
        self.fechas_grafico = fechas

        # 1. Crear la línea vertical (oculta por defecto)
        self.linea_cursor = self.ax.axvline(x=0, color='white', alpha=0.4, linestyle='--', visible=False)

        # 2. Crear la cajita flotante de información (oculta por defecto)
        self.anotacion = self.ax.annotate(
            "", xy=(0,0), xytext=(15, 15),
            textcoords="offset points",
            bbox=dict(boxstyle="round,pad=0.4", fc="#2b2b2b", ec="gray", lw=1),
            color="white", visible=False, fontfamily="Arial", fontsize=9
        )

        # 3. Conectar el movimiento del ratón con nuestra nueva función
        if hasattr(self, "evento_hover"):
            self.canvas.mpl_disconnect(self.evento_hover)
        self.evento_hover = self.canvas.mpl_connect("motion_notify_event", self.hover_grafico)
        # --------------------------------------------------------

        self.figura.autofmt_xdate()
        self.canvas.draw()
    
    def hover_grafico(self, event):
        """Detecta el ratón sobre el gráfico y dibuja el precio y fecha exactos"""
        # Si no hay datos cargados, no hacemos nada
        if not hasattr(self, 'valores_grafico') or self.valores_grafico is None:
            return

        # Comprobar si el ratón está dentro de la caja del gráfico
        if event.inaxes == self.ax:
            # Capturar en qué punto "X" (índice) está el ratón
            x_idx = int(round(event.xdata))

            # Verificar que el ratón no se haya salido de los límites de los datos
            if 0 <= x_idx < len(self.valores_grafico):
                precio_hover = self.valores_grafico[x_idx]
                fecha_hover = self.fechas_grafico[x_idx]

                # 📅 Formatear la fecha para la cajita según el periodo
                if self.periodo_actual == "1D":
                    fecha_str = fecha_hover.strftime('%H:%M')
                elif self.periodo_actual in ["1S", "1M"]:
                    fecha_str = fecha_hover.strftime('%d %b - %H:%M')
                else:
                    fecha_str = fecha_hover.strftime('%d %b %Y')

                # ✏️ Actualizar texto y posición de la cajita flotante
                texto = f"{fecha_str}\n{precio_hover:,.2f} €"
                self.anotacion.set_text(texto)
                self.anotacion.xy = (x_idx, precio_hover)

                # Si el ratón está muy a la derecha, mover la caja a la izquierda para que no se corte
                if x_idx > len(self.valores_grafico) * 0.7:
                    self.anotacion.set_position((-80, 15))
                else:
                    self.anotacion.set_position((15, 15))

                # 📍 Mover la línea vertical punteada a la posición del ratón
                self.linea_cursor.set_xdata([x_idx, x_idx])

                # Hacer visibles los elementos
                self.linea_cursor.set_visible(True)
                self.anotacion.set_visible(True)

                # 💰 TRUCO ROBINHOOD: Cambiar el precio GRANDE de arriba temporalmente
                self.lbl_precio_activo.config(text=f"{precio_hover:,.2f} €")

                # Redibujar solo los elementos dinámicos (para que vaya súper fluido)
                self.canvas.draw_idle()
        else:
            # Si el ratón SALE del gráfico, esconder todo y restaurar el precio original
            if hasattr(self, 'linea_cursor') and self.linea_cursor.get_visible():
                self.linea_cursor.set_visible(False)
                self.anotacion.set_visible(False)
                
                # Restaurar el texto con el último precio de cierre real
                precio_actual_real = float(self.valores_grafico[-1])
                self.lbl_precio_activo.config(text=f"{precio_actual_real:,.2f} €")
                
                self.canvas.draw_idle()

    def calcular_saldo_ahorros(self):
        """Calcula el saldo real leyendo el archivo nativo ahorros.txt"""
        # Obtenemos la ruta del archivo del usuario logueado (.txt del perfil)
        perfil_path = self.controller.usuario_logueado
        folder = os.path.dirname(perfil_path)
        
        # El archivo de ahorros se llama igual que el usuario pero terminado en _ahorros.txt
        nombre_base = os.path.splitext(os.path.basename(perfil_path))[0]
        archivo_ahorros = os.path.join(folder, "ahorros.txt")
        
        saldo = 0.0
        if os.path.exists(archivo_ahorros):
            try:
                with open(archivo_ahorros, "r", encoding="utf-8") as f:
                    for linea in f:
                        partes = linea.strip().split(",")
                        if len(partes) == 3:
                            tipo, _, cant_str = partes
                            try:
                                cantidad = float(cant_str)
                                # 🔍 SOLUCIÓN: Ahora reconoce tanto "Ingreso" como "Depósito"
                                if tipo in ["Depósito", "Ingreso"]:
                                    saldo += cantidad
                                elif tipo == "Retiro":
                                    saldo -= cantidad
                            except ValueError:
                                continue
            except Exception as e:
                print(f"Error al leer saldo de ahorros: {e}")
        return saldo, archivo_ahorros

    def leer_portafolio_activos(self):
        """Lee únicamente los activos (acciones/criptos) acumulados"""
        perfil_path = self.controller.usuario_logueado
        folder = os.path.dirname(perfil_path)
        nombre_base = os.path.splitext(os.path.basename(perfil_path))[0]
        archivo_portafolio = os.path.join(folder, f"{nombre_base}_portafolio.txt")
        
        portafolio = {}
        if os.path.exists(archivo_portafolio):
            try:
                with open(archivo_portafolio, "r", encoding="utf-8") as f:
                    for linea in f:
                        linea = linea.strip()
                        if ":" in linea:
                            ticker, cant = linea.split(":")
                            portafolio[ticker.strip()] = float(cant.strip())
            except Exception as e:
                print(f"Error al leer portafolio: {e}")
        return portafolio, archivo_portafolio

    def guardar_portafolio_activos(self, path, portafolio):
        """Guarda el inventario de activos de forma limpia"""
        try:
            with open(path, "w", encoding="utf-8") as f:
                for ticker, cant in portafolio.items():
                    if cant > 0:
                        f.write(f"{ticker}: {cant:.6f}\n")
        except Exception as e:
            print(f"Error al guardar portafolio: {e}")

    def ejecutar_compra(self):
        """Ejecuta la compra descontando el dinero directamente de la hucha de ahorros"""
        if not self.activo_seleccionado:
            messagebox.showerror("Error", "Primero debes seleccionar un activo del explorador.")
            return
            
        if not self.controller.usuario_logueado:
            messagebox.showerror("Error", "No se ha detectado ningún usuario activo.")
            return

        cantidad_str = self.entry_inversion.get().strip()
        try:
            cantidad = float(cantidad_str)
            if cantidad <= 0:
                raise ValueError
        except ValueError:
            messagebox.showerror("Error", "Introduce una cantidad de dinero válida y mayor a 0 €.")
            return

        # 1. Calcular el saldo real acumulado en tu sistema de Ahorros
        saldo_ahorros, archivo_ahorros = self.calcular_saldo_ahorros()

        # 2. Comprobar si hay fondos suficientes en la hucha general de ahorros
        if cantidad > saldo_ahorros:
            messagebox.showerror(
                "Fondos Insuficientes", 
                f"No tienes suficiente dinero en tu hucha de ahorros.\n\n"
                f"Saldo actual en Ahorros: {saldo_ahorros:,.2f} €\n"
                f"Costo de la inversión: {cantidad:,.2f} €"
            )
            return

        # 3. Obtener el precio actual del activo
        if hasattr(self, 'valores_grafico') and self.valores_grafico is not None and len(self.valores_grafico) > 0:
            precio_actual = float(self.valores_grafico[-1])
        else:
            precio_actual = float(self.activo_seleccionado['precio'])

        # 4. Calcular fracciones adquiridas
        ticker = self.activo_seleccionado['ticker']
        acciones_adquiridas = cantidad / precio_actual
        
        # 5. Cargar portafolio existente y sumar las nuevas unidades de acciones
        portafolio, archivo_portafolio = self.leer_portafolio_activos()
        acciones_previas = portafolio.get(ticker, 0.0)
        portafolio[ticker] = acciones_previas + acciones_adquiridas

        # 6. REGISTRO UNIFICADO EN LA HUCHA DE AHORROS
        # Escribimos un movimiento de retiro nativo para que 'ahorros.py' lo registre y reste
        try:
            with open(archivo_ahorros, "a", encoding="utf-8") as f:
                f.write(f"Retiro,Inversiones ({ticker}),{cantidad:.2f}\n")
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo asentar el cobro en tus Ahorros: {e}")
            return

        # 7. Guardar las unidades de acciones actualizadas
        self.guardar_portafolio_activos(archivo_portafolio, portafolio)

        # 8. Mostrar confirmación en pantalla
        nuevo_saldo_simulado = saldo_ahorros - cantidad
        messagebox.showinfo(
            "¡Compra Realizada con Éxito!", 
            f"El importe ha sido retirado de tu hucha general de ahorros.\n\n"
            f"🏢 Activo comprado: {ticker} ({self.activo_seleccionado['nombre']})\n"
            f"🛒 Fracciones adquiridas: +{acciones_adquiridas:.6f}\n"
            f"📉 Precio de mercado: {precio_actual:,.2f} €\n"
            f"💸 Fondos retirados de Ahorros: -{cantidad:,.2f} €\n"
            f"----------------------------------------\n"
            f"💰 Nuevo Saldo en Ahorros: {nuevo_saldo_simulado:,.2f} €\n"
            f"📊 Inventario total de {ticker}: {portafolio[ticker]:.6f} unidades"
        )

        # Limpiar campo de texto
        self.entry_inversion.delete(0, tk.END)