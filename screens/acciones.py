import tkinter as tk
from tkinter import ttk, messagebox
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.dates as mdates
from datetime import datetime, timedelta
import random
import os
import yfinance as yf

class AccionesFrame(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg="#121212")
        self.controller = controller
        self.modo_porcentaje = True  # True = Muestra %, False = Muestra €
        self.periodo_actual = "1M"   # Periodo por defecto
        self.filtro_activo = "Todo"  # NUEVO: Filtro por defecto
        self._job_refresco = None    # Referencia al timer de auto-refresco

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
        """Se ejecuta al entrar a la pestaña: carga datos e inicia el auto-refresco"""
        self.cambiar_filtro("Todo")
        self.cambiar_periodo("1M")
        self.iniciar_refresco()

    def iniciar_refresco(self):
        """Programa un refresco automático cada 5 segundos"""
        self.detener_refresco()
        self._job_refresco = self.after(5000, self._ciclo_refresco)

    def detener_refresco(self):
        """Cancela el timer de refresco si estaba activo"""
        if self._job_refresco is not None:
            self.after_cancel(self._job_refresco)
            self._job_refresco = None

    def _ciclo_refresco(self):
        """Se ejecuta cada 5 segundos: actualiza la gráfica y se reprograma"""
        self.generar_datos_y_graficar()
        self._job_refresco = self.after(5000, self._ciclo_refresco)

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
        """ Genera la gráfica HISTÓRICA REAL leyendo los tickets de compra y cruzándolos con yfinance """
        
        # 1. LEER EL HISTORIAL DE COMPRAS (Viajar al pasado)
        perfil_path = self.controller.usuario_logueado
        folder = os.path.dirname(perfil_path)
        archivo_historial = os.path.join(folder, "historial_inversiones.txt")
        
        transacciones = []
        if os.path.exists(archivo_historial):
            with open(archivo_historial, "r", encoding="utf-8") as f:
                for linea in f:
                    try:
                        if "COMPRA" in linea:
                            partes = linea.split("|")
                            
                            # partes[0] = "[2026-06-09 07:17:36] COMPRA"
                            # partes[1] = " Activo: BTC"
                            # partes[2] = " Dinero usado: 100.00 €"
                            # partes[3] = " Acciones obtenidas: +0.001823"
                            # partes[4] = " Precio de mercado: 54864.81 €"
                            fecha_str = partes[0].split("]")[0].replace("[", "").strip()
                            fecha = datetime.strptime(fecha_str, "%Y-%m-%d %H:%M:%S")
                            
                            ticker = partes[1].split(":")[1].strip()
                            
                            # Leer el dinero exacto pagado desde "Dinero usado: 100.00 €"
                            dinero_usado = float(
                                partes[2].split(":")[1].strip().replace("€", "").strip()
                            )
                            
                            acciones = float(partes[3].split(":")[1].strip().replace("+", ""))
                            transacciones.append({"fecha": fecha, "ticker": ticker,
                                                  "acciones": acciones, "dinero_usado": dinero_usado})
                    except Exception as e:
                        print(f"Error leyendo línea del historial: {e}")
                        continue

        # Si el historial está vacío, mostrar gráfico plano en 0
        if not transacciones:
            self.lbl_total.config(text="0.00 €")
            self.lbl_variacion.config(text="Sin inversiones", fg="#b3b3b3")
            self.ax.clear()
            self.ax.grid(True, linestyle='--', alpha=0.1, color="white")
            self.canvas.draw()
            return

        # 2. APLICAR FILTROS DE VISTA (Acciones vs Cripto)
        criptos_conocidas = ["BTC", "ETH", "DOGE", "ADA", "SOL", "XRP"]
        if self.filtro_activo == "Acciones":
            transacciones = [t for t in transacciones if t["ticker"] not in criptos_conocidas]
        elif self.filtro_activo == "Cripto":
            transacciones = [t for t in transacciones if t["ticker"] in criptos_conocidas]

        # Si tras filtrar no hay transacciones para esa categoría
        if not transacciones: 
            self.lbl_total.config(text="0.00 €")
            self.ax.clear()
            self.ax.grid(True, linestyle='--', alpha=0.1, color="white")
            self.canvas.draw()
            return

        # Identificar qué activos únicos tenemos en la lista filtrada
        tickers_unicos = list(set([t["ticker"] for t in transacciones]))
        tickers_yf = [f"{t}-EUR" if t in criptos_conocidas else t for t in tickers_unicos]

        # 3. CONFIGURAR TIEMPO Y DESCARGAR DATOS DEL MERCADO GLOBAL
        mapeo_tiempo = {
            "1D": {"periodo": "1d", "intervalo": "2m"},
            "1S": {"periodo": "5d", "intervalo": "5m"},
            "1M": {"periodo": "1mo", "intervalo": "30m"},
            "1A": {"periodo": "1y", "intervalo": "1d"},
            "MAX": {"periodo": "max", "intervalo": "1d"}
        }
        config = mapeo_tiempo.get(self.periodo_actual, {"periodo": "1mo", "intervalo": "1d"})

        try:
            # Descargamos los precios de TODOS los activos que posee el usuario a la vez
            datos = yf.download(tickers_yf, period=config["periodo"], interval=config["intervalo"], progress=False)
            if datos.empty: return
            
            # ffill() y bfill() rellenan los huecos de los fines de semana de las acciones de forma perfecta
            precios = datos['Close'].ffill().bfill()
            
            # CORRECCIÓN DE COMPATIBILIDAD: Si es una Serie, la convertimos en DataFrame
            if hasattr(precios, 'to_frame'):
                precios = precios.to_frame(name=tickers_yf[0])

            precios.index = precios.index.tz_localize(None)
            
            # Forzar el momento actual exacto al final para que las compras de hoy entren siempre
            ahora = datetime.now()
            if ahora not in precios.index and self.periodo_actual in ["1D", "1S", "1M"]:
                precios.loc[ahora] = precios.iloc[-1].copy()
                precios = precios.sort_index()

            fechas = precios.index
            valores = []

            # 🛠️ CORRECCIÓN AQUÍ: Determinar con precisión si es un gráfico de días enteros o de horas/minutos
            es_grafico_diario = self.periodo_actual in ["1A", "MAX"]

            # 4. RECONSTRUIR EL PORTAFOLIO PASO A PASO
            for fecha_merc in fechas:
                valor_momento = 0.0
                
                for i, ticker in enumerate(tickers_unicos):
                    ticker_yf = tickers_yf[i]
                    
                    # Si es vista diaria (1A/MAX), comparamos solo fechas. Si es intradía (1D/1S/1M), comparamos hora exacta.
                    if es_grafico_diario:
                        acciones_acumuladas = sum([tr["acciones"] for tr in transacciones if tr["ticker"] == ticker and tr["fecha"].date() <= fecha_merc.date()])
                    else:
                        acciones_acumuladas = sum([tr["acciones"] for tr in transacciones if tr["ticker"] == ticker and tr["fecha"] <= fecha_merc])
                    
                    if acciones_acumuladas > 0:
                        precio_activo = float(precios[ticker_yf].loc[fecha_merc])
                        valor_momento += acciones_acumuladas * precio_activo
                
                valores.append(valor_momento)
                
        except Exception as e:
            print(f"Error descargando portafolio real: {e}")
            return

        # Guardar valores para los textos de rendimiento
        # valor_final   = valor actual del portafolio (último punto del gráfico)
        # valor_inicial = suma exacta de "Dinero usado" leída del historial
        #                 → 100.00 € si invertiste 100, sin importar el periodo del gráfico
        self.valor_final = valores[-1] if valores else 0

        # Prioridad 1: sumar el "Dinero usado" exacto guardado en el historial (céntimo perfecto)
        coste_base = sum(tr["dinero_usado"] for tr in transacciones if tr.get("dinero_usado") is not None)

        # Prioridad 2 (fallback): calcular con yfinance si por algún motivo no había ese campo
        if coste_base == 0:
            for tr in transacciones:
                ticker_yf_tr = f"{tr['ticker']}-EUR" if tr['ticker'] in criptos_conocidas else tr['ticker']
                try:
                    idx_compra = precios.index.searchsorted(tr["fecha"])
                    idx_compra = min(idx_compra, len(precios) - 1)
                    precio_en_compra = float(precios[ticker_yf_tr].iloc[idx_compra])
                    coste_base += tr["acciones"] * precio_en_compra
                except Exception:
                    pass

        # Prioridad 3 (último recurso): primer valor no-cero del gráfico
        if coste_base == 0:
            primeros_no_cero = [v for v in valores if v > 0]
            coste_base = primeros_no_cero[0] if primeros_no_cero else self.valor_final

        self.valor_inicial = coste_base

        self.lbl_total.config(text=f"{self.valor_final:,.2f} €")
        self.actualizar_textos_variacion()

        # 5. DIBUJAR GRÁFICO
        self.ax.clear()
        self.ax.grid(True, linestyle='--', alpha=0.1, color="white")
        
        # Color dinámico (Verde si ganas o te mantienes, Rojo si pierdes)
        base_comparacion = self.valor_inicial if self.valor_inicial > 0 else (self.valor_final * 0.99)
        color_linea = "#2ecc71" if self.valor_final >= base_comparacion else "#ff4c4c"
        
        indices = list(range(len(valores)))
        self.ax.plot(indices, valores, color=color_linea, linewidth=2)
        
        min_y = min(valores) if min(valores) > 0 else 0
        self.ax.fill_between(indices, valores, min_y * 0.99, color=color_linea, alpha=0.1)

        num_ticks = 4
        if len(valores) > 1:
            indices_ticks = [int(i * (len(valores) - 1) / (num_ticks - 1)) for i in range(num_ticks)]
            
            if self.periodo_actual == "1D":
                etiquetas_ticks = [fechas[idx].strftime('%H:%M') for idx in indices_ticks]
            elif self.periodo_actual in ["1S", "1M"]:
                etiquetas_ticks = [fechas[idx].strftime('%d %b') for idx in indices_ticks]
            else:
                etiquetas_ticks = [fechas[idx].strftime('%b %Y') for idx in indices_ticks]

            self.ax.set_xticks(indices_ticks)
            self.ax.set_xticklabels(etiquetas_ticks)
        else:
            self.ax.set_xticks([])

        # --- 6. CONFIGURACIÓN DEL CURSOR INTERACTIVO ---
        self.valores_grafico = valores
        self.fechas_grafico = fechas

        self.linea_cursor = self.ax.axvline(x=0, color='white', alpha=0.4, linestyle='--', visible=False)
        self.anotacion = self.ax.annotate(
            "", xy=(0,0), xytext=(15, 15),
            textcoords="offset points",
            bbox=dict(boxstyle="round,pad=0.4", fc="#2b2b2b", ec="gray", lw=1),
            color="white", visible=False, fontfamily="Arial", fontsize=9
        )

        if hasattr(self, "evento_hover"):
            self.canvas.mpl_disconnect(self.evento_hover)
        self.evento_hover = self.canvas.mpl_connect("motion_notify_event", self.hover_grafico)

        self.figura.autofmt_xdate()
        self.canvas.draw()

    def hover_grafico(self, event):
        """Maneja el ratón sobre el gráfico general del portafolio"""
        if not hasattr(self, 'valores_grafico') or not self.valores_grafico:
            return

        if event.inaxes == self.ax:
            x_idx = int(round(event.xdata))
            if 0 <= x_idx < len(self.valores_grafico):
                precio_hover = self.valores_grafico[x_idx]
                fecha_hover = self.fechas_grafico[x_idx]

                if self.periodo_actual == "1D":
                    fecha_str = fecha_hover.strftime('%H:%M')
                elif self.periodo_actual in ["1S", "1M"]:
                    fecha_str = fecha_hover.strftime('%d %b - %H:%M')
                else:
                    fecha_str = fecha_hover.strftime('%d %b %Y')

                texto = f"{fecha_str}\n{precio_hover:,.2f} €"
                self.anotacion.set_text(texto)
                self.anotacion.xy = (x_idx, precio_hover)

                # Si el ratón está muy a la derecha, mover la caja a la izquierda
                if x_idx > len(self.valores_grafico) * 0.7:
                    self.anotacion.set_position((-80, 15))
                else:
                    self.anotacion.set_position((15, 15))

                self.linea_cursor.set_xdata([x_idx, x_idx])
                self.linea_cursor.set_visible(True)
                self.anotacion.set_visible(True)

                self.lbl_total.config(text=f"{precio_hover:,.2f} €")
                self.canvas.draw_idle()
        else:
            if hasattr(self, 'linea_cursor') and self.linea_cursor.get_visible():
                self.linea_cursor.set_visible(False)
                self.anotacion.set_visible(False)
                precio_actual_real = float(self.valores_grafico[-1])
                self.lbl_total.config(text=f"{precio_actual_real:,.2f} €")
                self.canvas.draw_idle()

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
        