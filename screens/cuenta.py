import tkinter as tk
from tkinter import messagebox
import os

class CuentaFrame(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg="#121212")
        self.controller = controller
        self.archivo_actual = None # Almacenará la ruta del perfil.txt del usuario logueado

        tk.Label(self, text="⚙️ CONFIGURACIÓN DE CUENTA", font=("Arial", 20, "bold"),
                 bg="#121212", fg="white").pack(pady=(20, 10))

        # Contenedor para organizar en 2 columnas (Izquierda: Datos, Derecha: Personalización)
        main_container = tk.Frame(self, bg="#121212")
        main_container.pack(fill="both", expand=True, padx=20, pady=10)

        # --- COLUMNA IZQUIERDA: INFORMACIÓN PERSONAL ---
        frame_info = tk.LabelFrame(main_container, text=" Información Personal ", 
                                   font=("Arial", 11, "bold"), fg="#00ffcc", bg="#121212", bd=1)
        frame_info.pack(side="left", fill="both", expand=True, padx=(0, 10))

        self.campos = {}
        # MODIFICADO: Quitamos "Contraseña" de aquí para manejarla exclusivamente con el nuevo botón
        labels = ["Nombre Completo:", "DNI / NIE:", "Fecha de Nac.:", "Correo:", "Teléfono:"]
        
        for i, texto in enumerate(labels):
            tk.Label(frame_info, text=texto, font=("Arial", 10), fg="#b3b3b3", bg="#121212").grid(row=i*2, column=0, sticky="w", padx=15, pady=(5, 0))
            entry = tk.Entry(frame_info, font=("Arial", 11), bg="#1e1e1e", fg="white", insertbackground="white", bd=0, width=35)
            entry.grid(row=i*2+1, column=0, sticky="w", padx=15, pady=2)
            self.campos[texto] = entry

        # Contenedor inferior para los botones de la izquierda
        frame_botones_perfil = tk.Frame(frame_info, bg="#121212")
        frame_botones_perfil.grid(row=len(labels)*2, column=0, sticky="w", padx=15, pady=20)

        # Botón para Guardar Datos (Nombre, DNI, Correo, etc.)
        btn_guardar = tk.Button(frame_botones_perfil, text="💾 Guardar Cambios", command=self.guardar_cambios,
                               font=("Arial", 10, "bold"), bg="#482673", fg="white", bd=0, padx=12, pady=6, cursor="hand2")
        btn_guardar.pack(side="left", padx=(0, 10))

        # NUEVO: Botón para abrir la ventana flotante de cambiar contraseña
        btn_pass = tk.Button(frame_botones_perfil, text="🔒 Cambiar Contraseña", command=self.abrir_ventana_cambiar_password,
                             font=("Arial", 10, "bold"), bg="#333333", fg="#00ffcc", bd=0, padx=12, pady=6, cursor="hand2")
        btn_pass.pack(side="left")

        # --- COLUMNA DERECHA: PERSONALIZACIÓN (COLORES) ---
        frame_colores = tk.LabelFrame(main_container, text=" Personalización de Colores ", 
                                      font=("Arial", 11, "bold"), fg="#00ffcc", bg="#121212", bd=1)
        frame_colores.pack(side="right", fill="both", expand=True, padx=(10, 0))

        tk.Label(frame_colores, text="Selecciona el tema de la aplicación:", font=("Arial", 10), fg="#b3b3b3", bg="#121212").pack(pady=10)

        colores = [
            ("Morado Imperial", "#2D033B", "#482673"),
            ("Azul Eléctrico", "#0D47A1", "#1976D2"),
            ("Naranja Atardecer", "#E65100", "#F57C00"),
            ("Verde Selva", "#1B5E20", "#2E7D32")
        ]

        for nombre, c_fondo, c_btn in colores:
            tk.Button(frame_colores, text=nombre, bg=c_fondo, fg="white", width=22, font=("Arial", 10), bd=0, pady=8, cursor="hand2",
                      command=lambda f=c_fondo, b=c_btn: self.controller.cambiar_color_global(f, b)).pack(pady=6)

    def cargar_datos_usuario(self):
        self.archivo_actual = self.controller.usuario_logueado
        if not self.archivo_actual or not os.path.exists(self.archivo_actual):
            return
            
        try:
            with open(self.archivo_actual, "r", encoding="utf-8") as f:
                lineas = f.readlines()
                
            for entry in self.campos.values():
                entry.delete(0, tk.END)
                
            for linea in lineas:
                partes = linea.split(":")
                if len(partes) >= 2:
                    clave = partes[0].strip()
                    valor = partes[1].strip()
                    
                    if clave == "Nombre Completo:":
                        self.campos["Nombre Completo:"].insert(0, valor)
                    elif clave == "DNI / NIE:":
                        self.campos["DNI / NIE:"].insert(0, valor)
                    elif clave == "Fecha de Nacimiento:":
                        self.campos["Fecha de Nac.:"].insert(0, valor)
                    elif clave == "Correo Electrónico:":
                        self.campos["Correo:"].insert(0, valor)
                    elif clave == "Teléfono:":
                        self.campos["Teléfono:"].insert(0, valor)
        except Exception as e:
            print(f"Error al cargar datos del usuario: {e}")

    def guardar_cambios(self):
        nombre = self.campos["Nombre Completo:"].get().strip()
        if not nombre:
            messagebox.showerror("Error", "El nombre completo no puede estar vacío.")
            return
            
        try:
            # Leemos la contraseña actual directamente desde el archivo para no perderla ni sobreescribirla
            contrasena_actual = ""
            if os.path.exists(self.archivo_actual):
                with open(self.archivo_actual, "r", encoding="utf-8") as f:
                    for linea in f.readlines():
                        if linea.startswith("Contraseña:"):
                            contrasena_actual = linea.split(":")[1].strip()
                            break
                            
            with open(self.archivo_actual, "w", encoding="utf-8") as f:
                f.write("=======================================\n")
                f.write("       INFORMACIÓN BANCARIA DEL CLIENTE\n")
                f.write("=======================================\n")
                f.write(f"Nombre Completo:      {nombre}\n")
                f.write(f"DNI / NIE:            {self.campos['DNI / NIE:'].get().strip()}\n")
                f.write(f"Fecha de Nacimiento:  {self.campos['Fecha de Nac.:'].get().strip()}\n")
                f.write(f"Correo Electrónico:   {self.campos['Correo:'].get().strip()}\n")
                f.write(f"Teléfono:             {self.campos['Teléfono:'].get().strip()}\n")
                f.write(f"Contraseña:           {contrasena_actual}\n")
                f.write(f"Color Fondo Menu:     {self.controller.color_menu}\n")
                f.write(f"Color Boton Menu:     {self.controller.color_btn}\n")
                f.write("=======================================\n")
                
            # Si cambió el nombre, renombramos la carpeta del usuario (Arquitectura nueva)
            nuevo_nombre_carpeta = nombre.replace(' ', '_')
            nueva_carpeta_usuario = os.path.join("informacion_cliente", nuevo_nombre_carpeta)
            carpeta_actual = os.path.dirname(self.archivo_actual)
            
            if carpeta_actual != nueva_carpeta_usuario:
                try:
                    os.rename(carpeta_actual, nueva_carpeta_usuario)
                    self.archivo_actual = os.path.join(nueva_carpeta_usuario, "perfil.txt")
                    self.controller.usuario_logueado = self.archivo_actual
                except Exception as e:
                    print(f"Error al renombrar la carpeta del usuario: {e}")
                
            messagebox.showinfo("Éxito", "Tus datos se han actualizado correctamente.")
        except Exception as e:
            messagebox.showerror("Error", f"No se pudieron guardar los cambios: {e}")

    # NUEVO MÉTODO: Ventana emergente ("pestaña") para cambiar contraseña
    def abrir_ventana_cambiar_password(self):
        ventana_pass = tk.Toplevel(self)
        ventana_pass.title("Cambiar Contraseña")
        ventana_pass.geometry("360x380")
        ventana_pass.configure(bg="#121212")
        ventana_pass.resizable(False, False)
        
        # Hace que la ventana flotante sea modal (bloquea la de atrás hasta cerrarse)
        ventana_pass.transient(self)
        ventana_pass.grab_set()
        
        tk.Label(ventana_pass, text="🔒 Actualizar Contraseña", font=("Arial", 14, "bold"), fg="#00ffcc", bg="#121212").pack(pady=15)
        
        # Caja 1: Contraseña Actual
        tk.Label(ventana_pass, text="Contraseña Actual:", font=("Arial", 10), fg="#b3b3b3", bg="#121212").pack(anchor="w", padx=30, pady=(5,0))
        entry_actual = tk.Entry(ventana_pass, font=("Arial", 11), bg="#1e1e1e", fg="white", insertbackground="white", bd=0, show="*", width=30)
        entry_actual.pack(padx=30, pady=5)
        
        # Caja 2: Nueva Contraseña
        tk.Label(ventana_pass, text="Nueva Contraseña:", font=("Arial", 10), fg="#b3b3b3", bg="#121212").pack(anchor="w", padx=30, pady=(5,0))
        entry_nueva = tk.Entry(ventana_pass, font=("Arial", 11), bg="#1e1e1e", fg="white", insertbackground="white", bd=0, show="*", width=30)
        entry_nueva.pack(padx=30, pady=5)
        
        # Caja 3: Repetir Nueva Contraseña
        tk.Label(ventana_pass, text="Repetir Nueva Contraseña:", font=("Arial", 10), fg="#b3b3b3", bg="#121212").pack(anchor="w", padx=30, pady=(5,0))
        entry_repetir = tk.Entry(ventana_pass, font=("Arial", 11), bg="#1e1e1e", fg="white", insertbackground="white", bd=0, show="*", width=30)
        entry_repetir.pack(padx=30, pady=5)
        
        def confirmar_cambio():
            pass_actual = entry_actual.get().strip()
            pass_nueva = entry_nueva.get().strip()
            pass_repetir = entry_repetir.get().strip()
            
            # 1. Validación de campos vacíos
            if not pass_actual or not pass_nueva or not pass_repetir:
                messagebox.showerror("Error", "Por favor, rellena las tres cajas de texto.", parent=ventana_pass)
                return
                
            # Leer el archivo actual para validar la contraseña guardada
            contrasena_guardada = ""
            try:
                with open(self.archivo_actual, "r", encoding="utf-8") as f:
                    lineas = f.readlines()
                for linea in lineas:
                    if linea.startswith("Contraseña:"):
                        contrasena_guardada = linea.split(":")[1].strip()
                        break
            except Exception as e:
                messagebox.showerror("Error", f"No se pudo leer el perfil: {e}", parent=ventana_pass)
                return
                
            # 2. Validación de Contraseña Actual correcta
            if pass_actual != contrasena_guardada:
                messagebox.showerror("Error", "La contraseña actual es incorrecta.", parent=ventana_pass)
                return
                
            # 3. Validación de coincidencia de contraseña nueva
            if pass_nueva != pass_repetir:
                messagebox.showerror("Error", "La nueva contraseña y su repetición no coinciden.", parent=ventana_pass)
                return
                
            # 4. Validación extra: que no ponga la misma que ya tenía
            if pass_actual == pass_nueva:
                messagebox.showerror("Error", "La nueva contraseña no puede ser igual a la actual.", parent=ventana_pass)
                return
            
            # Proceder a reescribir el archivo cambiando únicamente la línea de la contraseña
            try:
                lineas_actualizadas = []
                for linea in lineas:
                    if linea.startswith("Contraseña:"):
                        lineas_actualizadas.append(f"Contraseña:           {pass_nueva}\n")
                    else:
                        lineas_actualizadas.append(linea)
                        
                with open(self.archivo_actual, "w", encoding="utf-8") as f:
                    f.writelines(lineas_actualizadas)
                    
                messagebox.showinfo("Éxito", "¡Contraseña actualizada correctamente!", parent=ventana_pass)
                ventana_pass.destroy() # Cierra automáticamente la ventana flotante
                
            except Exception as e:
                messagebox.showerror("Error", f"No se pudo guardar la contraseña: {e}", parent=ventana_pass)
                
        # Botón Confirmar dentro de la ventana emergente (utiliza dinámicamente tu color de botón del menú)
        btn_confirmar = tk.Button(ventana_pass, text="Confirmar Cambio", command=confirmar_cambio,
                                  font=("Arial", 11, "bold"), bg=self.controller.color_btn, fg="white", bd=0, pady=8, cursor="hand2")
        btn_confirmar.pack(fill="x", padx=30, pady=25)