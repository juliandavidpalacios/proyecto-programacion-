import os # Importa la librería os para interactuar con rutas de archivos y nombres de directorios en el sistema
import tkinter as tk # Importa el módulo principal de tkinter para manipular constantes o flujos de interfaz base
from tkinter import messagebox # Importa messagebox para detonar cuadros modales de diálogos interactivos sobre la pantalla

class CuentaPresenter: # Declara la clase CuentaPresenter encargada de coordinar las reglas lógicas entre la vista y el modelo
    def __init__(self, view, model): # Constructor del presentador que recibe de forma obligatoria las instancias de la vista y del modelo
        self.view = view # Guarda internamente la instancia de la vista para poder interrogar y actualizar sus widgets visuales
        self.model = model # Almacena de forma interna el objeto modelo para delegar los procesos de almacenamiento físico de datos
        self.view.set_presenter(self) # Registra de forma cruzada este objeto presentador dentro de la configuración de la vista
    def cargar_datos_usuario(self): # Lógica encargada de coordinar la lectura de datos del modelo y poblar los cuadros de la vista
        self.view.archivo_actual = self.view.controller.usuario_logueado # Extrae la ruta de autenticación desde el controlador inyectándola en la variable de la vista
        lineas = self.model.cargar_lineas_perfil(self.view.archivo_actual) # Invoca al objeto modelo para extraer secuencialmente las líneas del fichero físico
        if lineas is None: # Evalúa si el archivo de datos no existe o arrojó una lectura vacía por error en el sistema
            return # Detiene la ejecución del procedimiento previniendo fallos por ausencia de datos de perfil legibles
        for entry in self.view.campos.values(): # Itera de forma limpia por cada objeto de entrada de texto registrado en el diccionario
            entry.delete(0, tk.END) # Vacía el contenido previo remanente en el campo de texto desde la posición inicial a la final
        for linea in lineas: # Recorre secuencialmente cada uno de los registros de líneas provistos por la lectura del modelo
            partes = linea.split(":") # Separa la cadena de caracteres utilizando el carácter de dos puntos como regla de segmentación
            if len(partes) >= 2: # Verifica que la línea procesada contenga al menos un par clave-valor válido tras la división
                clave = partes[0].strip() # Extrae la primera porción limpiando los espacios vacíos laterales para usarla como clave de control
                valor = partes[1].strip() # Recolecta la segunda sección limpiando los espacios para obtener el valor del atributo asociado
                if clave == "Nombre Completo:": # Evalúa si el identificador clave coincide de forma exacta con el nombre del cliente
                    self.view.campos["Nombre Completo:"].insert(0, valor) # Inserta la cadena del nombre dentro del correspondiente widget entry de la vista
                elif clave == "DNI / NIE:": # Evalúa si el indicador clave recuperado corresponde al documento nacional de identidad
                    self.view.campos["DNI / NIE:"].insert(0, valor) # Escribe el valor del documento de identidad en su cuadro de captura de texto
                elif clave == "Fecha de Nacimiento:": # Comprueba si el registro clave coincide con los datos de nacimiento del usuario activo
                    self.view.campos["Fecha de Nac.:"].insert(0, valor) # Escribe el valor de la fecha dentro de la caja de texto asignada en el panel
                elif clave == "Correo Electrónico:": # Evalúa si la etiqueta corresponde al correo electrónico guardado
                    self.view.campos["Correo:"].insert(0, valor) # Agrega la dirección de correo limpia en el campo de entrada de texto correspondiente
                elif clave == "Teléfono:": # Comprueba si el identificador de la línea corresponde al número telefónico de contacto
                    self.view.campos["Teléfono:"].insert(0, valor) # Rellena la entrada de texto de teléfono en la interfaz gráfica con el valor leído
    def guardar_cambios(self): # Método encargado de recopilar la información del formulario, validar su consistencia y persistir los cambios
        nombre = self.view.campos["Nombre Completo:"].get().strip() # Captura la cadena de texto del campo de nombre de la vista removiendo espacios en blanco
        if not nombre: # Evalúa si el usuario dejó en blanco el cuadro de texto del nombre completo obligatorio
            messagebox.showerror("Error", "El nombre completo no puede estar vacío.") # Dispara una alerta de error restrictiva informando sobre la omisión del campo
            return # Detiene el proceso de guardado para impedir que se creen perfiles sin una identificación nominal válida
        try: # Apertura del bloque de control de excepciones para aislar errores físicos de escritura o E/S en disco
            contrasena_actual = self.model.obtener_contrasena_actual(self.view.archivo_actual) # Llama al modelo para rastrear y extraer la clave de seguridad vigente del archivo de perfil
            self.model.escribir_perfil_completo(self.view.archivo_actual, nombre, self.view.campos['DNI / NIE:'].get().strip(), self.view.campos['Fecha de Nac.:'].get().strip(), self.view.campos['Correo:'].get().strip(), self.view.campos['Teléfono:'].get().strip(), contrasena_actual, self.view.controller.color_menu, self.view.controller.color_btn) # Ordena al modelo reescribir integralmente el archivo de configuración volcando los nuevos parámetros recolectados
            nuevo_nombre_carpeta = nombre.replace(' ', '_') # Crea la cadena del nuevo directorio sustituyendo todos los espacios vacíos por caracteres de guion bajo
            nueva_carpeta_usuario = os.path.join("informacion_cliente", nuevo_nombre_carpeta) # Compone la ruta absoluta destino combinando la carpeta base con el nuevo directorio formateado
            carpeta_actual = os.path.dirname(self.view.archivo_actual) # Extrae el nombre del directorio actual en donde se encuentra el archivo perfil en uso
            if carpeta_actual != nueva_carpeta_usuario: # Evalúa si la ruta de la carpeta física actual difiere de la nueva ubicación generada por el cambio de nombre
                try: # Bloque de seguridad interno para manejar la operación crítica de renombrado de carpetas del sistema
                    os.rename(carpeta_actual, nueva_carpeta_usuario) # Solicita al sistema operativo renombrar la carpeta del usuario a la nueva ubicación física en disco
                    self.view.archivo_actual = os.path.join(nueva_carpeta_usuario, "perfil.txt") # Actualiza la ruta del archivo actual dentro del objeto vista con la nueva dirección calculada
                    self.view.controller.usuario_logueado = self.view.archivo_actual # Sincroniza la propiedad de estado de sesión del controlador global apuntando al nuevo archivo
                except Exception as e: # Captura cualquier error de permisos o colisión al intentar modificar directorios del sistema de archivos
                    print(f"Error al renombrar la carpeta del usuario: {e}") # Emite un reporte descriptivo con la traza exacta del fallo por la consola estándar
            messagebox.showinfo("Éxito", "Tus datos se han actualizado correctamente.") # Lanza un cuadro de diálogo informando que los datos personales se modificaron de forma exitosa
        except Exception as e: # Captura cualquier otra excepción no controlada ocurrida durante las fases de persistencia de archivos
            messagebox.showerror("Error", f"No se pudieron guardar los cambios: {e}") # Muestra un cuadro emergente de error con los detalles técnicos del fallo en disco
    def confirmar_cambio_password(self, entry_actual, entry_nueva, entry_repetir, ventana_pass): # Método para realizar las validaciones de negocio y actualizar el campo de contraseña en el archivo
        pass_actual = entry_actual.get().strip() # Obtiene la cadena de texto de la contraseña actual de la entrada de interfaz de manera limpia
        pass_nueva = entry_nueva.get().strip() # Extrae el contenido de texto ingresado en el cuadro asignado para el nuevo password secreto
        pass_repetir = entry_repetir.get().strip() # Recolecta la cadena de caracteres digitada en el cuadro de confirmación y repetición obligatoria
        if not pass_actual or not pass_nueva or not pass_repetir: # Evalúa si alguna de las tres entradas de texto obligatorias de la interfaz quedó vacía
            messagebox.showerror("Error", "Por favor, rellena las tres cajas de texto.", parent=ventana_pass) # Despliega un cuadro de diálogo de error forzando a completar el formulario de seguridad entero
            return # Aborta la operación de guardado debido a que faltan datos esenciales para validar el cambio de clave
        contrasena_guardada = self.model.obtener_contrasena_actual(self.view.archivo_actual) # Solicita al modelo que abra el archivo y recupere el registro real de la clave secreta vigente
        if contrasena_guardada == "ERROR": # Verifica si el modelo reportó un fallo crítico de lectura al intentar acceder al archivo de configuración
            messagebox.showerror("Error", "No se pudo leer el perfil para verificar la contraseña.", parent=ventana_pass) # Muestra un error informando de la imposibilidad de verificar las credenciales actuales en disco
            return # Detiene la ejecución del flujo previniendo corrupción de datos por lectura fallida del perfil
        if pass_actual != contrasena_guardada: # Valida si la clave introducida por el usuario difiere de la contraseña real almacenada en el archivo plano
            messagebox.showerror("Error", "La contraseña actual es incorrecta.", parent=ventana_pass) # Muestra un cuadro de error informando que el password ingresado no autoriza la operación
            return # Cancela el proceso impidiendo que usuarios no autorizados alteren las claves de acceso de la cuenta
        if pass_nueva != pass_repetir: # Comprueba si la nueva contraseña y su correspondiente repetición de control no coinciden entre sí
            messagebox.showerror("Error", "La nueva contraseña y su repetición no coinciden.", parent=ventana_pass) # Emite un mensaje de error alertando sobre la asimetría de los datos clave ingresados
            return # Cancela la actualización de datos obligando a escribir las claves nuevas de forma idéntica
        if pass_actual == pass_nueva: # Evalúa si la nueva clave de seguridad ingresada es idéntica a la credencial actual que ya posee el usuario
            messagebox.showerror("Error", "La nueva contraseña no puede ser igual a la actual.", parent=ventana_pass) # Muestra un diálogo informando que las directivas exigen una clave diferente a la anterior
            return # Cancela el flujo evitando reprocesamientos innecesarios o riesgos de seguridad por contraseñas idénticas
        try: # Abre un bloque de captura para aislar fallos de sobreescritura del parámetro de seguridad en el archivo plano
            self.model.actualizar_contrasena(self.view.archivo_actual, pass_nueva) # Envía los parámetros al modelo para que actualice la línea de credencial dentro del perfil
            messagebox.showinfo("Éxito", "¡Contraseña actualizada correctamente!", parent=ventana_pass) # Lanza un aviso de confirmación informando al usuario el éxito del cambio de contraseña
            ventana_pass.destroy() # Ejecuta la destrucción y cierre físico del componente de la ventana modal liberando la interfaz principal
        except Exception as e: # Atrapa excepciones de E/S o fallos físicos al intentar guardar las nuevas directivas del password en disco
            messagebox.showerror("Error", f"No se pudo guardar la contraseña: {e}", parent=ventana_pass) # Presenta una notificación visual alertando del error crítico