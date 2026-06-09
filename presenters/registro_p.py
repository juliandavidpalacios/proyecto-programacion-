import tkinter as tk
from tkinter import messagebox

# Definimos la clase RegistroPresenter que actuará de controlador intermediario en el patrón MVP
class RegistroPresenter:
    # Constructor de la clase Presentador que recibe e intercepta las instancias de la vista y del modelo
    def __init__(self, view, model):
        # Enlazamos de forma interna la instancia de la vista para poder leer y alterar sus variables gráficas
        self.view = view
        # Enlazamos de forma interna la instancia del modelo para acceder a sus rutinas lógicas de datos
        self.model = model

        # Diccionario estructurado que almacena la información de los prefijos telefónicos y banderas por país
        self.paises = {
            "Afganistán": {"prefijo": "+93", "bandera": "🇦🇫"}, "Alemania": {"prefijo": "+49", "bandera": "🇩🇪"},
            "Argentina": {"prefijo": "+54", "bandera": "🇦🇷"}, "Colombia": {"prefijo": "+57", "bandera": "🇨🇴"},
            "España": {"prefijo": "+34", "bandera": "🇪🇸"}, "Estados Unidos": {"prefijo": "+1", "bandera": "🇺🇸"},
            "Francia": {"prefijo": "+33", "bandera": "🇫🇷"}, "México": {"prefijo": "+52", "bandera": "🇲🇽"},
            "Perú": {"prefijo": "+51", "bandera": "🇵🇪"}, "Reino Unido": {"prefijo": "+44", "bandera": "🇬🇧"},
            "Venezuela": {"prefijo": "+58", "bandera": "🇻🇪"}
        }

    # Método utilitario para proveer a la vista el listado crudo de los países admitidos por la aplicación
    def obtener_paises(self):
        # Retorna el diccionario de datos geográficos local
        return self.paises

    # Método interceptor de validación en tiempo real para prohibir la escritura de letras o más de 9 caracteres
    def limitar_telefono(self, texto_actual):
        # Si la longitud del texto pretendido por el teclado excede los 9 dígitos, rechaza el ingreso (False)
        if len(texto_actual) > 9: return False
        # Retorna un valor booleano comprobando si la cadena es un dígito entero o si el campo se encuentra vacío
        return texto_actual.isdigit() or texto_actual == ""

    # Método encargado de actualizar dinámicamente la etiqueta de advertencia si el teléfono está incompleto
    def verificar_9_digitos(self, event):
        # Extrae la cadena de caracteres alojada actualmente en el cuadro numérico de la vista
        num = self.view.entry_tel.get()
        # Si el número ingresado posee caracteres pero no alcanza la cuota obligatoria de 9 dígitos
        if len(num) < 9 and len(num) > 0:
            # Modifica la etiqueta de error de la vista inyectándole el texto de advertencia explícito
            self.view.lbl_error_tel.config(text="⚠ El número debe tener exactamente 9 dígitos")
        # Si el campo se vacía o cumple de forma perfecta con los 9 dígitos requeridos
        else:
            # Limpia por completo el mensaje de advertencia visual de la pantalla
            self.view.lbl_error_tel.config(text="")

    # Evento de UI gatillado al pulsar el ratón sobre el entry de fecha para remover el marcador de posición
    def fecha_focus_in(self, event):
        # Si el contenido actual coincide de forma exacta con la cadena base del placeholder
        if self.view.entry_fecha.get() == "DD/MM/AAAA":
            # Vacía la caja de texto eliminando los caracteres desde el índice cero hasta el final (tk.END)
            self.view.entry_fecha.delete(0, tk.END)
            # Modifica el color de la tipografía a blanco para adecuarlo a la entrada de datos activa
            self.view.entry_fecha.config(fg="white")

    # Evento de UI gatillado cuando el cursor abandona la caja de texto de la fecha dejándola desatendida
    def fecha_focus_out(self, event):
        # Si el cliente retiró el foco del teclado dejando la caja de texto totalmente vacía
        if self.view.entry_fecha.get() == "":
            # Inserta de forma automática el texto guía predeterminado del marcador de posición
            self.view.entry_fecha.insert(0, "DD/MM/AAAA")
            # Configura un color gris opaco para denotar el estado inactivo del placeholder
            self.view.entry_fecha.config(fg="#555555")

    # Algoritmo interactivo encargado de inyectar las barras laterales ("/") automáticamente al digitar la fecha
    def formatear_fecha(self, event):
        # Si la tecla liberada por el usuario corresponde al borrado hacia atrás, detiene la autoinserción de barras
        if event.keysym == "BackSpace": return
        # Obtiene el texto del entry de fecha removiendo temporalmente las barras existentes para analizar los números
        texto = self.view.entry_fecha.get().replace("/", "")
        # Inicializa una cadena vacía destinada a reconstruir la fecha formateada de forma limpia
        nuevo_texto = ""
        # Limpia el texto reteniendo única y exclusivamente los caracteres numéricos mediante una lista de comprensión
        texto = "".join([c for c in texto if c.isdigit()])
        # Si el cliente ya ingresó números, toma los primeros dos dígitos representativos del Día
        if len(texto) > 0: nuevo_texto += texto[:2]
        # Si el volumen numérico rebasa los dos caracteres, concatena la barra divisoria seguida de los dígitos del Mes
        if len(texto) > 2: nuevo_texto += "/" + texto[2:4]
        # Si el volumen numérico rebasa los cuatro caracteres, anexa la segunda barra junto con los dígitos del Año
        if len(texto) > 4: nuevo_texto += "/" + texto[4:8]
        # Remueve la cadena desorganizada presente en la caja de texto de la vista
        self.view.entry_fecha.delete(0, tk.END)
        # Inserta de forma limpia la cadena estructurada bajo el formato cronológico correcto (DD/MM/AAAA)
        self.view.entry_fecha.insert(0, nuevo_texto)

    # Método principal ejecutado al pulsar el botón de confirmación para validar y procesar el alta de la cuenta
    def ejecutar_registro(self):
        # Extrae y remueve espacios del parámetro del nombre guardado en la vista
        nombre = self.view.entry_nombre.get().strip()
        # Extrae y remueve espacios del parámetro de los apellidos guardado en la vista
        apellidos = self.view.entry_apellidos.get().strip()
        # Extrae y remueve espacios del parámetro de identificación DNI guardado en la vista
        dni = self.view.entry_dni.get().strip()
        # Extrae y remueve espacios de la cadena cronológica de la fecha de nacimiento de la vista
        fecha = self.view.entry_fecha.get().strip()
        # Extrae y remueve espacios de la dirección de correo electrónico de la vista
        email = self.view.entry_email.get().strip()
        # Extrae y remueve espacios del número de contacto telefónico de la vista
        telefono = self.view.entry_tel.get().strip()
        # Extrae y remueve espacios de la contraseña de seguridad ingresada en la vista
        pass1 = self.view.entry_pass.get().strip()
        # Extrae y remueve espacios de la confirmación de contraseña ingresada en la vista
        pass2 = self.view.entry_pass_confirm.get().strip()

        # Valida de manera colectiva si algún campo obligatorio se encuentra vacío o conserva el marcador de la fecha
        if not (nombre and apellidos and dni and email and telefono and pass1 and pass2) or fecha == "DD/MM/AAAA":
            # Lanza un modal de error notificando la obligatoriedad de rellenar todo el formulario
            messagebox.showerror("Error", "Todos los campos son obligatorios.")
            # Rompe la ejecución del flujo de alta
            return

        # Verifica sintácticamente si la longitud de la cadena telefónica es inferior a los 9 dígitos obligatorios
        if len(telefono) < 9:
            # Lanza una ventana modal avisando la anomalía numérica del teléfono
            messagebox.showerror("Error", "El número de teléfono debe tener 9 dígitos.")
            # Rompe la ejecución de la orden de registro
            return

        # Solicita al modelo validar la dirección de correo electrónico mediante su motor de expresiones regulares
        if not self.model.validar_correo(email):
            # Lanza una ventana de alerta informando que la sintaxis de la dirección de email es incorrecta
            messagebox.showerror("Error", "El correo electrónico introducido no es válido.")
            # Detiene el proceso de guardado
            return

        # Comprueba de forma lógica si las dos cadenas de texto de las contraseñas difieren entre sí
        if pass1 != pass2:
            # Lanza un modal de error advirtiendo que las claves introducidas no coinciden de forma exacta
            messagebox.showerror("Error", "Las contraseñas no coinciden.")
            # Detiene la rutina de registro
            return

        # Extrae el texto de selección actual del menú desplegable Combobox de la vista
        seleccion_pais = self.view.combo_pais.get()
        # Descompone el texto del país por medio de espacios y extrae el segundo elemento (índice 1), es decir, el prefijo
        prefijo = seleccion_pais.split(" ")[1]

        # Invoca formalmente al modelo delegándole todos los parámetros depurados para efectuar la persistencia en disco
        exito, error_obj = self.model.registrar_usuario(nombre, apellidos, dni, fecha, email, telefono, prefijo, pass1)

        # Evalúa si la operación de registro fue procesada y confirmada de forma exitosa por el modelo
        if exito:
            # Despliega una alerta modal de éxito confirmando la apertura de la cuenta bancaria del cliente
            messagebox.showinfo("Éxito", f"Cuenta bancaria creada para {nombre} {apellidos}.")
            # Redirige de forma automática al usuario a la pantalla de Login a través del controlador global de la vista
            self.view.controller.regresar_al_login()
        # Si el modelo capturó una excepción y devolvió un estado fallido en la operación
        else:
            # Despliega una alerta modal de error proyectando en pantalla la descripción técnica del fallo surgido
            messagebox.showerror("Error", f"No se pudo crear el perfil: {error_obj}")