from tkinter import messagebox
import tkinter as tk

class AhorrosPresenter:
    # Constructor que asocia las instancias físicas de la vista y el modelo con el presentador
    def __init__(self, view, model):
        # Guarda la referencia a la clase que dibuja los elementos de interfaz gráfica (Vista)
        self.view = view
        # Guarda la referencia a la clase que manipula la persistencia e integraciones (Modelo)
        self.model = model
        # Genera un canal de comunicación bidireccional inyectando este objeto en la propia vista
        self.view.set_presenter(self)

    # Coordina el flujo de arranque de datos del usuario extrayendo variables del controlador
    def inicializar_sesion(self):
        # Lee la propiedad de texto de identificación guardada en el controlador de la ventana principal
        perfil_txt = self.view.controller.usuario_logueado
        # Si la cadena del perfil se encuentra vacía o el usuario no está autenticado, detiene el flujo
        if not perfil_txt:
            # Termina la ejecución del método de forma prematura al no haber sesión válida
            return
        # Llama al modelo para verificar o crear los archivos de almacenamiento según la ruta del perfil
        self.model.establecer_ruta_usuario(perfil_txt)
        # Invoca la rutina de sincronización para actualizar los datos visibles en la pantalla
        self.actualizar_interfaz()

    # Procesa la lógica de negocio requerida para refrescar y redibujar métricas e historiales
    def actualizar_interfaz(self):
        # Borra todos los renglones y registros presentes actualmente en la cuadrícula Treeview
        for item in self.view.tabla.get_children():
            # Remueve de forma individual cada identificador del nodo de la tabla gráfica
            self.view.tabla.delete(item)
        # Declara la variable para computar la suma algebraica total de los ahorros guardados
        total_ahorrado = 0.0
        # Declara el acumulador específico encargado de medir los ingresos financieros mensuales
        aportado_mes = 0.0
        # Invoca al modelo para recuperar las líneas crudas escritas en el archivo de texto
        lineas = self.model.leer_lineas_ahorros()
        # Bloque de captura preventiva contra fallas lógicas o de conversión de tipos de datos
        try:
            # Recorre el listado de transacciones obtenidas de manera invertida (de la más nueva a la más antigua)
            for linea in reversed(lineas):
                # Remueve del fragmento de texto caracteres de control ocultos y saltos de línea
                linea = linea.strip()
                # Salta de inmediato las líneas que se encuentren totalmente vacías
                if not linea: continue
                # Descompone el registro de texto plano en una lista dividiéndolo por comas
                partes = linea.split(",")
                # Confirma si la estructura del registro cumple con las 3 variables obligatorias definidas
                if len(partes) == 3:
                    # Desempaqueta la lista asignando los valores a variables individuales claras
                    tipo, cat, cant_str = partes
                    # Transforma la cadena de caracteres del monto en un valor numérico de punto flotante
                    cantidad = float(cant_str)
                    # Elige el símbolo matemático en función de la naturaleza de la transacción ejecutada
                    signo = "+" if tipo == "Ingreso" else "-"
                    # Envía los datos ordenados a la vista para renderizarlos en una nueva fila de la tabla
                    self.view.tabla.insert("", "end", values=(tipo, cat, f"{signo} {cantidad:.2f} €"))
                    # Si el movimiento es de entrada, adiciona los montos a los saldos totales y mensuales
                    if tipo == "Ingreso":
                        # Suma el valor procesado al balance histórico general de ahorros
                        total_ahorrado += cantidad
                        # Incrementa el indicador de inyecciones financieras mensuales directas
                        aportado_mes += cantidad
                    # En caso de tratarse de un retiro de capital, resta el valor del balance global
                    else:
                        # Deduce el dinero retirado del acumulador histórico total
                        total_ahorrado -= cantidad
            # Actualiza el componente de texto de la vista para reflejar el saldo histórico total formateado
            self.view.lbl_total.config(text=f"{total_ahorrado:.2f} €")
            # Actualiza la etiqueta mensual de la vista inyectando la cifra con su formato de moneda
            self.view.lbl_mes.config(text=f"{aportado_mes:.2f} €")
            # Configura de forma provisional un estado de espera en la tarjeta de activos en red
            self.view.lbl_inversiones.config(text="Cargando...")
            # Fuerza a Tkinter a redibujar la interfaz de forma inmediata antes de la llamada de red bloqueante
            self.view.update_idletasks()
            # Ordena al modelo contactar con Yahoo Finance para evaluar el portafolio en tiempo real
            total_invertido = self.model.obtener_valor_portafolio()
            # Envía a la vista el resultado final en euros obtenido del cálculo de las inversiones
            self.view.lbl_inversiones.config(text=f"{total_invertido:.2f} €")
        # Captura excepciones generalizadas durante la sincronización o formateo de los datos del panel
        except Exception as e:
            # Genera un reporte escrito del fallo en la salida del sistema de depuración
            print(f"Error cargando el historial de ahorros/acciones: {e}")

    # Método que gestiona el flujo para registrar un nuevo movimiento de ingreso o egreso financiero
    def ejecutar_movimiento(self, tipo):
        # Captura el texto ingresado por el usuario en el campo numérico eliminando espacios vacíos
        cant_texto = self.view.entry_cantidad.get().strip()
        # Captura la opción textual de la categoría seleccionada en el menú desplegable del formulario
        categoria = self.view.combo_categoria.get()
        # Valida si la entrada de texto de la cantidad se encuentra totalmente vacía
        if not cant_texto:
            # Despliega una ventana emergente de error advirtiendo la omisión del parámetro numérico
            messagebox.showerror("Error", "Por favor, introduce una cantidad numérica.")
            # Cancela de forma inmediata la ejecución de la rutina de guardado
            return
        try:
            # Intenta convertir el texto extraído del formulario a un formato decimal analizable
            cantidad = float(cant_texto)
            # Lanza una excepción lógica controlada si el valor es negativo o igual a cero
            if cantidad <= 0:
                # Dispara el error para desviar el flujo hacia el bloque de manejo de excepciones
                raise ValueError
        # Captura fallos si el formato del texto no es convertible o viola los mínimos requeridos
        except ValueError:
            # Muestra un aviso de error informando que se requiere un valor numérico superior a cero
            messagebox.showerror("Error", "La cantidad debe ser un número válido y mayor que cero.")
            # Interrumpe y detiene la ejecución del proceso de registro de movimientos
            return
        # Evalúa reglas de control financiero específicas si la transacción implica retirar dinero
        if tipo == "Retiro":
            # Extrae la cifra de saldo actual expuesta en la etiqueta transformándola a formato flotante
            total_actual = float(self.view.lbl_total.cget("text").replace(" €", ""))
            # Si el monto que se intenta retirar supera los fondos disponibles del cliente, deniega el proceso
            if cantidad > total_actual:
                # Lanza un modal de alerta bloqueante reportando la insuficiencia de fondos líquidos
                messagebox.showerror("Fondos Insuficientes", f"No puedes retirar {cantidad:.2f} € porque tu saldo de ahorro actual es de {total_actual:.2f} €.")
                # Aborta el guardado para evitar saldos negativos inconsistentes
                return
        try:
            # Envía la orden y los parámetros validados al modelo para escribir la línea en el archivo
            self.model.guardar_movimiento(tipo, categoria, cantidad)
            # Limpia por completo la caja de texto del campo numérico en la interfaz gráfica
            self.view.entry_cantidad.delete(0, tk.END)
            # Invoca de forma recursiva la actualización visual total para reflejar el cambio en la tabla
            self.actualizar_interfaz()
            # Muestra al usuario un aviso informativo de éxito confirmando el registro de la transacción
            messagebox.showinfo("Éxito", f"¡{tipo} de {cantidad:.2f} € registrado correctamente!")
        # Captura excepciones críticas relativas a fallos de permisos o de escritura física en disco
        except Exception as e:
            # Notifica el error al usuario mediante una ventana emergente con la traza técnica resumida
            messagebox.showerror("Error", f"No se pudo guardar la operación: {e}")
