import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


class InvertirView(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg="#121212")
        self.controller = controller
        self.presenter = None
        
        # Variables internas para la interactividad del gráfico
        self.valores_grafico = None
        self.fechas_grafico = None
        self.linea_cursor = None
        self.anotacion = None
        self.evento_hover = None

    def set_presenter(self, presenter):
        self.presenter = presenter
        self.crear_interfaz()

    def crear_interfaz(self):
        # CABECERA GENERAL (Márgenes muy compactos)
        frame_top = tk.Frame(self, bg="#121212")
        frame_top.pack(fill="x", padx=15, pady=(6, 2))

        tk.Button(frame_top, text="⬅ Volver a Portafolio", font=("Arial", 9, "bold"),
                  bg="#333333", fg="white", bd=0, padx=8, pady=2, cursor="hand2",
                  command=lambda: self.controller.mostrar_frame("Acciones")).pack(side="left", padx=(0, 10))

        tk.Label(frame_top, text="🛒 MERCADO DE INVERSIONES", font=("Arial", 14, "bold"), bg="#121212", fg="white").pack(
            side="left")

        # Contenedor principal de la interfaz
        main_container = tk.Frame(self, bg="#121212")
        main_container.pack(fill="both", expand=True, padx=15, pady=2)

        # 1. PANEL IZQUIERDO: EXPLORADOR DE MERCADO (Ocupa todo el alto de forma limpia)
        frame_lista = tk.LabelFrame(main_container, text=" Explorador ", font=("Arial", 9, "bold"), fg="#00ffcc",
                                    bg="#121212", bd=1)
        frame_lista.pack(side="left", fill="y", ipadx=2)

        estilo = ttk.Style()
        estilo.theme_use('clam')
        estilo.configure("TNotebook", background="#121212", borderwidth=0)
        estilo.configure("TNotebook.Tab", background="#333333", foreground="white", padding=[6, 2])
        estilo.map("TNotebook.Tab", background=[("selected", "#482673")])

        self.notebook = ttk.Notebook(frame_lista, style="TNotebook")
        self.notebook.pack(fill="both", expand=True, padx=2, pady=2)

        tab_acciones = tk.Frame(self.notebook, bg="#1e1e1e")
        self.notebook.add(tab_acciones, text="🏢 Acciones")
        for ticker in self.presenter.obtener_activos_por_categoria("Acciones"):
            self.crear_boton_activo(tab_acciones, "Acciones", ticker)

        tab_cripto = tk.Frame(self.notebook, bg="#1e1e1e")
        self.notebook.add(tab_cripto, text="🪙 Cripto")
        for ticker in self.presenter.obtener_activos_por_categoria("Cripto"):
            self.crear_boton_activo(tab_cripto, "Cripto", ticker)

        # 2. PANEL DERECHO: DETALLES, GRÁFICO Y OPERACIÓN (Estructuración secuencial limpia)
        self.frame_detalles = tk.Frame(main_container, bg="#121212")
        self.frame_detalles.pack(side="right", fill="both", expand=True, padx=(15, 0))
        
        # Elemento A: Identificación del activo
        self.lbl_nombre_activo = tk.Label(self.frame_detalles, text="Selecciona un activo...",
                                          font=("Arial", 16, "bold"), bg="#121212", fg="white")
        self.lbl_nombre_activo.pack(side="top", anchor="w", pady=(0, 1))

        self.lbl_precio_activo = tk.Label(self.frame_detalles, text="0.00 €", font=("Arial", 12, "bold"), bg="#121212",
                                          fg="#2ecc71")
        self.lbl_precio_activo.pack(side="top", anchor="w", pady=(0, 2))

        # Elemento B: Selectores temporales
        frame_tiempos = tk.Frame(self.frame_detalles, bg="#121212")
        frame_tiempos.pack(side="top", anchor="w", pady=(0, 4))

        self.botones_tiempo = {}
        for t in ["1D", "1S", "1M", "1A", "MAX"]:
            btn = tk.Button(frame_tiempos, text=t, font=("Arial", 8, "bold"), bg="#333333", fg="white", bd=0, width=4,
                            cursor="hand2",
                            command=lambda valor=t: self.presenter.cambiar_periodo(valor))
            btn.pack(side="left", padx=2)
            self.botones_tiempo[t] = btn

        # Elemento C: El Gráfico (Tamaño compacto fijo e inamovible)
        self.frame_grafico = tk.Frame(self.frame_detalles, bg="#1e1e1e")
        self.frame_grafico.pack(side="top", fill="x", pady=(2, 4))

        # Fijamos la altura a 2.8 pulgadas para garantizar espacio holgado al resto de componentes
        self.figura = Figure(figsize=(5, 2.8), dpi=100, facecolor="#1e1e1e")
        self.ax = self.figura.add_subplot(111)
        self.ax.set_facecolor("#1e1e1e")
        self.ax.tick_params(colors="white", labelsize=8)
        for spine in self.ax.spines.values():
            spine.set_color("#333333")

        self.canvas = FigureCanvasTkAgg(self.figura, master=self.frame_grafico)
        self.canvas.get_tk_widget().pack(fill="x", pady=2)

        # Elemento D: CAJA DE COMPRA (Ubicada exactamente debajo del gráfico)
        frame_comprar = tk.Frame(self.frame_detalles, bg="#1e1e1e", padx=10, pady=6)
        frame_comprar.pack(side="top", fill="x", pady=(4, 4))

        tk.Label(frame_comprar, text="Invertir cantidad (€):", font=("Arial", 9, "bold"), bg="#1e1e1e", fg="white").pack(
            side="left")
        self.entry_inversion = tk.Entry(frame_comprar, font=("Arial", 10), width=12, bg="#121212", fg="white", bd=0,
                                        insertbackground="white")
        self.entry_inversion.pack(side="left", padx=8)

        tk.Button(frame_comprar, text="🛒 COMPRAR", font=("Arial", 9, "bold"), bg="#2ecc71", fg="black", bd=0, padx=14, pady=2,
                  cursor="hand2",
                  command=lambda: self.presenter.ejecutar_compra()).pack(side="right")

        # Elemento E: Cuadro informativo "Sobre este activo"
        frame_info = tk.LabelFrame(self.frame_detalles, text=" Sobre este activo ", font=("Arial", 8, "bold"),
                                   fg="#b3b3b3", bg="#121212", bd=1)
        frame_info.pack(side="top", fill="x", pady=(4, 2), ipadx=5, ipady=2)

        self.lbl_sector = tk.Label(frame_info, text="Sector: -", font=("Arial", 8, "bold"), bg="#121212", fg="#00ffcc")
        self.lbl_sector.pack(anchor="w", padx=5)

        self.txt_resumen = tk.Message(frame_info,
                                      text="Haz clic en una acción o criptomoneda en el menú lateral para ver su gráfica y resumen.",
                                      font=("Arial", 8), bg="#121212", fg="white", width=450, justify="left")
        self.txt_resumen.pack(anchor="w", pady=2, padx=5)

    def crear_boton_activo(self, parent, categoria, ticker):
        precio = self.presenter.obtener_precio_inicial(categoria, ticker)
        btn = tk.Button(parent, text=f"{ticker}  -  {precio}€", font=("Arial", 8, "bold"),
                        bg="#333333", fg="white", bd=0, pady=4, cursor="hand2", anchor="w", padx=10,
                        command=lambda c=categoria, t=ticker: self.presenter.seleccionar_activo(c, t))
        btn.pack(fill="x", pady=1, padx=2)

    def obtener_cantidad_ingresada(self):
        return self.entry_inversion.get()

    def limpiar_campo_inversion(self):
        self.entry_inversion.delete(0, tk.END)

    def actualizar_datos_visuales(self, nombre, ticker, precio_formateado, sector, resumen):
        self.lbl_nombre_activo.config(text=f"{nombre} ({ticker})")
        self.lbl_precio_activo.config(text=f"{precio_formateado} €")
        self.lbl_sector.config(text=f"Sector: {sector}")
        self.txt_resumen.config(text=resumen)

    def refrescar_precio_cabecera(self, precio_real_actual):
        self.lbl_precio_activo.config(text=f"{precio_real_actual:,.2f} €")

    def iluminar_boton_periodo(self, periodo_seleccionado):
        color_activo = self.controller.color_btn if hasattr(self.controller, 'color_btn') else "#482673"
        for p, btn in self.botones_tiempo.items():
            if p == periodo_seleccionado:
                btn.config(bg=color_activo, fg="white")
            else:
                btn.config(bg="#333333", fg="white")

    def mostrar_error(self, titulo, mensaje):
        messagebox.showerror(titulo, mensaje)

    def mostrar_advertencia(self, titulo, mensaje):
        messagebox.showwarning(titulo, mensaje)

    def mostrar_exito(self, titulo, mensaje):
        messagebox.showinfo(titulo, mensaje)

    def dibujar_grafica(self, fechas, valores, periodo_actual, color_linea):
        self.valores_grafico = valores
        self.fechas_grafico = fechas

        self.ax.clear()
        self.ax.grid(True, linestyle='--', alpha=0.1, color="white")
        
        indices = list(range(len(valores)))
        self.ax.plot(indices, valores, color=color_linea, linewidth=1.5)
        self.ax.fill_between(indices, valores, min(valores) * 0.99, color=color_linea, alpha=0.1)

        num_ticks = 4
        indices_ticks = [int(i * (len(valores) - 1) / (num_ticks - 1)) for i in range(num_ticks)]

        if periodo_actual == "1D":
            etiquetas_ticks = [fechas[idx].strftime('%H:%M') for idx in indices_ticks]
        elif periodo_actual in ["1S", "1M"]:
            etiquetas_ticks = [fechas[idx].strftime('%d %b') for idx in indices_ticks]
        else:
            etiquetas_ticks = [fechas[idx].strftime('%b %Y') for idx in indices_ticks]

        self.ax.set_xticks(indices_ticks)
        self.ax.set_xticklabels(etiquetas_ticks)

        self.linea_cursor = self.ax.axvline(x=0, color='white', alpha=0.4, linestyle='--', visible=False)
        self.anotacion = self.ax.annotate(
            "", xy=(0, 0), xytext=(10, 10), textcoords="offset points",
            bbox=dict(boxstyle="round,pad=0.3", fc="#2b2b2b", ec="gray", lw=1),
            color="white", visible=False, fontfamily="Arial", fontsize=8
        )

        if self.evento_hover is not None:
            self.canvas.mpl_disconnect(self.evento_hover)
        self.evento_hover = self.canvas.mpl_connect("motion_notify_event", self._hover_grafico)

        self.canvas.draw()

    def _hover_grafico(self, event):
        if event.inaxes == self.ax and self.valores_grafico is not None:
            x = int(round(event.xdata))
            if 0 <= x < len(self.valores_grafico):
                precio = self.valores_grafico[x]
                fecha = self.fechas_grafico[x]

                self.linea_cursor.set_xdata([x])
                self.linea_cursor.set_visible(True)

                self.anotacion.xy = (x, precio)
                texto = f"Fecha: {fecha.strftime('%d/%m/%Y %H:%M')}\nPrecio: {precio:,.2f} €"
                self.anotacion.set_text(texto)
                self.anotacion.set_visible(True)
                self.canvas.draw_idle()
                return

        if self.linea_cursor and self.linea_cursor.get_visible():
            self.linea_cursor.set_visible(False)
            self.anotacion.set_visible(False)
            self.canvas.draw_idle()