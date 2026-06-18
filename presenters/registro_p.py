# presenters/registro_p.py

class RegistroPresenter:
    def __init__(self, view, model):
        self.view = view
        self.model = model

    def obtener_paises(self):
        """Pide al modelo la lista de países para que la vista los pueda cargar en el Combobox."""
        return self.model.obtener_paises()

    def verificar_registro(self, nombre, apellidos, dni, fecha, email, telefono, pais_seleccionado, pass1, pass2):
        """Recibe datos puros de la vista, valida lo básico y delega al modelo."""
        
        # 1. Validaciones de la interfaz (Campos vacíos o contraseñas que no coinciden)
        if not all([nombre, apellidos, dni, fecha, email, telefono, pais_seleccionado, pass1, pass2]):
            self.view.mostrar_error("Error", "Todos los campos son obligatorios.")
            return

        if pass1 != pass2:
            self.view.mostrar_error("Error", "Las contraseñas no coinciden.")
            return

        # 2. Extraer prefijo del país de forma limpia
        try:
            prefijo = pais_seleccionado.split(" ")[1]
        except IndexError:
            self.view.mostrar_error("Error", "Selecciona un país válido.")
            return

        # 3. Delegar la validación y creación al MODELO
        exito, error_msg = self.model.registrar_usuario(
            nombre, apellidos, dni, fecha, email, telefono, prefijo, pass1
        )

        # 4. Decidir qué hacer según lo que responda el modelo
        if exito:
            self.view.mostrar_exito("Éxito", f"Cuenta bancaria creada para {nombre} {apellidos}.")
            self.view.controller.regresar_al_login()
        else:
            self.view.mostrar_error("Error", f"No se pudo crear el perfil: {error_msg}")

    def regresar(self):
        """Método para el botón cancelar/regresar"""
        self.view.controller.regresar_al_login()