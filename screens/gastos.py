import tkinter as tk
from tkinter import ttk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class GastosFrame(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg="#121212")
        self.controller = controller
        self.presenter = None
        self.canvas = None

        # --- ENCABEZADO ---
        tk.Label(self, text="📉 CONTROL DE GASTOS E INFORMES", font=("Arial", 18, "bold"),
                 bg="#121212", fg="white").pack(anchor="w", padx=25, pady=(15, 10))

        # --- TARJETAS DE MÉTRICAS (INFORME RÁPIDO) ---
        frame_tarjetas = tk.Frame(self, bg="#121212")
        frame_tarjetas.pack(fill="x", padx=25, pady=5)

        # Tarjeta 1: Fijos
        self.card_fijos = tk.Frame(frame_tarjetas, bg="#1e1e1e", bd=1, relief="flat", highlightbackground="#ff4444", highlightthickness=1)
        self.card_fijos.pack(side="left", fill="both", expand=True, padx=(0, 5), ipady=5)
        tk.Label(self.card_fijos, text="Gastos Fijos", font=("Arial", 9), fg="#b3b3b3", bg="#1e1e1e").pack(pady=2)
        self.lbl_fijos = tk.Label(self.card_fijos, text="0.00 €", font=("Arial", 14, "bold"), fg="#ff4444", bg="#1e1e1e")
        self.lbl_fijos.pack()

        # Tarjeta 2: Variables
        self.card_var = tk.Frame(frame_tarjetas, bg="#1e1e1e", bd=0)
        self.card_var.pack(side="left", fill="both", expand=True, padx=5, ipady=5)
        tk.Label(self.card_var, text="Gastos Variables", font=("Arial", 9), fg="#b3b3b3", bg="#1e1e1e").pack(pady=2)
        self.lbl_variables = tk.Label(self.card_var, text="0.00 €", font=("Arial", 14, "bold"), fg="#ffcc00", bg="#1e1e1e")
        self.lbl_variables.pack()

        # Tarjeta 3: Filtro Hogar
        self.card_hogar = tk.Frame(frame_tarjetas, bg="#1e1e1e", bd=0)
        self.card_hogar.pack(side="left", fill="both", expand=True, padx=5, ipady=5)
        tk.Label(self.card_hogar, text="Total Hogar 🏠", font=("Arial", 9), fg="#b3b3b3", bg="#1e1e1e").pack(pady=2)
        self.lbl_hogar = tk.Label(self.card_hogar, text="0.00 €", font=("Arial", 14, "bold"), fg="#00ffcc", bg="#1e1e1e")
        self.lbl_hogar.pack()

        # Tarjeta 4: Filtro Coche
        self.card_coche = tk.Frame(frame_tarjetas, bg="#1e1e1e", bd=0)
        self.card_coche.pack(side="left", fill="both", expand=True, padx=(5, 0), ipady=5)
        tk.Label(self.card_coche, text="Total Coche 🚗", font=("Arial", 9), fg="#b3b3b3", bg="#1e1e1e").pack(pady=2)
        self.lbl_coche = tk.Label(self.card_coche, text="0.00 €", font=("Arial", 14, "bold"), fg="#3498db", bg="#1e1e1e")
        self.lbl_coche.pack()

        # --- CUERPO INFERIOR DISPUESTO EN DOS COLUMNAS ---
        cuerpo = tk.Frame(self, bg="#121212")
        cuerpo.pack(fill="both", expand=True, padx=25, pady=10)

        # Columna Izquierda: Formulario Dinámico
        form_frame = tk.LabelFrame(cuerpo, text=" Registrar Gasto ", font=("Arial", 11, "bold"),
                                   fg="#ff4444", bg="#121212", bd=1, padx=15, pady=10, width=280)
        form_frame.pack(side="left", fill="both", expand=False)

        tk.Label(form_frame, text="Categoría Principal:", font=("Arial", 10), fg="#b3b3b3", bg="#121212").pack(anchor="w", pady=(5,2))
        self.combo_cat = ttk.Combobox(form_frame, font=("Arial", 10), state="readonly")
        self.combo_cat["values"] = ("Gastos Fijos 📌", "Gastos Variables 💸", "Gastos del Hogar 🏠", "Gastos del Coche 🚗")
        self.combo_cat.current(0)
        self.combo_cat.pack(fill="x", pady=(0, 10))
        self.combo_cat.bind("<<ComboboxSelected>>", self.actualizar_subcategorias_combobox)

        tk.Label(form_frame, text="Subcategoría / Concepto:", font=("Arial", 10), fg="#b3b3b3", bg="#121212").pack(anchor="w", pady=(5,2))
        self.combo_sub = ttk.Combobox(form_frame, font=("Arial", 10), state="readonly")
        self.combo_sub.pack(fill="x", pady=(0, 10))

        tk.Label(form_frame, text="Cantidad (€):", font=("Arial", 10), fg="#b3b3b3", bg="#121212").pack(anchor="w", pady=(5,2))
        self.entry_monto = tk.Entry(form_frame, font=("Arial", 11), bg="#1e1e1e", fg="white", bd=0, insertbackground="white")
        self.entry_monto.pack(fill="x", ipady=4, pady=(0, 15))

        btn_gastar = tk.Button(form_frame, text="📉 Aplicar y Restar de Cuenta", font=("Arial", 10, "bold"),
                               bg="#ff4444", fg="white", bd=0, pady=8, cursor="hand2", command=self.enviar_datos_gasto)
        btn_gastar.pack(fill="x")

        # Etiquetas de saldo disponible
        tk.Label(form_frame, text="Saldo disponible en Cuenta:", font=("Arial", 9), fg="#b3b3b3", bg="#121212").pack(
            pady=(15, 2))
        self.lbl_saldo_disponible = tk.Label(form_frame, text="0.00 €", font=("Arial", 14, "bold"), fg="#2ecc71",
                                             bg="#121212")
        self.lbl_saldo_disponible.pack()

        self.frame_grafico = tk.Frame(form_frame, bg="#121212", height=250)
        self.frame_grafico.pack(fill="both", expand=True, pady=10)

        # Columna Derecha: Informe / Historial Detallado
        historial_frame = tk.LabelFrame(cuerpo, text=" Desglose de Gastos Guardados ", font=("Arial", 11, "bold"), fg="#ff4444", bg="#121212", bd=1, padx=10, pady=10)
        historial_frame.pack(side="right", fill="both", expand=True, padx=(15, 0))

        # Tabla Estilizada modo oscuro
        self.tabla = ttk.Treeview(historial_frame, columns=("Tipo", "Categoria", "Subcategoria", "Monto"), show="headings", style="Treeview")
        self.tabla.heading("Tipo", text="Macro")
        self.tabla.heading("Categoria", text="Categoría")
        self.tabla.heading("Subcategoria", text="Subcategoría")
        self.tabla.heading("Monto", text="Importe")

        self.tabla.column("Tipo", width=70, anchor="center")
        self.tabla.column("Categoria", width=130, anchor="w")
        self.tabla.column("Subcategoria", width=160, anchor="w")
        self.tabla.column("Monto", width=80, anchor="e")
        self.tabla.pack(fill="both", expand=True)

    def set_presenter(self, presenter):
        self.presenter = presenter
        # Forzar carga inicial de subcategorías al enlazar
        self.actualizar_subcategorias_combobox()

    def actualizar_subcategorias_combobox(self, event=None):
        if self.presenter:
            cat_seleccionada = self.combo_cat.get()
            subcategorias = self.presenter.obtener_subcategorias(cat_seleccionada)
            self.combo_sub["values"] = subcategorias
            if subcategorias:
                self.combo_sub.current(0)

    def enviar_datos_gasto(self):
        if self.presenter:
            self.presenter.ejecutar_gasto(
                self.combo_cat.get(),
                self.combo_sub.get(),
                self.entry_monto.get()
            )

    def limpiar_formulario(self):
        self.entry_monto.delete(0, tk.END)

    def actualizar_interfaz_informe(self, totales, historial):
        # Actualizar Tarjetas Superiores
        self.lbl_fijos.config(text=f"{totales['Fijos']:.2f} €")
        self.lbl_variables.config(text=f"{totales['Variables']:.2f} €")
        self.lbl_hogar.config(text=f"{totales['Hogar']:.2f} €")
        self.lbl_coche.config(text=f"{totales['Coche']:.2f} €")

        # Limpiar y rellenar tabla analítica
        for item in self.tabla.get_children():
            self.tabla.delete(item)
        for fila in historial:
            self.tabla.insert("", tk.END, values=fila)

    def cargar_datos_usuario(self):
        if self.presenter:
            self.presenter.inicializar_sesion()

    def dibujar_grafico_pastel(self, fijos, variables, ahorros):
        """Genera un diagrama de pastel seguro con Matplotlib incrustado en Tkinter"""
        # Limpiar gráfico anterior si existe para que no se encimen
        if self.canvas:
            self.canvas.get_tk_widget().destroy()

        # 🛡️ ESCUDO ANTI-NEGATIVOS: Matplotlib da ValueError si algún valor es menor a 0
        fijos = max(0.0, fijos)
        variables = max(0.0, variables)
        ahorros = max(0.0, ahorros)

        # Datos y configuración visual
        labels = ['Fijos', 'Variables', 'Ahorro/Inv']
        valores = [fijos, variables, ahorros]
        colores = ['#ff4444', '#3498db', '#2ecc71']  # Rojo, Azul, Verde

        # Si tras la limpieza todos los valores quedan en 0, mostramos aviso en vez de romper la app
        if sum(valores) == 0:
            # Creamos un contenedor temporal de texto informativo
            lbl_aviso = tk.Label(self.frame_grafico, text="Sin fondos o balance en negativo\npara graficar.",
                                 bg="#121212", fg="grey", font=("Arial", 10))
            lbl_aviso.pack(expand=True)
            return

        try:
            # Crear la figura de Matplotlib con fondo oscuro estilizado
            fig, ax = plt.subplots(figsize=(3, 3), dpi=80)
            fig.patch.set_facecolor('#121212')  # Fondo del frame general

            # Dibujar el pastel de forma segura
            wedges, texts, autotexts = ax.pie(
                valores,
                labels=labels,
                autopct='%1.1f%%',
                colors=colores,
                textprops={'color': "w", 'fontsize': 8},
                startangle=140
            )

            ax.set_title("Distribución de Capital", color="white", fontsize=10)

            # Incrustar el canvas de Matplotlib dentro del widget de Tkinter
            self.canvas = FigureCanvasTkAgg(fig, master=self.frame_grafico)
            self.canvas.draw()
            self.canvas.get_tk_widget().pack(fill="both", expand=True)

            # Cerrar la figura explícitamente para liberar memoria RAM
            plt.close(fig)

        except Exception as e:
            print(f"[ERROR GRÁFICO] No se pudo renderizar Matplotlib: {e}")