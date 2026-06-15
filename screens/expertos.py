import tkinter as tk
from tkinter import ttk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


class ExpertosFrame(tk.Frame):
    """Vista de Expertos: compras de los grandes inversores en el último trimestre.

    Solo construye widgets y pinta lo que el presentador le ordena. No realiza
    cálculos ni accede a datos (MVP estricto)."""

    def __init__(self, parent, controller):
        super().__init__(parent, bg="#121212")
        self.controller = controller
        self.presenter = None
        self.canvas = None

        # --- ENCABEZADO ---
        tk.Label(self, text="🏛️ EXPERTOS · Compras institucionales del trimestre",
                 font=("Arial", 18, "bold"), bg="#121212", fg="white").pack(anchor="w", padx=25, pady=(15, 2))
        tk.Label(self, text="Acciones que los grandes inversores (fondos, bancos y gestoras) "
                            "han aumentado en su cartera durante el último trimestre.",
                 font=("Arial", 10), bg="#121212", fg="#b3b3b3").pack(anchor="w", padx=25, pady=(0, 8))

        # Barra superior: resumen + botón de actualizar
        barra = tk.Frame(self, bg="#121212")
        barra.pack(fill="x", padx=25)
        self.lbl_total = tk.Label(barra, text="Cargando…", font=("Arial", 11, "bold"),
                                  bg="#121212", fg="#00ffcc")
        self.lbl_total.pack(side="left")
        tk.Button(barra, text="🔄 Actualizar", font=("Arial", 9, "bold"), bg="#482673",
                  fg="white", bd=0, padx=10, pady=4, cursor="hand2",
                  command=self.cargar_datos_usuario).pack(side="right")

        # --- CUERPO: gráfico (izquierda) + tabla (derecha) ---
        cuerpo = tk.Frame(self, bg="#121212")
        cuerpo.pack(fill="both", expand=True, padx=25, pady=10)

        # Columna izquierda: gráfico de barras de las mayores compras
        frame_grafico_cont = tk.LabelFrame(cuerpo, text=" Mayores compras por valor ",
                                           font=("Arial", 11, "bold"), fg="#a78bfa",
                                           bg="#121212", bd=1, padx=10, pady=10)
        frame_grafico_cont.pack(side="left", fill="both", expand=False)
        self.frame_grafico = tk.Frame(frame_grafico_cont, bg="#121212", width=430, height=320)
        self.frame_grafico.pack(fill="both", expand=True)
        self.frame_grafico.pack_propagate(False)

        # Columna derecha: tabla detallada
        frame_tabla = tk.LabelFrame(cuerpo, text=" Detalle de compras ",
                                    font=("Arial", 11, "bold"), fg="#a78bfa",
                                    bg="#121212", bd=1, padx=10, pady=10)
        frame_tabla.pack(side="right", fill="both", expand=True, padx=(15, 0))

        estilo = ttk.Style()
        estilo.configure("Expertos.Treeview", background="#1e1e1e", foreground="white",
                         fieldbackground="#1e1e1e", rowheight=26, borderwidth=0)
        estilo.configure("Expertos.Treeview.Heading", background="#2a2a2a", foreground="white",
                         relief="flat", font=("Arial", 9, "bold"))

        columnas = ("Inversor", "Activo", "Empresa", "Acciones", "Valor", "Variacion")
        self.tabla = ttk.Treeview(frame_tabla, columns=columnas, show="headings", style="Expertos.Treeview")
        for col, texto, ancho, anc in [
            ("Inversor", "Inversor", 150, "w"),
            ("Activo", "Activo", 60, "center"),
            ("Empresa", "Empresa", 150, "w"),
            ("Acciones", "Acciones", 90, "e"),
            ("Valor", "Valor", 110, "e"),
            ("Variacion", "Variación", 80, "e"),
        ]:
            self.tabla.heading(col, text=texto)
            self.tabla.column(col, width=ancho, anchor=anc)
        # Etiquetas de color para la variación positiva/negativa.
        self.tabla.tag_configure("pos", foreground="#2ecc71")
        self.tabla.tag_configure("neg", foreground="#ff4c4c")
        self.tabla.pack(fill="both", expand=True)

    # --- Enlace MVP ---
    def set_presenter(self, presenter):
        self.presenter = presenter

    def cargar_datos_usuario(self):
        if self.presenter:
            self.presenter.cargar_datos_usuario()

    # =================================================================
    # MÉTODOS DE RENDERIZADO (la Vista solo pinta lo que ordena el Presentador)
    # =================================================================
    def limpiar_tabla(self):
        for item in self.tabla.get_children():
            self.tabla.delete(item)

    def agregar_fila(self, inversor, simbolo, empresa, acciones, valor, variacion, positiva):
        tag = "pos" if positiva else "neg"
        self.tabla.insert("", "end", values=(inversor, simbolo, empresa, acciones, valor, variacion), tags=(tag,))

    def mostrar_total(self, texto):
        self.lbl_total.config(text=texto)

    def mostrar_cargando(self):
        self.lbl_total.config(text="Cargando datos de mercado…")

    def refrescar(self):
        self.update_idletasks()

    def dibujar_grafico_barras(self, etiquetas, valores):
        # Limpiamos el gráfico anterior para que no se encimen.
        if self.canvas:
            self.canvas.get_tk_widget().destroy()
            self.canvas = None

        if not valores or sum(valores) == 0:
            tk.Label(self.frame_grafico, text="Sin datos para graficar.",
                     bg="#121212", fg="grey", font=("Arial", 10)).pack(expand=True)
            return

        try:
            fig, ax = plt.subplots(figsize=(4.2, 3.1), dpi=80)
            fig.patch.set_facecolor("#121212")
            ax.set_facecolor("#121212")

            posiciones = range(len(valores))
            # Valores en millones para que las etiquetas sean legibles.
            valores_m = [v / 1_000_000 for v in valores]
            ax.barh(list(posiciones), valores_m, color="#a78bfa")
            ax.set_yticks(list(posiciones))
            ax.set_yticklabels(etiquetas, color="white", fontsize=7)
            ax.invert_yaxis()  # La mayor arriba.
            ax.set_xlabel("Valor comprado (millones €)", color="white", fontsize=8)
            ax.tick_params(colors="white", labelsize=7)
            for spine in ax.spines.values():
                spine.set_color("#333333")
            fig.tight_layout()

            self.canvas = FigureCanvasTkAgg(fig, master=self.frame_grafico)
            self.canvas.draw()
            self.canvas.get_tk_widget().pack(fill="both", expand=True)
            plt.close(fig)
        except Exception as e:
            print(f"[ERROR GRÁFICO EXPERTOS] {e}")

    # --- Diálogos (la Vista decide CÓMO se muestran) ---
    def mostrar_error(self, titulo, mensaje):
        from tkinter import messagebox
        messagebox.showerror(titulo, mensaje)
