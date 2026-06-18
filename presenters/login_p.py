# presenters/login_p.py
# ¡NOTAR QUE HEMOS ELIMINADO COMPLETAMENTE EL IMPORT DE TKINTER MESSAGEBOX AQUÍ!

class LoginPresenter:
    def __init__(self, view, model):
        self.view = view
        self.model = model

    def crear_cuenta(self):
        # Mantiene tu navegación delegada al controlador de pantallas
        self.view.controller.mostrar_registro()

    def verificar_login(self, usuario_crudo, password_crudo):
        """Ahora recibe los textos directamente desde la vista como parámetros limpios"""
        correo_ingresado = usuario_crudo.strip()
        pass_ingresada = password_crudo.strip()

        # Validación de campos vacíos
        if not correo_ingresado or not pass_ingresada:
            # Le ordenamos a la vista que muestre el popup. El presenter no decide CÓMO se muestra.
            self.view.mostrar_error("Error", "Por favor, rellena todos los campos.")
            return

        # Solicitamos de forma directa al modelo evaluar los textos
        usuario_valido, ruta_usuario, codigo_error = self.model.validar_credenciales(correo_ingresado, pass_ingresada)

        if codigo_error == "no_usuarios":
            self.view.mostrar_error("Error", "No hay usuarios registrados en el sistema.")
            return

        if usuario_valido:
            # Transferimos el archivo de perfil correspondiente para iniciar la sesión
            self.view.controller.login_exitoso(ruta_usuario)
        else:
            self.view.mostrar_error("Error", "El correo o la contraseña son incorrectos.")