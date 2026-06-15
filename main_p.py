
class MainPresenter:
    # Constructor que recibe inyectados a la Vista y al Modelo principales
    def __init__(self, view, model):
        # Almacenamos la vista en una propiedad local
        self.view = view
        # Almacenamos el modelo en una propiedad local
        self.model = model

        # Propiedad de estado que guarda la ruta física del archivo del usuario activo
        self.usuario_logueado = None
        # Propiedad que almacena el color de menú actual en memoria
        self.color_menu = "#2D033B"
        # Propiedad que almacena el color de los botones actual en memoria
        self.color_btn = "#482673"

    # Método de arranque que expone el login como pantalla de inicio
    def iniciar(self):
        # Mandamos a la vista la orden de renderizar el layout de acceso
        self.view.mostrar_login()

    # Método delegado para exponer la pantalla de registro
    def mostrar_registro(self):
        # Instruye a la vista a limpiar e invocar la pantalla de registro
        self.view.mostrar_registro()

    # Método delegado para regresar a la pantalla de login (usado por el botón cancelar del registro)
    def regresar_al_login(self):
        # Ejecuta la misma función que el arranque
        self.view.mostrar_login()

    # Método núcleo ejecutado cuando un usuario aprueba las credenciales
    def login_exitoso(self, ruta_archivo_usuario):
        # Actualizamos la variable de estado con la ruta validada del cliente
        self.usuario_logueado = ruta_archivo_usuario

        # Solicitamos al modelo que busque y extraiga los colores del perfil del archivo
        self.color_menu, self.color_btn = self.model.obtener_colores_tema(ruta_archivo_usuario)

        # Instruimos a la vista a construir el dashboard usando el color del menú recuperado
        self.view.construir_layout_principal(self.color_menu)
        # Instruimos a la vista a crear los botones laterales pasándole su color correspondiente
        self.view.crear_menu_botones(self.color_btn)
        # Instruimos a la vista a inicializar y cargar los frames de las secciones
        self.view.cargar_frames_internos()

        # Forzamos a la vista a levantar (mostrar) el frame de inicio "Home"
        self.mostrar_frame("Home")

    # Método para instruir a la vista a cambiar de sección
    def mostrar_frame(self, nombre):
        # Delegamos completamente la orden visual de cambio a la vista
        self.view.mostrar_frame(nombre)

    # Método gatillado cuando el usuario interactúa con la configuración de temas en la vista Cuenta
    def cambiar_color_global(self, fondo, boton):
        # Actualizamos las variables de estado en memoria local del presentador
        self.color_menu = fondo
        self.color_btn = boton

        # Ordenamos a la vista que cambie instantáneamente los colores de la interfaz
        self.view.aplicar_nuevos_colores(fondo, boton)

        # Invocamos al modelo para persistir (guardar) de forma permanente esta configuración
        self.model.guardar_colores_tema(self.usuario_logueado, fondo, boton)

    def ejecutar_cerrar_sesion(self):
        # Resetea el estado de sesión y ordena a la vista desmontar el dashboard.
        self.usuario_logueado = None
        if hasattr(self, "view") and self.view:
            self.view.cerrar_sesion_completo()

# ... (todo tu código anterior de main_p.py) ...

if __name__ == "__main__":
    # 1. Importamos la vista y el modelo principales
    from main_view import MainView
    from main_m import MainModel

    # 2. Creamos la ventana (Vista) y el administrador de archivos (Modelo)
    vista = MainView()
    modelo = MainModel()

    # 3. Creamos el Presentador inyectándole la vista y el modelo
    presentador = MainPresenter(view=vista, model=modelo)

    # 4. LE PASAMOS EL PRESENTADOR A LA VISTA (Paso crucial)
    vista.set_presenter(presentador)

    # 5. ¡AQUÍ ESTÁ EL TRUCO! Le decimos al presentador que pinte el Login
    presentador.iniciar()

    # 6. Arrancamos el bucle de Tkinter para que la ventana responda
    vista.mainloop()