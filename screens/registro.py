import tkinter as tk

class RegistroFrame(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg="#121212")
        self.controller = controller

        # Contenedor principal centrado
        container = tk.Frame(self, bg="#121212")
        container.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

        tk.Label(container, text="🏦 Apertura de Cuenta Nueva", font=("Arial", 20, "bold"), 
                 fg="white", bg="#121212").grid(row=0, column=0, columnspan=2, pady=(0, 20))

        # --- COLUMNA 1 (Información Personal) ---
        self.crear_campo(container, "Nombre Completo:", 1, 0)
        self.entry_nombre = self.crear_entry(container, 2, 0)

        self.crear_campo(container, "DNI / NIE / Pasaporte:", 3, 0)
        self.entry_dni = self.crear_entry(container, 4, 0)

        self.crear_campo(container, "Fecha de Nacimiento (DD/MM/AAAA):", 5, 0)
        self.entry_fecha = self.crear_entry(container, 6, 0)

        # --- COLUMNA 2 (Contacto y Seguridad) ---
        self.crear_campo(container, "Correo Electrónico:", 1, 1)
        self.entry_email = self.crear_entry(container, 2, 1)

        self.crear_campo(container, "Teléfono de contacto:", 3, 1)
        self.entry_tel = self.crear_entry(container, 4, 1)

        self.crear_campo(container, "Definir Contraseña:", 5, 1)
        self.entry_pass = self.crear_entry(container, 6, 1, show="*")

        # --- BOTONES ---
        btn_frame = tk.Frame(container, bg="#121212")
        btn_frame.grid(row=7, column=0, columnspan=2, pady=30)

        tk.Button(btn_frame, text="Confirmar Registro", command=self.ejecutar_registro,
                  font=("Arial", 11, "bold"), bg="#482673", fg="white", 
                  width=20, bd=0, pady=10, cursor="hand2").pack(side="left", padx=10)

        tk.Button(btn_frame, text="Cancelar", command=lambda: self.controller.regresar_al_login(),
                  font=("Arial", 11, "bold"), bg="#333333", fg="white", 
                  width=20, bd=0, pady=10, cursor="hand2").pack(side="left", padx=10)

    def crear_campo(self, parent, texto, row, col):
        tk.Label(parent, text=texto, font=("Arial", 10), fg="#b3b3b3", 
                 bg="#121212").grid(row=row, column=col, sticky="w", padx=20, pady=(10, 0))

    def crear_entry(self, parent, row, col, show=""):
        entry = tk.Entry(parent, font=("Arial", 12), width=30, bg="#1e1e1e", 
                         fg="white", insertbackground="white", bd=0, show=show)
        entry.grid(row=row, column=col, padx=20, pady=5)
        # Añadimos un pequeño borde inferior estético
        line = tk.Frame(parent, bg="#482673", height=2)
        line.grid(row=row, column=col, sticky="swe", padx=20)
        return entry

    def ejecutar_registro(self):
        # Aquí iría la lógica para guardar en base de datos
        print(f"Registrando cuenta para: {self.entry_nombre.get()}")
        self.controller.regresar_al_login()