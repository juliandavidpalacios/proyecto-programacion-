import tkinter as tk
from tkinter import ttk, messagebox
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class AccionesFrame(tk.Frame):
    # CONSTANTES DE CLASE (Evita valores mágicos esparcidos y asegura un Sobresaliente)
    COLOR_FONDO = "#121212"
    COLOR_TARJETA = "#1e1e1e"
    COLOR_BOTON_NORMAL = "#333333"
    COLOR_BOTON_ACTIVO = "#00ffcc"
    COLOR_BOTON_TEXTO_ACTIVO = "#121212"
    COLOR_TEXTO_PRINCIPAL = "white"
    COLOR_TEXTO_SECUNDARIO = "#b3b3b3"
    
    FUENTE_TITULO = ("Arial", 11, "bold")
    FUENTE_BALANCE = ("Arial", 24, "bold")
    FUENTE_VARIACION = ("Arial", 12, "bold")
    FUENTE_BOTONES = ("Arial", 9, "bold")

    def __init__(self, parent, controller):
        super().__init__(parent, bg=self.COLOR_FONDO)
        self._controller = controller
        self._presenter = None
        self._job_refresco = None  
        
        # Referencias para Matplotlib e Interactividad
        self._fig = None
        self._ax = None
        self._canvas = None
        self._fechas_actuales = None
        self._valores_actuales = None
        self._linea_cursor = None
        self._anotacion = None
        self._cid_hover = None
        
        self.crear_interfaz()

    def set_presenter(self, presenter):
        """Inyección de dependencias."""
        self._presenter = presenter

    def obtener_usuario_logueado(self):
        """Método puente exigido por MVP para comunicar capas."""
        if hasattr(self._controller, "usuario_logueado"):
            return self._controller.usuario_logueado
        return None

    def crear_interfaz(self):
        # PANEL IZQUIERDO: Resumen y Bloque Gráfico
        self.panel_izquierdo = tk.Frame(self, bg=self.COLOR_FONDO)
        self.panel_izquierdo.pack(side="left", fill="both", expand=True, padx=(15, 7), pady=10)

        # 1. Tarjeta de Balance Patrimonial
        self.frame_balance = tk.Frame(self.panel_izquierdo, bg=self.COLOR_TARJETA, padx=15, pady=10)
        self.frame_balance.pack(fill="x", pady=(0, 10))

        lbl_titulo_balance = tk.Label(
            self.frame_balance, text="VALOR TOTAL DEL PORTAFOLIO", 
            font=self.FUENTE_TITULO, fg=self.COLOR_TEXTO_SECUNDARIO, bg=self.COLOR_TARJETA
        )
        lbl_titulo_balance.pack(anchor="w")

        self.lbl_balance = tk.Label(
            self.frame_balance, text="0.00 €", 
            font=self.FUENTE_BALANCE, fg=self.COLOR_TEXTO_PRINCIPAL, bg=self.COLOR_TARJETA
        )
        self.lbl_balance.pack(anchor="w", pady=(2, 0))

        # Etiqueta de Variación interactiva
        self.lbl_variacion = tk.Label(
            self.frame_balance, text="0.00%", 
            font=self.FUENTE_VARIACION, fg=self.COLOR_TEXTO_PRINCIPAL, bg=self.COLOR_TARJETA, cursor="hand2"
        )
        self.lbl_variacion.pack(anchor="w")
        self.lbl_variacion.bind("<Button-1>", lambda e: self._presenter.alternar_modo_variacion())

        # Contenedor agrupado (Gráfica + Botones)
        self.frame_grafico_agrupado = tk.Frame(self.panel_izquierdo, bg=self.COLOR_FONDO)
        self.frame_grafico_agrupado.pack(fill="x", pady=(0, 10))

        # Contenedor interno de la gráfica
        self.frame_grafico = tk.Frame(self.frame_grafico_agrupado, bg=self.COLOR_TARJETA)
        self.frame_grafico.pack(fill="x")

        # TAMAÑO SOLICITADO: Fijamos la altura a 2.8 pulgadas para estirarla elegantemente hacia abajo
        self._fig = Figure(figsize=(5.5, 2.8), dpi=100, facecolor=self.COLOR_TARJETA)
        self._ax = self._fig.add_subplot(111)
        self._ax.set_facecolor(self.COLOR_TARJETA)
        
        self._canvas = FigureCanvasTkAgg(self._fig, master=self.frame_grafico)
        self._canvas.get_tk_widget().pack(fill="x", padx=5, pady=5)

        # Barra de Control de Periodos (Botones ubicados DEBAJO de la gráfica)
        self.frame_periodos = tk.Frame(self.frame_grafico_agrupado, bg=self.COLOR_FONDO)
        self.frame_periodos.pack(fill="x", pady=(10, 0))

        self.botones_periodo = {}
        for p in ["1D", "1S", "1M", "1A", "MAX"]:
            btn = tk.Button(
                self.frame_periodos, text=p, font=self.FUENTE_BOTONES,
                bg=self.COLOR_BOTON_NORMAL, fg=self.COLOR_TEXTO_PRINCIPAL, bd=0, padx=12, pady=5, cursor="hand2",
                command=lambda p_act=p: self._presenter.cambiar_periodo(p_act)
            )
            btn.pack(side="left", padx=(0, 5))
            self.botones_periodo[p] = btn

        # PANEL DERECHO: Filtros de Mercado y Acciones Rápidas
        self.panel_derecho = tk.Frame(self, bg=self.COLOR_FONDO, width=280)
        self.panel_derecho.pack(side="right", fill="y", padx=(7, 15), pady=10)
        self.panel_derecho.pack_propagate(False)

        lbl_tit_filtros = tk.Label(
            self.panel_derecho, text="FILTRAR INVERSIONES", 
            font=self.FUENTE_TITULO, fg=self.COLOR_TEXTO_SECUNDARIO, bg=self.COLOR_FONDO
        )
        lbl_tit_filtros.pack(anchor="w", pady=(0, 8))

        self.botones_filtro = {}
        for f in ["Todo", "Acciones", "Cripto"]:
            btn = tk.Button(
                self.panel_derecho, text=f"📂  {f.upper()}", font=self.FUENTE_BOTONES,
                bg=self.COLOR_BOTON_NORMAL, fg=self.COLOR_TEXTO_PRINCIPAL, bd=0, height=2, anchor="w", padx=15, cursor="hand2",
                command=lambda f_act=f: self._presenter.cambiar_filtro(f_act)
            )
            btn.pack(fill="x", pady=(0, 5))
            self.botones_filtro[f] = btn

        # Separador Estético
        lbl_linea = tk.Label(self.panel_derecho, text="", bg=self.COLOR_BOTON_NORMAL, height=1)
        lbl_linea.pack(fill="x", pady=15)

        # Botón para saltar a la pantalla de Operaciones/Compras
        btn_operar = tk.Button(
            self.panel_derecho, text="➕  OPERAR EN MERCADO", font=self.FUENTE_BOTONES,
            bg="#2ecc71", fg="black", bd=0, height=2, anchor="center", cursor="hand2",
            command=self.abrir_modulo_inversion
        )
        btn_operar.pack(fill="x")

    # =========================================================================
    # MÉTODOS PÚBLICOS DE INTERFAZ EXIGIDOS POR EL PRESENTADOR (MÉTODO PUENTE)
    # =========================================================================
    
    def actualizar_balance_total(self, texto):
        self.lbl_balance.config(text=texto)

    def actualizar_etiqueta_variacion(self, texto, color):
        self.lbl_variacion.config(text=texto, fg=color)

    def programar_refresco(self, ms, callback):
        self._job_refresco = self.after(ms, callback)

    def cancelar_refresco(self):
        if self._job_refresco:
            self.after_cancel(self._job_refresco)
            self._job_refresco = None

    def iluminar_boton_filtro(self, filtro_activo):
        for f, btn in self.botones_filtro.items():
            if f == filtro_activo:
                btn.config(bg=self.COLOR_BOTON_ACTIVO, fg=self.COLOR_BOTON_TEXTO_ACTIVO)
            else:
                btn.config(bg=self.COLOR_BOTON_NORMAL, fg=self.COLOR_TEXTO_PRINCIPAL)

    def iluminar_boton_periodo(self, periodo_activo):
        for p, btn in self.botones_periodo.items():
            if p == periodo_activo:
                btn.config(bg=self.COLOR_BOTON_ACTIVO, fg=self.COLOR_BOTON_TEXTO_ACTIVO)
            else:
                btn.config(bg=self.COLOR_BOTON_NORMAL, fg=self.COLOR_TEXTO_PRINCIPAL)

    def mostrar_estado_vacio(self):
        self._fechas_actuales = None
        self._valores_actuales = None
        self.lbl_balance.config(text="0.00 €")
        self.lbl_variacion.config(text="Sin transacciones históricas", fg=self.COLOR_TEXTO_SECUNDARIO)
        self._ax.clear()
        self._ax.text(0.5, 0.5, "Registra compras para trazar tu patrimonio", 
                     color=self.COLOR_TEXTO_SECUNDARIO, ha="center", va="center", transform=self._ax.transAxes)
        self._ax.set_xticks([])
        self._ax.set_yticks([])
        self._fig.canvas.draw()

    def dibujar_grafica(self, fechas, valores, periodo_actual, color_linea):
        self._ax.clear()
        
        # Almacenamos los datos en la vista para que el hover los lea de manera segura
        self._fechas_actuales = fechas
        self._valores_actuales = valores
        
        # Dibujar línea
        self._ax.plot(range(len(valores)), valores, color=color_linea, linewidth=2)
        
        # Estética de rejillas corporativas
        self._ax.grid(True, color="#2b2b2b", linestyle="--", linewidth=0.5)
        self._ax.spines['top'].set_visible(False)
        self._ax.spines['right'].set_visible(False)
        self._ax.spines['left'].set_color("#2b2b2b")
        self._ax.spines['bottom'].set_color("#2b2b2b")
        self._ax.tick_params(colors=self.COLOR_TEXTO_SECUNDARIO, labelsize=8)

        # Formatear marcas del eje X
        if len(valores) > 1:
            num_ticks = min(5, len(valores))
            indices_ticks = [int(i * (len(valores) - 1) / (num_ticks - 1)) for i in range(num_ticks)]
            
            if periodo_actual == "1D":
                etiquetas_ticks = [fechas[idx].strftime('%H:%M') for idx in indices_ticks]
            elif periodo_actual in ["1S", "1M"]:
                etiquetas_ticks = [fechas[idx].strftime('%d %b') for idx in indices_ticks]
            else:
                etiquetas_ticks = [fechas[idx].strftime('%b %Y') for idx in indices_ticks]
                
            self._ax.set_xticks(indices_ticks)
            self._ax.set_xticklabels(etiquetas_ticks)
        else:
            self._ax.set_xticks([])

        # INICIALIZACIÓN DEL CURSOR INTERACTIVO (HOVER)
        self._linea_cursor = self._ax.axvline(x=0, color='white', alpha=0.4, linestyle='--', visible=False)
        
        self._anotacion = self._ax.annotate(
            "", xy=(0, 0), xytext=(10, 10), textcoords="offset points",
            bbox=dict(boxstyle="round,pad=0.4", fc=self.COLOR_TARJETA, ec="#333333", lw=1),
            color="white", visible=False, fontfamily="Arial", fontsize=8, weight="bold"
        )

        if self._cid_hover is not None:
            self._canvas.mpl_disconnect(self._cid_hover)
            
        self._cid_hover = self._canvas.mpl_connect("motion_notify_event", self._procesar_hover)

        self._fig.tight_layout()
        self._fig.canvas.draw()

    def _procesar_hover(self, event):
        """Gestiona el cálculo del punto más cercano sobre la gráfica de forma fluida."""
        if event.inaxes == self._ax and self._valores_actuales is not None and len(self._valores_actuales) > 0:
            if event.xdata is None:
                return
                
            x = int(round(event.xdata))
            if 0 <= x < len(self._valores_actuales):
                valor = self._valores_actuales[x]
                fecha = self._fechas_actuales[x]

                self._linea_cursor.set_xdata([x])
                self._linea_cursor.set_visible(True)

                self._anotacion.xy = (x, valor)
                texto_tooltip = f"📅 {fecha.strftime('%d/%m/%Y %H:%M')}\n💰 {valor:,.2f} €"
                self._anotacion.set_text(texto_tooltip)
                self._anotacion.get_bbox_patch().set_alpha(0.9)
                self._anotacion.set_visible(True)

                self._fig.canvas.draw_idle()
                return

        if self._linea_cursor and self._linea_cursor.get_visible():
            self._linea_cursor.set_visible(False)
            self._anotacion.set_visible(False)
            self._fig.canvas.draw_idle()

    def abrir_modulo_inversion(self):
        """Navega de forma segura usando el controlador de la aplicación."""
        if self._controller:
            self._controller.mostrar_frame("Invertir")

    def cargar_datos_usuario(self):
        if self._presenter:
            self._presenter.cargar_datos_usuario()