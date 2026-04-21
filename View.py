import tkinter as tk


class FinanceView(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("Tracker Financiero - Personal")
        self.geometry("900x500")
        self.configure(bg="#121212")  # Gris oscuro de fondo principal

        self.presenter = None

        # --- ESTRUCTURA ---

        # Guardamos el color actual en una variable para poder actualizar los botones después
        self.color_menu_actual = "#2D033B"  # Morado inicial

        # 1. Menú Lateral
        self.menu_lateral = tk.Frame(self, bg=self.color_menu_actual, width=200, height=500)
        self.menu_lateral.pack(side="left", fill="y")
        self.menu_lateral.pack_propagate(False)

        # 2. Contenedor Principal
        self.contenedor_principal = tk.Frame(self, bg="#121212")
        self.contenedor_principal.pack(side="right", expand=True, fill="both")

        # Etiqueta de Menú
        self.lbl_menu_titulo = tk.Label(self.menu_lateral, text="MENÚ", font=("Arial", 14, "bold"),
                                        bg=self.color_menu_actual, fg="#FFFFFF", pady=20)
        self.lbl_menu_titulo.pack()

        # Lista para guardar las referencias de los botones y poder cambiarles el color
        self.botones_del_menu = []
        self.crear_botones_menu()

        self.cambiar_pantalla("Home")

    def crear_botones_menu(self):
        opciones = [
            ("Home", self.btn_home_click),
            ("Ahorros", self.btn_ahorros_click),
            ("Categorías", self.btn_categorias_click),
            ("Acciones", self.btn_acciones_click),
            ("Cuenta", self.btn_cuenta_click)
        ]

        for texto, comando in opciones:
            btn = tk.Button(self.menu_lateral, text=texto, font=("Arial", 11),
                            bg="#482673", fg="#FFFFFF", bd=0, padx=10, pady=15,
                            cursor="hand2", activebackground="#810CA8",
                            command=comando)
            btn.pack(fill="x", pady=2)
            self.botones_del_menu.append(btn)  # Guardamos el botón en la lista

    # --- MÉTODOS DE CAMBIO DE COLOR ---

    def actualizar_colores_interfaz(self, color_fondo, color_boton):
        """Cambia el color del menú y todos sus componentes"""
        self.color_menu_actual = color_fondo
        self.menu_lateral.configure(bg=color_fondo)
        self.lbl_menu_titulo.configure(bg=color_fondo)

        # Actualizamos cada botón del menú lateral
        for btn in self.botones_del_menu:
            btn.configure(bg=color_boton)

    # --- NAVEGACIÓN ---

    def btn_cuenta_click(self):
        self.cambiar_pantalla("Cuenta")

    def btn_home_click(self):
        self.cambiar_pantalla("Home")

    def btn_ahorros_click(self):
        self.cambiar_pantalla("Ahorros")

    def btn_categorias_click(self):
        self.cambiar_pantalla("Categorías")

    def btn_acciones_click(self):
        self.cambiar_pantalla("Acciones")

    def limpiar_contenedor(self):
        for widget in self.contenedor_principal.winfo_children():
            widget.destroy()

    def cambiar_pantalla(self, titulo_pantalla):
        self.limpiar_contenedor()

        lbl_titulo = tk.Label(self.contenedor_principal, text=titulo_pantalla,
                              font=("Arial", 24, "bold"), bg="#121212", fg="#FFFFFF")
        lbl_titulo.pack(pady=30)

        # SI LA PANTALLA ES "CUENTA", CREAMOS LOS BOTONES DE COLORES
        if titulo_pantalla == "Cuenta":
            lbl_instruccion = tk.Label(self.contenedor_principal, text="Selecciona un color para el menú:",
                                       bg="#121212", fg="#A0A0A0", font=("Arial", 12))
            lbl_instruccion.pack(pady=10)

            # Definimos los colores (Fondo del menú, Color del botón)
            colores = [
                ("Morado", "#2D033B", "#482673"),
                ("Azul", "#0D47A1", "#1976D2"),
                ("Naranja Oscuro", "#E65100", "#F57C00"),
                ("Amarillo Oscuro", "#F57F17", "#FBC02D"),
                ("Verde Selva", "#1B5E20", "#2E7D32")
            ]

            # Creamos un botón en el área principal por cada color
            for nombre, color_f, color_b in colores:
                btn_color = tk.Button(self.contenedor_principal, text=nombre, bg=color_f, fg="white",
                                      width=20, pady=10, font=("Arial", 10, "bold"),
                                      command=lambda f=color_f, b=color_b: self.actualizar_colores_interfaz(f, b))
                btn_color.pack(pady=5)
        else:
            lbl_info = tk.Label(self.contenedor_principal, text=f"Sección: {titulo_pantalla}",
                                bg="#121212", fg="#A0A0A0", font=("Arial", 12))
            lbl_info.pack(pady=10)


if __name__ == "__main__":
    app = FinanceView()
    app.mainloop()