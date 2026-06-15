# El Presentador es Python puro: NO importa tkinter ni messagebox.
# Solo coordina la Vista (a través de métodos limpios) y el Modelo.

class AhorrosPresenter:
    # Constructor que asocia las instancias de la vista y el modelo con el presentador.
    def __init__(self, view, model):
        self.view = view
        self.model = model
        # Estado de negocio que el presentador mantiene en memoria (no lo lee de un widget).
        self.total_ahorrado = 0.0
        # Canal de comunicación: la vista podrá pedirle cosas al presentador.
        self.view.set_presenter(self)

    # Coordina el flujo de arranque de datos del usuario extrayendo variables del controlador.
    def inicializar_sesion(self):
        perfil_txt = self.view.controller.usuario_logueado
        if not perfil_txt:
            return
        self.model.establecer_ruta_usuario(perfil_txt)
        self.actualizar_interfaz()

    # Procesa la lógica de negocio y ordena a la vista cómo redibujarse (sin tocar widgets).
    def actualizar_interfaz(self):
        self.view.limpiar_tabla()

        lineas = self.model.leer_lineas_ahorros()
        try:
            # Renderizado de filas (de la más nueva a la más antigua).
            for linea in reversed(lineas):
                linea = linea.strip()
                if not linea:
                    continue
                partes = linea.split(",")
                if len(partes) == 3:
                    tipo, cat, cant_str = partes
                    cantidad = float(cant_str)
                    signo = "+" if tipo == "Ingreso" else "-"
                    # Le pasamos a la vista datos YA formateados; ella solo los pinta.
                    self.view.agregar_fila_historial(tipo, cat, f"{signo} {cantidad:.2f} €")

            # Los totales los calcula el MODELO con una CuentaBancaria de dominio.
            total_ahorrado, aportado_mes = self.model.calcular_resumen(lineas)
            # Guardamos el total en el presentador (fuente de verdad para validar retiros).
            self.total_ahorrado = total_ahorrado
            self.view.actualizar_totales(f"{total_ahorrado:.2f} €", f"{aportado_mes:.2f} €")

            # Avisamos a la vista que estamos consultando el mercado (operación lenta).
            self.view.mostrar_inversiones_cargando()
            self.view.refrescar()

            total_invertido = self.model.obtener_valor_portafolio()
            self.view.actualizar_inversiones(f"{total_invertido:.2f} €")
        except Exception as e:
            print(f"Error cargando el historial de ahorros/acciones: {e}")

    # Gestiona el registro de un nuevo movimiento de ingreso o egreso.
    def ejecutar_movimiento(self, tipo):
        cant_texto = self.view.obtener_cantidad().strip()
        categoria = self.view.obtener_categoria()
        if not cant_texto:
            self.view.mostrar_error("Error", "Por favor, introduce una cantidad numérica.")
            return
        try:
            cantidad = float(cant_texto)
            if cantidad <= 0:
                raise ValueError
        except ValueError:
            self.view.mostrar_error("Error", "La cantidad debe ser un número válido y mayor que cero.")
            return

        # Regla de negocio: no se puede retirar más de lo ahorrado.
        if tipo == "Retiro" and cantidad > self.total_ahorrado:
            self.view.mostrar_error(
                "Fondos Insuficientes",
                f"No puedes retirar {cantidad:.2f} € porque tu saldo de ahorro actual "
                f"es de {self.total_ahorrado:.2f} €.",
            )
            return

        try:
            self.model.guardar_movimiento(tipo, categoria, cantidad)
            self.view.limpiar_cantidad()
            self.actualizar_interfaz()
            self.view.mostrar_exito("Éxito", f"¡{tipo} de {cantidad:.2f} € registrado correctamente!")
        except Exception as e:
            self.view.mostrar_error("Error", f"No se pudo guardar la operación: {e}")
