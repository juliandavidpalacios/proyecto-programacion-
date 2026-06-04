import tkinter as tk
from tkinter import ttk, messagebox
import os
import json  # NUEVO: Importamos json para leer las futuras acciones

class AhorrosFrame(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg="#121212")
        self.controller = controller
        self.archivo_ahorros = None

        # --- TÍTULO PRINCIPAL ---
        tk.Label(self, text="💰 PANEL DE AHORROS", font=("Arial", 18, "bold"),
                 bg="#121212", fg="white").pack(anchor="w", padx=25, pady=(15, 10))

        # --- CONTENEDOR SUPERIOR: TARJETAS DE MÉTRICAS ---
        frame_tarjetas = tk.Frame(self, bg="#121212")
        frame_tarjetas.pack(fill="x", padx=25, pady=5)

        # Tarjeta 1: Total Ahorrado
        self.card_total = tk.Frame(frame_tarjetas, bg="#1e1e1e", bd=1, relief="flat", highlightbackground="#2ecc71", highlightthickness=1)
        self.card_total.pack(side="left", fill="both", expand=True, padx=(0, 10), ipady=10)
        tk.Label(self.card_total, text="Total Ahorrado", font=("Arial", 10), fg="#b3b3b3", bg="#1e1e1e").pack(pady=(8, 2))
        self.lbl_total = tk.Label(self.card_total, text="0.00 €", font=("Arial", 18, "bold"), fg="#2ecc71", bg="#1e1e1e")
        self.lbl_total.pack()

        # Tarjeta 2: Guardado este mes
        self.card_mes = tk.Frame(frame_tarjetas, bg="#1e1e1e", bd=0)
        self.card_mes.pack(side="left", fill="both", expand=True, padx=10, ipady=10)
        tk.Label(self.card_mes, text="Aportado este mes", font=("Arial", 10), fg="#b3b3b3", bg="#1e1e1e").pack(pady=(8, 2))
        self.lbl_mes = tk.Label(self.card_mes, text="0.00 €", font=("Arial", 18, "bold"), fg="#00ffcc", bg="#1e1e1e")
        self.lbl_mes.pack()

        # Tarjeta 3: MODIFICADO -> Dinero Invertido
        self.card_inversiones = tk.Frame(frame_tarjetas, bg="#1e1e1e", bd=0)
        self.card_inversiones.pack(side="left", fill="both", expand=True, padx=(10, 0), ipady=10)
        tk.Label(self.card_inversiones, text="Dinero Invertido", font=("Arial", 10), fg="#b3b3b3", bg="#1e1e1e").pack(pady=(8, 2))
        self.lbl_inversiones = tk.Label(self.card_inversiones, text="0.00 €", font=("Arial", 18, "bold"), fg="#ffcc00", bg="#1e1e1e")
        self.lbl_inversiones.pack()

        # --- CONTENEDOR INFERIOR (FORMULARIO E HISTORIAL) ---
        main_inferior = tk.Frame(self, bg="#121212")
        main_inferior.pack(fill="both", expand=True, padx=25, pady=15)

        # - COLUMNA IZQUIERDA: ACCIONES / OPERACIONES -
        frame_acciones = tk.LabelFrame(main_inferior, text=" Nueva Aportación ", font=("Arial", 11, "bold"),
                                       fg="#2ecc71", bg="#121212", bd=1, padx=15, pady=10)
        frame_acciones.pack(side="left", fill="both", expand=False)

        tk.Label(frame_acciones, text="Cantidad (€):", font=("Arial", 10), fg="#b3b3b3", bg="#121212").pack(anchor="w", pady=(5, 2))
        self.entry_cantidad = tk.Entry(frame_acciones, font=("Arial", 11), bg="#1e1e1e", fg="white", bd=0, insertbackground="white")
        self.entry_cantidad.pack(fill="x", ipady=4, pady=(0, 10))

        tk.Label(frame_acciones, text="Categoría / Hucha:", font=("Arial", 10), fg="#b3b3b3", bg="#121212").pack(anchor="w", pady=(5, 2))
        
        # Configuración estética del Combobox desplegable
        estilo_combo = ttk.Style()
        estilo_combo.theme_use('clam')
        estilo_combo.configure("TCombobox", fieldbackground="#1e1e1e", background="#1e1e1e", foreground="black")
        
        self.combo_categoria = ttk.Combobox(frame_acciones, font=("Arial", 10), state="readonly", style="TCombobox")
        self.combo_categoria["values"] = ("Fondo de Emergencia", "Vacaciones ✈️", "Coche Nuevo 🚗", "Inversiones 📈", "Otros")
        self.combo_categoria.current(0)
        self.combo_categoria.pack(fill="x", ipady=2, pady=(0, 15))

        # Botones de Acción
        btn_ingresar = tk.Button(frame_acciones, text="➕ Añadir al Ahorro", font=("Arial", 10, "bold"),
                                 bg="#2ecc71", fg="black", bd=0, pady=6, cursor="hand2", command=lambda: self.registrar_movimiento("Ingreso"))
        btn_ingresar.pack(fill="x", pady=5)

        btn_retirar = tk.Button(frame_acciones, text="➖ Retirar Fondos", font=("Arial", 10, "bold"),
                                bg="#333333", fg="#ff4444", bd=0, pady=6, cursor="hand2", command=lambda: self.registrar_movimiento("Retiro"))
        btn_retirar.pack(fill="x", pady=5)


        # - COLUMNA DERECHA: TABLA DE HISTORIAL -
        frame_historial = tk.LabelFrame(main_inferior, text=" Historial Reciente de Ahorro ", font=("Arial", 11, "bold"),
                                        fg="#2ecc71", bg="#121212", bd=1, padx=10, pady=10)
        frame_historial.pack(side="right", fill="both", expand=True, padx=(15, 0))

        # Estilo oscuro personalizado para la tabla (Treeview)
        estilo_tabla = ttk.Style()
        estilo_tabla.configure("Treeview", background="#1e1e1e", foreground="white", fieldbackground="#1e1e1e", rowheight=25, borderwidth=0)
        estilo_tabla.configure("Treeview.Heading", background="#2a2a2a", foreground="white", relief="flat", font=("Arial", 9, "bold"))
        estilo_tabla.map("Treeview", background=[('selected', '#2ecc71')], foreground=[('selected', 'black')])

        # Creación del Treeview
        self.tabla = ttk.Treeview(frame_historial, columns=("Tipo", "Categoría", "Cantidad"), show="headings", style="Treeview")
        self.tabla.heading("Tipo", text="Operación")
        self.tabla.heading("Categoría", text="Categoría / Destino")
        self.tabla.heading("Cantidad", text="Monto")
        
        self.tabla.column("Tipo", width=90, anchor="center")
        self.tabla.column("Categoría", width=160, anchor="w")
        self.tabla.column("Cantidad", width=90, anchor="e")
        self.tabla.pack(fill="both", expand=True)

    def cargar_datos_usuario(self):
        perfil_txt = self.controller.usuario_logueado
        if not perfil_txt:
            return

        carpeta_usuario = os.path.dirname(perfil_txt)
        self.archivo_ahorros = os.path.join(carpeta_usuario, "ahorros.txt")

        if not os.path.exists(self.archivo_ahorros):
            with open(self.archivo_ahorros, "w", encoding="utf-8") as f:
                pass

        self.actualizar_interfaz()

    def actualizar_interfaz(self):
        for item in self.tabla.get_children():
            self.tabla.delete(item)

        total_ahorrado = 0.0
        aportado_mes = 0.0
        total_invertido = 0.0  # Preparado para el futuro

        if not self.archivo_ahorros or not os.path.exists(self.archivo_ahorros):
            return

        try:
            with open(self.archivo_ahorros, "r", encoding="utf-8") as f:
                lineas = f.readlines()

            for linea in reversed(lineas):
                linea = linea.strip()
                if not linea: continue
                
                partes = linea.split(",")
                if len(partes) == 3:
                    tipo, cat, cant_str = partes
                    cantidad = float(cant_str)

                    signo = "+" if tipo == "Ingreso" else "-"
                    self.tabla.insert("", "end", values=(tipo, cat, f"{signo} {cantidad:.2f} €"))

                    if tipo == "Ingreso":
                        total_ahorrado += cantidad
                        aportado_mes += cantidad
                    else:
                        total_ahorrado -= cantidad

            # Actualizar métricas de ahorro
            self.lbl_total.config(text=f"{total_ahorrado:.2f} €")
            self.lbl_mes.config(text=f"{aportado_mes:.2f} €")

            # 🚀 LÓGICA DEL FUTURO: Leer archivo de acciones si ya existe
            carpeta_usuario = os.path.dirname(self.archivo_ahorros)
            archivo_acciones = os.path.join(carpeta_usuario, "acciones.json")
            
            if os.path.exists(archivo_acciones):
                with open(archivo_acciones, "r", encoding="utf-8") as f:
                    datos_acciones = json.load(f)
                    # Calculamos (cantidad * precio_compra) de cada cripto/acción
                    for ticker, info in datos_acciones.items():
                        cantidad_acciones = info.get("cantidad", 0)
                        precio_compra = info.get("precio_compra", 0)
                        total_invertido += (cantidad_acciones * precio_compra)

            # Actualizar la nueva tarjeta de inversiones
            self.lbl_inversiones.config(text=f"{total_invertido:.2f} €")

        except Exception as e:
            print(f"Error cargando el historial de ahorros/acciones: {e}")

    def registrar_movimiento(self, tipo):
        cant_texto = self.entry_cantidad.get().strip()
        categoria = self.combo_categoria.get()

        if not cant_texto:
            messagebox.showerror("Error", "Por favor, introduce una cantidad numérica.")
            return

        try:
            cantidad = float(cant_texto)
            if cantidad <= 0:
                raise ValueError

        except ValueError:
            messagebox.showerror("Error", "La cantidad debe ser un número válido y mayor que cero.")
            return

        if tipo == "Retiro":
            total_actual = float(self.lbl_total.cget("text").replace(" €", ""))
            if cantidad > total_actual:
                messagebox.showerror("Fondos Insuficientes", f"No puedes retirar {cantidad:.2f} € porque tu saldo de ahorro actual es de {total_actual:.2f} €.")
                return

        try:
            with open(self.archivo_ahorros, "a", encoding="utf-8") as f:
                f.write(f"{tipo},{categoria},{cantidad:.2f}\n")

            self.entry_cantidad.delete(0, tk.END)
            self.actualizar_interfaz()
            messagebox.showinfo("Éxito", f"¡{tipo} de {cantidad:.2f} € registrado correctamente!")

        except Exception as e:
            messagebox.showerror("Error", f"No se pudo guardar la operación: {e}")