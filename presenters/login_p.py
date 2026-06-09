# Importamos el módulo de alertas gráficas messagebox perteneciente a la librería tkinter
from tkinter import messagebox

# Definimos la clase del Presentador encargada de intermediar los flujos lógicos entre el Modelo y la Vista
class LoginPresenter:
    # Definimos el constructor del presentador requiriendo las instancias físicas de la vista y del modelo
    def __init__(self, view, model):
        # Almacenamos la referencia de la vista en una variable de instancia interna para leer y mutar su estado
        self.view = view
        # Almacenamos la referencia del modelo para llamarlo cuando se requieran transacciones de datos
        self.model = model

    # Método que intercepta la petición de registro de cuenta del botón correspondiente
    def crear_cuenta(self):
        # Delega la tarea al controlador original llamando al método mostrar_registro para cambiar de frame
        self.view.controller.mostrar_registro()

    # Método que orquesta la verificación completa de las credenciales del formulario de login
    def verificar_login(self):
        # Obtenemos los caracteres escritos en el cuadro de texto del usuario, removiendo los espacios en blanco
        correo_ingresado = self.view.entry_usuario.get().strip()
        # Obtenemos los caracteres escritos en el cuadro de contraseña limpiando también sus extremos
        pass_ingresada = self.view.entry_password.get().strip()

        # Evaluamos de manera condicional si alguno de los dos campos del formulario fue enviado vacío
        if not correo_ingresado or not pass_ingresada:
            # Mostramos un cuadro emergente de error indicando al cliente que debe llenar todos los datos
            messagebox.showerror("Error", "Por favor, rellena todos los campos.")
            # Interrumpimos inmediatamente la secuencia de ejecución del login mediante un return de escape
            return

        # Solicitamos de forma directa al modelo evaluar los textos extraídos comparándolos contra los archivos
        usuario_valido, ruta_usuario, codigo_error = self.model.validar_credenciales(correo_ingresado, pass_ingresada)

        # Si el modelo responde que el error específico devuelto fue la ausencia absoluta de usuarios
        if codigo_error == "no_usuarios":
            # Desplegamos un mensaje flotante advirtiendo que el sistema no posee cuentas creadas aún
            messagebox.showerror("Error", "No hay usuarios registrados en el sistema.")
            # Finalizamos la función de inicio de sesión
            return

        # Si el modelo confirma mediante su bandera booleana que las credenciales son auténticas e idénticas
        if usuario_valido:
            # Ejecutamos con éxito el método del controlador original transfiriéndole el archivo perfil.txt correspondiente
            self.view.controller.login_exitoso(ruta_usuario)
        # Si la bandera es False lo que significa que el correo o la contraseña no matchearon con ningún perfil
        else:
            # Lanzamos un cuadro modal informando el rechazo de las credenciales ingresadas al sistema
            messagebox.showerror("Error", "El correo o la contraseña son incorrectos.")