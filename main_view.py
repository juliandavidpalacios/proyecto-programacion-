import tkinter as tk
from screens.home import HomeFrame
from screens.ahorros import AhorrosFrame
from screens.acciones import AccionesFrame
from screens.cuenta import CuentaFrame
from screens.login import LoginView
from screens.registro import RegistroView
from screens.invertir import InvertirView


# Definimos la clase MainView que hereda las propiedades de una ventana principal tk.Tk
class MainView(tk.Tk):
    # Constructor de la ventana gráfica
    def __init__(self):
        # Iniciamos el constructor padre de la ventana Tkinter
        super().__init__()
        # Definimos el título corporativo de la barra superior de la ventana
        self.title("Tracker Financiero Modular - Banco Digital")

        # Neutralizamos el escalado por DPI de Windows (125 % / 150 %), que es lo
        # que hacía que los widgets se renderizaran gigantes y se salieran de la
        # pantalla. 96/72 = 1.333 reproduce una pantalla estándar al 100 %, que es
        # el tamaño para el que se diseñó la interfaz.
        try:
            self.tk.call("tk", "scaling", 96.0 / 72.0)
        except Exception:
            pass

        # Ventana redimensionable (ya NO bloqueada con maxsize) que arranca
        # maximizada para aprovechar toda la pantalla disponible.
        self.geometry("1280x720")
        self.minsize(1024, 640)
        self.resizable(True, True)
        try:
            self.state("zoomed")  # En Windows: abre la ventana maximizada.
        except Exception:
            pass

        # Configuramos el color de fondo oscuro global de la ventana
        self.configure(bg="#121212")

        # Diccionario que almacenará las instancias de todos los frames principales
        self.frames = {}
        # Lista que guardará las referencias de los botones del menú lateral
        self.botones_lista = []
        # Inicializamos la variable del presentador en vacío
        self.presenter = None

        # Instanciamos el frame principal exclusivo para los módulos de Auth (Login/Registro)
        self.contenedor_auth = tk.Frame(self, bg="#121212")
        # Empaquetamos este contenedor llenando todo el espacio disponible
        self.contenedor_auth.pack(fill="both", expand=True)

    # Método para inyectar el controlador (presentador) en la vista
    def set_presenter(self, presenter):
        # Guardamos la referencia del presentador en la propiedad interna
        self.presenter = presenter

    # Método para limpiar visualmente todo el contenedor de autenticación
    def limpiar_auth(self):
        # Iteramos por cada elemento hijo dibujado dentro del contenedor_auth
        for widget in self.contenedor_auth.winfo_children():
            # Destruimos (eliminamos de memoria y pantalla) el widget actual
            widget.destroy()

    # Método visual para renderizar la pantalla de login
    def mostrar_login(self):
        self.limpiar_auth()

        # Importamos el modelo y presentador específicos del Login
        from Models.login_m import LoginModel
        from presenters.login_p import LoginPresenter

        # 1. Instanciamos su propio modelo
        modelo_login = LoginModel()

        # 2. Instanciamos la Vista (buscando tu archivo login.py)
        self.frame_login = LoginView(parent=self.contenedor_auth, controller=self.presenter)

        # 3. Instanciamos su Presentador conectando la vista recién creada y su modelo
        presentador_login = LoginPresenter(view=self.frame_login, model=modelo_login)

        # 4. Le inyectamos el presentador a la vista de login para que dibuje los botones
        self.frame_login.set_presenter(presentador_login)

        # 5. La mostramos en pantalla
        self.frame_login.pack(fill="both", expand=True)
        if hasattr(self, "contenedor_principal") and self.contenedor_principal:
            # Intentamos con pack_forget o grid_forget según cómo los hayas montado
            try:
                self.contenedor_principal.pack_forget()
            except Exception:
                self.contenedor_principal.grid_forget()

        if hasattr(self, "menu_lateral") and self.menu_lateral:
            try:
                self.menu_lateral.pack_forget()
            except Exception:
                self.menu_lateral.grid_forget()

            # 2. HACEMOS VISIBLE EL LOGIN: Volvemos a empaquetar el contenedor de autenticación
        if hasattr(self, "contenedor_auth") and self.contenedor_auth:
            # Lo volvemos a mostrar en pantalla ocupando todo el espacio disponible
            self.contenedor_auth.pack(fill="both", expand=True)

            # Forzamos a Tkinter a redibujar y actualizar la ventana inmediatamente
            self.update_idletasks()

    # Método visual para renderizar la pantalla de registro
    def mostrar_registro(self):
        # Limpiamos el contenedor gráfico de autenticación
        self.limpiar_auth()

        # IMPORTACIONES CORRECTAS BASADAS EN TU ESTRUCTURA:
        # Importamos el Modelo desde la carpeta Models
        from Models.registro_m import RegistroModel
        # Importamos el Presentador desde la carpeta presenters
        from presenters.registro_p import RegistroPresenter
        # Importamos la Vista desde la carpeta screens
        from screens.registro import RegistroView

        # 1. Instanciamos el modelo de datos encargado del registro
        modelo_registro = RegistroModel()

        # 2. Instanciamos la vista de registro mapeando sus contenedores de interfaz
        self.frame_registro = RegistroView(parent=self.contenedor_auth, controller=self.presenter)

        # 3. Instanciamos su presentador cruzando las referencias del módulo de registro
        presentador_registro = RegistroPresenter(view=self.frame_registro, model=modelo_registro)

        # 4. Establecemos la conexión de vuelta inyectando el presentador a la vista
        self.frame_registro.set_presenter(presentador_registro)

        # 5. Desplegamos el frame de registro ocupando todo el espacio disponible
        self.frame_registro.pack(fill="both", expand=True)

    # Método para construir el esqueleto general de la app una vez logueado
    def construir_layout_principal(self, color_menu):
        # Ocultamos el contenedor de login/registro (sin destruirlo por completo)
        self.contenedor_auth.pack_forget()

        # Instanciamos el panel lateral usando el color personalizado recuperado
        self.menu_lateral = tk.Frame(self, bg=color_menu, width=200, height=500)
        # Empaquetamos el menú alineándolo a la izquierda y rellenando el eje Y
        self.menu_lateral.pack(side="left", fill="y")
        # Desactivamos la propagación para que el ancho de 200px se respete rígidamente
        self.menu_lateral.pack_propagate(False)

        # Instanciamos el contenedor derecho donde vivirán las pantallas principales
        self.contenedor_principal = tk.Frame(self, bg="#121212")
        # Lo empaquetamos a la derecha permitiéndole expandirse y llenar el resto de la ventana
        self.contenedor_principal.pack(side="right", expand=True, fill="both")

    # Método visual que dibuja e inserta los botones en el panel lateral
    def crear_menu_botones(self, color_btn):
        # Definimos tu arreglo de opciones originales para los botones
        opciones = ["Home", "Ahorros", "Acciones", "Cuenta","Expertos"]
        # Limpiamos la lista de botones por seguridad
        self.botones_lista = []
        # Iteramos sobre los textos de las opciones
        for texto in opciones:
            # Creamos el botón, vinculándolo al presentador usando un comando lambda
            btn = tk.Button(self.menu_lateral, text=texto, bg=color_btn, fg="white",
                            font=("Arial", 11), bd=0, pady=15, cursor="hand2",
                            command=lambda t=texto: self.presenter.mostrar_frame(t))
            # Empaquetamos el botón llenando el ancho del panel lateral
            btn.pack(fill="x", pady=2)
            # Añadimos el objeto botón a la lista para futuras modificaciones (cambios de color)
            self.botones_lista.append(btn)

    # Método encargado de inicializar todos los frames operativos en memoria
    def cargar_frames_internos(self):
        # Importamos todas las clases de Vistas desde la carpeta screens
        from screens.home import HomeFrame
        from screens.ahorros import AhorrosFrame
        from screens.acciones import AccionesFrame
        from screens.cuenta import CuentaFrame
        from screens.invertir import InvertirView
        from screens.expertos import ExpertosFrame

        # Mapeamos cada Vista con su respectivo Modelo y Presentador
        # Esto le permite al bucle saber exactamente qué piezas conectar para cada sección
        config_modulos = {
            "Home": {
                "vista_clase": HomeFrame,
                "import_modelo": lambda: __import__("Models.home_m", fromlist=["HomeModel"]).HomeModel,
                "import_presenter": lambda: __import__("presenters.home_p", fromlist=["HomePresenter"]).HomePresenter
            },
            "Ahorros": {
                "vista_clase": AhorrosFrame,
                "import_modelo": lambda: __import__("Models.ahorros_m", fromlist=["AhorrosModel"]).AhorrosModel,
                "import_presenter": lambda: __import__("presenters.ahorros_p",
                                                       fromlist=["AhorrosPresenter"]).AhorrosPresenter
            },
            "Acciones": {
                "vista_clase": AccionesFrame,
                "import_modelo": lambda: __import__("Models.acciones_m", fromlist=["AccionesModel"]).AccionesModel,
                "import_presenter": lambda: __import__("presenters.acciones_p",
                                                       fromlist=["AccionesPresenter"]).AccionesPresenter
            },
            "Invertir": {
                "vista_clase": InvertirView,
                "import_modelo": lambda: __import__("Models.invertir_m", fromlist=["InvertirModel"]).InvertirModel,
                "import_presenter": lambda: __import__("presenters.invertir_p",
                                                       fromlist=["InvertirPresenter"]).InvertirPresenter
            },
            "Cuenta": {
                "vista_clase": CuentaFrame,
                "import_modelo": lambda: __import__("Models.cuenta_m", fromlist=["CuentaModel"]).CuentaModel,
                "import_presenter": lambda: __import__("presenters.cuenta_p",
                                                       fromlist=["CuentaPresenter"]).CuentaPresenter
            },
            "Expertos": {
                "vista_clase": ExpertosFrame,
                "import_modelo": lambda: __import__("Models.expertos_m", fromlist=["ExpertosModel"]).ExpertosModel,
                "import_presenter": lambda: __import__("presenters.expertos_p", fromlist=["ExpertosPresenter"]).ExpertosPresenter
            }
        }

        # Iteramos sobre nuestra configuración para armar el engranaje MVP de cada pantalla
        for nombre_clave, componentes in config_modulos.items():
            # 1. Instanciamos la Vista pasando el contenedor y el presentador global (controller)
            F = componentes["vista_clase"]
            frame = F(parent=self.contenedor_principal, controller=self.presenter)

            try:
                # 2. Cargamos dinámicamente el Modelo y el Presentador de esta pantalla
                ModeloClase = componentes["import_modelo"]()
                PresenterClase = componentes["import_presenter"]()

                modelo_instancia = ModeloClase()
                # 3. Creamos el presentador secundario cruzando la vista actual y su modelo
                presentador_instancia = PresenterClase(view=frame, model=modelo_instancia)

                # 4. LE INYECTAMOS EL PRESENTADOR A LA VISTA (Esto resuelve el error del NoneType)
                if hasattr(frame, "set_presenter"):
                    frame.set_presenter(presentador_instancia)
                else:
                    # Si tu archivo original no usa set_presenter pero guarda la variable directa:
                    frame.presenter = presentador_instancia

            except Exception as e:
                print(f"Nota: No se pudo enlazar el MVP completo para {nombre_clave}: {e}")
                print("Se usará la configuración base del frame.")

            # Guardamos el frame listo en el diccionario de la app
            self.frames[nombre_clave] = frame
            frame.grid(row=0, column=0, sticky="nsew")

    # Método para elevar y mostrar una pantalla específica dentro del contenedor principal
    def mostrar_frame(self, nombre):
        # Extraemos la pantalla solicitada del diccionario de frames
        frame = self.frames[nombre]
        # Elevamos visualmente ese frame sobre todos los demás (Z-Index en Tkinter)
        frame.tkraise()
        # Si la pantalla cuenta con el método interno de recarga de datos, lo invocamos
        if hasattr(frame, "cargar_datos_usuario"):
            # Ejecutamos la recarga de datos para refrescar la vista
            frame.cargar_datos_usuario()

    # Método que desmonta por completo el dashboard y vuelve a la pantalla de login.
    # Antes esta lógica vivía (mezclada con messagebox) en el HomePresenter, lo que
    # violaba MVP. Ahora la destrucción de widgets es responsabilidad de la Vista.
    def cerrar_sesion_completo(self):
        # Detenemos el refresco asíncrono de la pantalla de Acciones si está activo.
        if "Acciones" in self.frames:
            acciones_frame = self.frames["Acciones"]
            if hasattr(acciones_frame, "detener_refresco"):
                acciones_frame.detener_refresco()

        # Destruimos todos los frames de la sesión y vaciamos el registro.
        for frame in self.frames.values():
            frame.destroy()
        self.frames = {}

        # Eliminamos el menú lateral y el contenedor principal del dashboard.
        if hasattr(self, "menu_lateral") and self.menu_lateral:
            self.menu_lateral.destroy()
        if hasattr(self, "contenedor_principal") and self.contenedor_principal:
            self.contenedor_principal.destroy()

        # Reconstruimos un contenedor de autenticación limpio y mostramos el login.
        self.contenedor_auth = tk.Frame(self, bg="#121212")
        self.contenedor_auth.pack(fill="both", expand=True)
        self.mostrar_login()

    # Método para aplicar dinámicamente un cambio estético general
    def aplicar_nuevos_colores(self, fondo, boton):
        # Verificamos si la interfaz ya cuenta con el menú lateral construido
        if hasattr(self, 'menu_lateral'):
            # Alteramos su propiedad de color de fondo (background)
            self.menu_lateral.config(bg=fondo)

        # Verificamos si la lista de botones ya está instanciada
        if hasattr(self, 'botones_lista'):
            # Recorremos cada botón dibujado
            for btn in self.botones_lista:
                # Alteramos su color de fondo individualmente
                btn.config(bg=boton)