from tkinter import messagebox


class GastosPresenter:
    def __init__(self, view, model):
        self.view = view
        self.model = model

    def obtener_subcategorias(self, categoria_principal):
        """Devuelve las subcategorías solicitadas de manera exacta"""
        mapeo = {
            "Gastos Fijos 📌": [
                "Vivienda (Hipoteca/Alquiler)",
                "Servicios (Seguros/Otros)",
                "Obligaciones Financieras Externas",
                "Transporte Público"
            ],
            "Gastos Variables 💸": [
                "Compras del Supermercado",
                "Ocio / Entretenimiento",
                "Cuidado Personal / Ropa",
                "Gastos Hormiga",
                "Suscripciones Streaming"
            ],
            "Gastos del Hogar 🏠": [
                "Servicios (Agua/Gas/Luz/Internet)",
                "Arreglos de la Casa",
                "Decoraciones y Muebles"
            ],
            "Gastos del Coche 🚗": [
                "Mantenimiento / Aceite",
                "Gasolina / Diésel / kWh",
                "Arreglos / Reparaciones"
            ]
        }
        return mapeo.get(categoria_principal, [])

    def ejecutar_gasto(self, categoria, subcategoria, cantidad_str):
        """Procesa y valida la transacción económica"""
        try:
            cantidad = float(cantidad_str)
            if cantidad <= 0:
                raise ValueError
        except ValueError:
            messagebox.showerror("Error", "Por favor, introduce una cantidad numérica válida y mayor a 0.")
            return

        # ⬇️ NUEVA LÓGICA DE CLASIFICACIÓN CORREGIDA ⬇️
        # Por defecto, asumimos que es Variable a menos que sea explícitamente un bloque fijo
        if categoria == "Gastos Fijos 📌":
            tipo_macro = "Fijo"
        elif categoria == "Gastos del Coche 🚗" and subcategoria != "Arreglos / Reparaciones":
            # El mantenimiento regular o el combustible del coche actúan como fijos/operativos,
            # pero si es "Arreglos / Reparaciones", saltará al 'else' como Variable.
            tipo_macro = "Fijo"
        else:
            tipo_macro = "Variable"

        # Recuperar la sesión del usuario a través del controlador global
        ruta_usuario = self.view.controller.usuario_logueado

        # Llamar al modelo para restar el dinero y validar saldo
        exito, mensaje = self.model.registrar_gasto_en_archivo(
            ruta_usuario, tipo_macro, categoria, subcategoria, cantidad
        )

        if exito:
            messagebox.showinfo("Éxito", mensaje)
            self.view.limpiar_formulario()
            self.inicializar_sesion()
        else:
            messagebox.showwarning("Advertencia", mensaje)

    def inicializar_sesion(self):
        ruta_usuario = self.view.controller.usuario_logueado

        # 1. Datos para informe y tablas
        totales, historial = self.model.obtener_informe_gastos(ruta_usuario)

        # 2. Saldo de cuenta (lo que hay para gastar)
        saldo_cuenta = self.model.obtener_saldo_cuenta(ruta_usuario)

        # 3. Ahorro acumulado (huchas/inversiones) para el gráfico
        ahorro_total = self.model.obtener_ahorro_total(ruta_usuario)

        # 4. Actualizar etiquetas
        self.view.actualizar_interfaz_informe(totales, historial)
        self.view.lbl_saldo_disponible.config(text=f"{saldo_cuenta:.2f} €")

        # 5. Generar/Actualizar Gráfico de Pastel
        # Pasamos: Fijos, Variables, Ahorros
        self.view.dibujar_grafico_pastel(totales["Fijos"], totales["Variables"], ahorro_total)