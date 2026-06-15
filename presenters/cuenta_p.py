# El Presentador es lógica pura: NO importa tkinter, messagebox ni os.
# La interfaz (popups, widgets) la maneja la Vista; el disco lo maneja el Modelo.

class CuentaPresenter:
    """Coordina la pantalla de configuración de cuenta entre Vista y Modelo."""

    def __init__(self, view, model):
        self.view = view
        self.model = model
        # El presentador mantiene la ruta del perfil activo (estado de negocio).
        self.archivo_actual = None
        # Registro cruzado de la dependencia.
        self.view.set_presenter(self)

    def cargar_datos_usuario(self):
        # Tomamos la ruta del usuario logueado desde el controlador global.
        self.archivo_actual = self.view.controller.usuario_logueado
        # El Modelo entrega un diccionario limpio; la Vista solo lo pinta.
        datos = self.model.obtener_datos_perfil(self.archivo_actual)
        self.view.poblar_campos(datos)

    def guardar_cambios(self):
        datos = self.view.obtener_datos_formulario()
        # Regla de negocio: el nombre es obligatorio.
        if not datos["nombre"]:
            self.view.mostrar_error("Error", "El nombre completo no puede estar vacío.")
            return
        try:
            # Conservamos la contraseña actual (no se toca al editar datos personales).
            contrasena_actual = self.model.obtener_contrasena_actual(self.archivo_actual)
            self.model.escribir_perfil_completo(
                self.archivo_actual,
                datos["nombre"], datos["dni"], datos["fecha"],
                datos["correo"], datos["telefono"], contrasena_actual,
                self.view.controller.color_menu, self.view.controller.color_btn,
            )
            # La persistencia del renombrado de carpeta la resuelve el Modelo.
            try:
                nueva_ruta = self.model.renombrar_carpeta_usuario(self.archivo_actual, datos["nombre"])
                self.archivo_actual = nueva_ruta
                self.view.controller.usuario_logueado = nueva_ruta
            except Exception as e:
                print(f"Error al renombrar la carpeta del usuario: {e}")

            self.view.mostrar_exito("Éxito", "Tus datos se han actualizado correctamente.")
        except Exception as e:
            self.view.mostrar_error("Error", f"No se pudieron guardar los cambios: {e}")

    def confirmar_cambio_password(self, pass_actual, pass_nueva, pass_repetir):
        """Valida el cambio de clave y devuelve (exito, titulo, mensaje).

        Recibe STRINGS (no widgets) y devuelve datos: la Vista se encarga de
        mostrar el diálogo y de cerrar la ventana modal si procede."""
        pass_actual = pass_actual.strip()
        pass_nueva = pass_nueva.strip()
        pass_repetir = pass_repetir.strip()

        if not pass_actual or not pass_nueva or not pass_repetir:
            return False, "Error", "Por favor, rellena las tres cajas de texto."

        contrasena_guardada = self.model.obtener_contrasena_actual(self.archivo_actual)
        if contrasena_guardada == "ERROR":
            return False, "Error", "No se pudo leer el perfil para verificar la contraseña."
        if pass_actual != contrasena_guardada:
            return False, "Error", "La contraseña actual es incorrecta."
        if pass_nueva != pass_repetir:
            return False, "Error", "La nueva contraseña y su repetición no coinciden."
        if pass_actual == pass_nueva:
            return False, "Error", "La nueva contraseña no puede ser igual a la actual."

        try:
            self.model.actualizar_contrasena(self.archivo_actual, pass_nueva)
            return True, "Éxito", "¡Contraseña actualizada correctamente!"
        except Exception as e:
            return False, "Error", f"No se pudo guardar la contraseña: {e}"
