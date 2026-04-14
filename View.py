import tkinter as tk  # Importamos la librería estándar para interfaces gráficas
from tkinter import messagebox  # Importamos el módulo para mostrar alertas o mensajes


# Definimos la clase de la Vista que hereda de tk.Tk
class FinanceView(tk.Tk):
    def __init__(self):
        super().__init__()  # Inicializamos la clase padre tk.Tk

        # Configuración básica de la ventana
        self.title("Tracker Financiero - Personal")  # Título de la aplicación
        self.geometry("900x500")  # Tamaño de la ventana (ancho x alto)
        self.configure(bg="#f0f0f0")  # Color de fondo gris claro

        # Atributo para guardar la referencia al Presenter
        self.presenter = None

        # --- ESTRUCTURA DE LA PANTALLA ---

        # 1. Menú Lateral (Panel Izquierdo)
        self.menu_lateral = tk.Frame(self, bg="#2c3e50", width=200, height=500)
        self.menu_lateral.pack(side="left", fill="y")  # Se fija a la izquierda y ocupa todo el alto
        self.menu_lateral.pack_propagate(False)  # Evita que el frame cambie de tamaño según los botones

        # 2. Contenedor Principal (Panel Derecho)
        # Aquí se "dibujarán" las pantallas al presionar los botones
        self.contenedor_principal = tk.Frame(self, bg="white")
        self.contenedor_principal.pack(side="right", expand=True, fill="both")

        # Texto de encabezado en el menú
        tk.Label(self.menu_lateral, text="MENÚ", font=("Arial", 14, "bold"),
                 bg="#2c3e50", fg="white", pady=20).pack()

        # Llamamos a la función que crea los 5 botones
        self.crear_botones_menu()

        # Mostrar la pantalla "Home" por defecto al abrir el programa
        self.cambiar_pantalla("Home")

    def crear_botones_menu(self):
        """Crea los botones con los nuevos nombres solicitados"""
        # Lista de tuplas: (Nombre visual, Función a ejecutar)
        opciones = [
            ("Home", self.btn_home_click),
            ("Ahorros", self.btn_ahorros_click),
            ("Categorías", self.btn_categorias_click),
            ("Acciones", self.btn_acciones_click),
            ("Cuenta", self.btn_cuenta_click)
        ]

        # Ciclo para crear cada botón con el mismo estilo
        for texto, comando in opciones:
            btn = tk.Button(self.menu_lateral, text=texto, font=("Arial", 11),
                            bg="#34495e", fg="white", bd=0, padx=10, pady=15,
                            cursor="hand2", activebackground="#1abc9c",
                            command=comando)
            btn.pack(fill="x", pady=2)  # fill="x" hace que el botón ocupe todo el ancho del menú

    # --- MÉTODOS DE EVENTO (Interacción con el usuario) ---

    def btn_home_click(self):
        self.cambiar_pantalla("Home")  # Cambia la vista a Home
        if self.presenter:
            self.presenter.al_seleccionar_home()  # Notifica al presentador

    def btn_ahorros_click(self):
        self.cambiar_pantalla("Ahorros")  # Cambia la vista a Ahorros
        if self.presenter:
            self.presenter.al_seleccionar_ahorros()

    def btn_categorias_click(self):
        self.cambiar_pantalla("Categorías")  # Cambia la vista a Categorías
        if self.presenter:
            self.presenter.al_seleccionar_categorias()

    def btn_acciones_click(self):
        self.cambiar_pantalla("Acciones")  # Cambia la vista a Acciones
        if self.presenter:
            self.presenter.al_seleccionar_acciones()

    def btn_cuenta_click(self):
        self.cambiar_pantalla("Cuenta")  # Cambia la vista a Cuenta
        if self.presenter:
            self.presenter.al_seleccionar_cuenta()

    # --- LÓGICA DE INTERFAZ ---

    def limpiar_contenedor(self):
        """Elimina los elementos de la pantalla anterior para dejar el espacio en blanco"""
        for widget in self.contenedor_principal.winfo_children():
            widget.destroy()

    def cambiar_pantalla(self, titulo_pantalla):
        """Actualiza el panel derecho con el título de la opción seleccionada"""
        self.limpiar_contenedor()  # Borra lo que había antes

        # Crea el título principal en el panel derecho
        lbl_titulo = tk.Label(self.contenedor_principal, text=titulo_pantalla,
                              font=("Arial", 20, "bold"), bg="white", fg="#2c3e50")
        lbl_titulo.pack(pady=20)

        # Texto informativo de relleno
        lbl_info = tk.Label(self.contenedor_principal,
                            text=f"Bienvenido a la sección: {titulo_pantalla}",
                            bg="white", font=("Arial", 12))
        lbl_info.pack(pady=10)


# Ejecución de prueba
if __name__ == "__main__":
    app = FinanceView()
    app.mainloop()