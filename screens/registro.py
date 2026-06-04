import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
import os
import re

class RegistroFrame(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg="#121212")
        self.controller = controller

        # --- DICCIONARIO MASIVO DE PAÍSES ---
        self.paises = {
            "Afganistán": {"prefijo": "+93", "bandera": "🇦🇫"}, "Alemania": {"prefijo": "+49", "bandera": "🇩🇪"},
            "Argentina": {"prefijo": "+54", "bandera": "🇦🇷"}, "Colombia": {"prefijo": "+57", "bandera": "🇨🇴"},
            "España": {"prefijo": "+34", "bandera": "🇪🇸"}, "Estados Unidos": {"prefijo": "+1", "bandera": "🇺🇸"},
            "Francia": {"prefijo": "+33", "bandera": "🇫🇷"}, "México": {"prefijo": "+52", "bandera": "🇲🇽"},
            "Perú": {"prefijo": "+51", "bandera": "🇵🇪"}, "Reino Unido": {"prefijo": "+44", "bandera": "🇬🇧"},
            "Venezuela": {"prefijo": "+58", "bandera": "🇻🇪"} # (Puedes añadir más si lo deseas)
        }

        # Contenedor principal centrado
        container = tk.Frame(self, bg="#121212")
        container.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

        tk.Label(container, text="🏦 Apertura de Cuenta Bancaria", font=("Arial", 18, "bold"), 
                 fg="white", bg="#121212").grid(row=0, column=0, columnspan=2, pady=(0, 15))

        # --- COLUMNA 1 (Información Personal) ---
        self.crear_campo(container, "Nombre:", 1, 0)
        self.entry_nombre = self.crear_entry(container, 2, 0)

        self.crear_campo(container, "Apellidos:", 3, 0)
        self.entry_apellidos = self.crear_entry(container, 4, 0)

        self.crear_campo(container, "DNI / NIE / Pasaporte:", 5, 0)
        self.entry_dni = self.crear_entry(container, 6, 0)

        self.crear_campo(container, "Fecha de Nacimiento:", 7, 0)
        self.entry_fecha = self.crear_entry(container, 8, 0)
        self.entry_fecha.insert(0, "DD/MM/AAAA")
        self.entry_fecha.config(fg="#555555")
        self.entry_fecha.bind("<FocusIn>", self.fecha_focus_in)
        self.entry_fecha.bind("<FocusOut>", self.fecha_focus_out)
        self.entry_fecha.bind("<KeyRelease>", self.formatear_fecha)

        # --- COLUMNA 2 (Contacto y Seguridad) ---
        self.crear_campo(container, "Correo Electrónico:", 1, 1)
        self.entry_email = self.crear_entry(container, 2, 1)

        # Teléfono con lista desplegable con scroll (Combobox)
        self.crear_campo(container, "Teléfono de contacto (9 dígitos):", 3, 1)
        
        frame_tel = tk.Frame(container, bg="#121212")
        frame_tel.grid(row=4, column=1, padx=20, pady=5, sticky="w")

        opciones_paises = [f"{info['bandera']} {info['prefijo']} ({pais})" for pais, info in self.paises.items()]
        
        self.combo_pais = ttk.Combobox(frame_tel, values=opciones_paises, state="readonly", width=16, font=("Arial", 11))
        self.combo_pais.set("🇪🇸 +34 (España)") 
        self.combo_pais.pack(side="left")

        validador_num = self.register(self.limitar_telefono)
        self.entry_tel = tk.Entry(frame_tel, font=("Arial", 12), width=15, bg="#1e1e1e", 
                                  fg="white", insertbackground="white", bd=0, 
                                  validate="key", validatecommand=(validador_num, '%P'))
        self.entry_tel.pack(side="left", padx=(5, 0))
        self.entry_tel.bind("<KeyRelease>", self.verificar_9_digitos)

        tk.Frame(container, bg="#482673", height=2).grid(row=4, column=1, sticky="swe", padx=20)

        self.lbl_error_tel = tk.Label(container, text="", font=("Arial", 8), fg="#ff4c4c", bg="#121212")
        self.lbl_error_tel.grid(row=5, column=1, sticky="w", padx=20)

        self.crear_campo(container, "Definir Contraseña:", 5, 1)
        self.entry_pass = self.crear_entry(container, 6, 1, show="*")

        self.crear_campo(container, "Repetir Contraseña:", 7, 1)
        self.entry_pass_confirm = self.crear_entry(container, 8, 1, show="*")

        # --- BOTONES ---
        btn_frame = tk.Frame(container, bg="#121212")
        btn_frame.grid(row=9, column=0, columnspan=2, pady=20)

        tk.Button(btn_frame, text="Confirmar Registro", command=self.ejecutar_registro,
                  font=("Arial", 11, "bold"), bg="#482673", fg="white", 
                  width=20, bd=0, pady=10, cursor="hand2").pack(side="left", padx=10)

        tk.Button(btn_frame, text="Cancelar", command=lambda: self.controller.regresar_al_login(),
                  font=("Arial", 11, "bold"), bg="#333333", fg="white", 
                  width=20, bd=0, pady=10, cursor="hand2").pack(side="left", padx=10)

    def crear_campo(self, parent, texto, row, col):
        tk.Label(parent, text=texto, font=("Arial", 10), fg="#b3b3b3", bg="#121212").grid(row=row, column=col, sticky="w", padx=20, pady=(6, 0))

    def crear_entry(self, parent, row, col, show=""):
        entry = tk.Entry(parent, font=("Arial", 12), width=30, bg="#1e1e1e", fg="white", insertbackground="white", bd=0, show=show)
        entry.grid(row=row, column=col, padx=20, pady=5)
        tk.Frame(parent, bg="#482673", height=2).grid(row=row, column=col, sticky="swe", padx=20)
        return entry

    # --- LÓGICA DE INTERFAZ AVANZADA ---
    def limitar_telefono(self, texto_actual):
        if len(texto_actual) > 9: return False
        return texto_actual.isdigit() or texto_actual == ""

    def verificar_9_digitos(self, event):
        num = self.entry_tel.get()
        if len(num) < 9 and len(num) > 0:
            self.lbl_error_tel.config(text="⚠ El número debe tener exactamente 9 dígitos")
        else:
            self.lbl_error_tel.config(text="")

    def fecha_focus_in(self, event):
        if self.entry_fecha.get() == "DD/MM/AAAA":
            self.entry_fecha.delete(0, tk.END)
            self.entry_fecha.config(fg="white")

    def fecha_focus_out(self, event):
        if self.entry_fecha.get() == "":
            self.entry_fecha.insert(0, "DD/MM/AAAA")
            self.entry_fecha.config(fg="#555555")

    def formatear_fecha(self, event):
        if event.keysym == "BackSpace": return
        texto = self.entry_fecha.get().replace("/", "")
        nuevo_texto = ""
        texto = "".join([c for c in texto if c.isdigit()])
        if len(texto) > 0: nuevo_texto += texto[:2]
        if len(texto) > 2: nuevo_texto += "/" + texto[2:4]
        if len(texto) > 4: nuevo_texto += "/" + texto[4:8]
        self.entry_fecha.delete(0, tk.END)
        self.entry_fecha.insert(0, nuevo_texto)

    # --- LÓGICA DE GUARDADO EN .TXT ---
    def ejecutar_registro(self):
        nombre = self.entry_nombre.get().strip()
        apellidos = self.entry_apellidos.get().strip()
        dni = self.entry_dni.get().strip()
        fecha = self.entry_fecha.get().strip()
        email = self.entry_email.get().strip()
        telefono = self.entry_tel.get().strip()
        pass1 = self.entry_pass.get().strip()
        pass2 = self.entry_pass_confirm.get().strip()

        if not (nombre and apellidos and dni and email and telefono and pass1 and pass2) or fecha == "DD/MM/AAAA":
            messagebox.showerror("Error", "Todos los campos son obligatorios.")
            return

        if len(telefono) < 9:
            messagebox.showerror("Error", "El número de teléfono debe tener 9 dígitos.")
            return

        patron_correo = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        if not re.match(patron_correo, email):
            messagebox.showerror("Error", "El correo electrónico introducido no es válido.")
            return

        if pass1 != pass2:
            messagebox.showerror("Error", "Las contraseñas no coinciden.")
            return

        carpeta = "informacion_cliente"
        
        # 📂 NUEVO: Creamos un nombre de carpeta único y seguro para el usuario
        nombre_usuario_seguro = f"{nombre}_{apellidos}".replace(" ", "_")
        carpeta_usuario = os.path.join(carpeta, nombre_usuario_seguro)
        os.makedirs(carpeta_usuario, exist_ok=True)

        # El archivo de perfil ahora se llamará siempre "perfil.txt" dentro de su carpeta
        ruta_completa = os.path.join(carpeta_usuario, "perfil.txt")

        seleccion_pais = self.combo_pais.get()
        prefijo = seleccion_pais.split(" ")[1]

        try:
            with open(ruta_completa, "w", encoding="utf-8") as archivo:
                archivo.write("=======================================\n")
                archivo.write("       INFORMACIÓN BANCARIA DEL CLIENTE\n")
                archivo.write("=======================================\n")
                archivo.write(f"Nombre Completo:      {nombre} {apellidos}\n")
                archivo.write(f"DNI / NIE:            {dni}\n")
                archivo.write(f"Fecha de Nacimiento:  {fecha}\n")
                archivo.write(f"Correo Electrónico:   {email}\n")
                archivo.write(f"Teléfono:             {prefijo} {telefono}\n")
                archivo.write(f"Contraseña:           {pass1}\n")
                
                # Colores por defecto
                archivo.write(f"Color Fondo Menu:     #2D033B\n")
                archivo.write(f"Color Boton Menu:     #482673\n")
                
                archivo.write("=======================================\n")
            
            messagebox.showinfo("Éxito", f"Cuenta bancaria creada para {nombre} {apellidos}.")
            self.controller.regresar_al_login()
            
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo crear el perfil: {e}")