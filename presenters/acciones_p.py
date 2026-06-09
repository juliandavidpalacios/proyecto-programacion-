from datetime import datetime # Importa el módulo para gestionar la obtención e instanciación de marcas de tiempo del sistema
import tkinter as tk # Importa la librería gráfica básica para poder referenciar constantes globales de control interno

class AccionesPresenter: # Declaración estructural de la clase Presentador encargada de la lógica del flujo de control
    def __init__(self, view, model): # Constructor de enlace que recibe las instancias físicas de la vista y del modelo
        self.view = view # Almacena la referencia hacia el Frame de la interfaz gráfica de usuario (Vista)
        self.model = model # Almacena la referencia hacia el motor de cómputo y extracción bursátil (Modelo)
        self.modo_porcentaje = True # Inicializa el estado para discriminar la visualización de retornos: True para %, False para €
        self.periodo_actual = "1M" # Establece el alcance cronológico inicial por defecto de la aplicación a un mes
        self.filtro_activo = "Todo" # Inicializa la categoría sectorial base mostrando tanto acciones como criptoactivos
        self._job_refresco = None # Declara la propiedad contenedora destinada a retener el identificador del temporizador automático
        self.view.set_presenter(self) # Ejecuta la inyección bidireccional registrando este presentador dentro del objeto de la vista

    def cargar_datos_usuario(self): # Coordina las acciones necesarias para preparar el panel cuando entra en pantalla
        self.cambiar_filtro("Todo") # Fuerza un estado inicial de filtrado general para unificar las visualizaciones
        self.cambiar_periodo("1M") # Aplica por defecto la ventana temporal mensual al histórico inicial del portafolio
        self.iniciar_refresco() # Dispara el temporizador en bucle continuo para el auto-refresco en tiempo real del gráfico

    def iniciar_refresco(self): # Inicializa el planificador interno encargado de automatizar las llamadas asíncronas de red
        self.detener_refresco() # Invoca un saneamiento de seguridad cancelando cualquier temporizador huérfano previo
        self._job_refresco = self.view.after(5000, self._ciclo_refresco) # Programa una llamada diferida a los 5000ms reteniendo su ID de control

    def detener_refresco(self): # Desactiva de forma controlada el hilo de ejecución diferido provisto por Tkinter
        if self._job_refresco is not None: # Valida si la propiedad retiene una referencia activa de temporizador en memoria
            self.view.after_cancel(self._job_refresco) # Detiene la ejecución del temporizador de Tkinter usando el identificador registrado
            self._job_refresco = None # Blanquea la variable de control restaurándola a su estado inactivo de seguridad

    def _ciclo_refresco(self): # Callback automático recurrente que se ejecuta de forma cíclica cada 5 segundos
        self.generar_datos_y_graficar() # Ejecuta la reconstrucción completa de datos bursátiles y su renderizado en el lienzo
        self._job_refresco = self.view.after(5000, self._ciclo_refresco) # Reprograma de manera recursiva la llamada diferida para perpetuar el ciclo

    def toggle_variacion(self): # Alterna la métrica visual encargada de representar el rendimiento de las inversiones
        self.modo_porcentaje = not self.modo_porcentaje # Invierte el estado booleano de control de porcentaje frente a valor monetario bruto
        self.actualizar_textos_variacion() # Redibuja inmediatamente el texto de las métricas aplicando el nuevo formato

    def cambiar_periodo(self, periodo): # Modifica el alcance cronológico del gráfico respondiendo a la interacción del usuario
        self.periodo_actual = periodo # Actualiza el estado del periodo de tiempo retenido en el presentador
        self.view.actualizar_estilo_botones_tiempo() # Ordena a la vista repintar los botones temporales destacando la selección
        self.generar_datos_y_graficar() # Redibuja el gráfico descargando y proyectando el nuevo intervalo de mercado

    def cambiar_filtro(self, filtro): # Altera la segregación sectorial del portafolio basada en los clics del panel de control
        self.filtro_activo = filtro # Actualiza la categoría o etiqueta sectorial activa en el presentador
        self.view.actualizar_estilo_filtros() # Solicita a la vista sincronizar los estilos visuales de los botones de filtrado
        self.generar_datos_y_graficar() # Reconstruye la trayectoria histórica recalculando solo los activos del sector elegido

    def generar_datos_y_graficar(self): # Orquesta la extracción matemática del modelo y la renderización final sobre Matplotlib
        perfil_path = self.view.controller.usuario_logueado # Extrae la ruta de sesión activa del cliente mediante el objeto controlador
        resultado = self.model.calcular_portafolio(perfil_path, self.filtro_activo, self.periodo_actual) # Invoca el cálculo del modelo
        if resultado is None: # Si el modelo intercepta un estado de error, de datos nulos o fallo de red en la descarga
            self.view.lbl_total.config(text="0.00 €") # Reconfigura a cero el texto del saldo monetario de la interfaz
            self.view.ax.clear() # Remueve cualquier trazo o línea previa presente en los ejes de Matplotlib
            self.view.ax.grid(True, linestyle='--', alpha=0.1, color="white") # Dibuja la rejilla estandarizada de tono oscuro
            self.view.canvas.draw() # Ordena al lienzo actualizar y plasmar los cambios de borrado en la pantalla
            return # Aborta la continuación del flujo lógico del método de graficación
        if resultado == "VACIO": # Si el modelo dictamina que el archivo de transacciones carece por completo de datos válidos
            self.view.lbl_total.config(text="0.00 €") # Iguala a cero el marcador gráfico de balance financiero
            self.view.lbl_variacion.config(text="Sin inversiones", fg="#b3b3b3") # Imprime un aviso de texto neutro en la sección de fluctuación
            self.view.ax.clear() # Limpia los trazos gráficos remanentes en los ejes del plano bidimensional
            self.view.ax.grid(True, linestyle='--', alpha=0.1, color="white") # Proyecta de nuevo la cuadrícula estructural de la interfaz
            self.view.canvas.draw() # Sincroniza y redibuja la estructura vacía limpia sobre el widget físico de la aplicación
            return # Finaliza de forma segura la ejecución del método de actualización visual
        # Desempaqueta las variables de cálculo devueltas por el modelo conservando rigurosamente su nomenclatura
        valores, fechas, self.valor_final, self.valor_inicial, base_comparacion, color_linea, etiquetas_ticks, indices_ticks = resultado
        self.valores_grafico = valores # Almacena el vector de valoraciones históricas para habilitar la lectura interactiva del hover
        self.fechas_grafico = fechas # Almacena la serie temporal de índices cronológicos para el uso del cursor interactivo
        self.view.lbl_total.config(text=f"{self.valor_final:,.2f} €") # Formatea e inyecta la tasación final actual en la etiqueta de la vista
        self.actualizar_textos_variacion() # Calcula y actualiza la tasa matemática o monto real de ganancia/pérdida en pantalla
        self.view.ax.clear() # Blanquea los ejes antes de dibujar las nuevas trayectorias lineales calculadas
        self.view.ax.grid(True, linestyle='--', alpha=0.1, color="white") # Vuelve a estampar la rejilla de coordenadas semitransparente
        indices = list(range(len(valores))) # Convierte el rango secuencial de datos en una lista entera para el eje coordenado X
        self.view.ax.plot(indices, valores, color=color_linea, linewidth=2) # Traza la curva continua de evolución patrimonial del cliente
        min_y = min(valores) if min(valores) > 0 else 0 # Calcula la cota inferior del eje Y para ceñir el sombreado de Matplotlib
        self.view.ax.fill_between(indices, valores, min_y * 0.99, color=color_linea, alpha=0.1) # Rellena con un degradado sutil el área bajo la curva
        if len(valores) > 1: # Si la matriz temporal cuenta con los puntos mínimos requeridos para desplegar marcas cronológicas
            self.view.ax.set_xticks(indices_ticks) # Fija las marcas de posición horizontal sobre la regla del eje de Matplotlib
            self.view.ax.set_xticklabels(etiquetas_ticks) # Rotula con las cadenas de texto de fechas estructuradas los puntos fijados
        else: # Si el portafolio registra un único e histórico punto inicial o aislado de información comercial
            self.view.ax.set_xticks([]) # Desactiva las marcas de rotulado del eje para evitar encabalgamiento visual de datos
        self.view.linea_cursor = self.view.ax.axvline(x=0, color='white', alpha=0.4, linestyle='--', visible=False) # Inicializa la línea de trazos interactiva
        self.view.anotacion = self.view.ax.annotate("", xy=(0,0), xytext=(15, 15), textcoords="offset points", bbox=dict(boxstyle="round,pad=0.4", fc="#2b2b2b", ec="gray", lw=1), color="white", visible=False, fontfamily="Arial", fontsize=9) # Inicializa la caja flotante oculta
        if hasattr(self, "evento_hover"): # Evalúa si el objeto almacena un registro previo de escucha de eventos del ratón
            self.view.canvas.mpl_disconnect(self.evento_hover) # Desconecta el listener antiguo de Matplotlib previniendo la degradación de memoria
        self.evento_hover = self.view.canvas.mpl_connect("motion_notify_event", self.hover_grafico) # Conecta el movimiento del ratón con la función hover
        self.view.figura.autofmt_xdate() # Aplica la rotación angular automática a las fechas del eje horizontal de la figura
        self.view.canvas.draw() # Fuerza al lienzo gráfico a compilar y pintar en pantalla toda la estructura analítica montada

    def hover_grafico(self, event): # Gestiona de manera interactiva los movimientos del ratón del usuario sobre la rejilla lineal del gráfico
        if not hasattr(self, 'valores_grafico') or not self.valores_grafico: # Valida que existan vectores de datos activos y legibles en memoria
            return # Interrumpe el flujo si el cursor interactúa con un lienzo carente de información bursátil
        if event.inaxes == self.view.ax: # Comprueba si las coordenadas geográficas del ratón caen dentro del marco de los ejes válidos del gráfico
            x_idx = int(round(event.xdata)) # Captura el índice entero flotante del eje X aproximándolo al valor entero más cercano
            if 0 <= x_idx < len(self.valores_grafico): # Valida que el índice resuelto se encuentre dentro de los límites físicos del vector
                precio_hover = self.valores_grafico[x_idx] # Extrae el valor patrimonial exacto asociado al índice temporal seleccionado
                fecha_hover = self.fechas_grafico[x_idx] # Recupera el objeto fecha y hora exacto correspondiente a la muestra espacial
                if self.periodo_actual == "1D": # Si el entorno de análisis visual se limita a las fluctuaciones de un único día de mercado
                    fecha_str = fecha_hover.strftime('%H:%M') # Formatea el string flotante del hover aislando únicamente la hora y el minuto
                elif self.periodo_actual in ["1S", "1M"]: # Si el horizonte gráfico comprende balances semanales o mensuales consolidados
                    fecha_str = fecha_hover.strftime('%d %b - %H:%M') # Estructura el texto indicando el número de día, mes abreviado, hora y minuto
                else: # Para estrategias históricas extensas a largo plazo que operan sobre cierres diarios acumulados
                    fecha_str = fecha_hover.strftime('%d %b %Y') # Compone el texto visual mostrando el día del calendario, mes abreviado y año completo
                texto = f"{fecha_str}\n{precio_hover:,.2f} €" # Sincroniza la cadena de texto final multilínea incorporando el valor monetario
                self.view.anotacion.set_text(texto) # Aplica la nueva cadena de texto al elemento gráfico interactivo de la vista
                self.view.anotacion.xy = (x_idx, precio_hover) # Desplaza la ancla espacial de la caja informativa al punto exacto sobre la curva
                if x_idx > len(self.valores_grafico) * 0.7: # Si la posición horizontal del ratón invade el último tramo derecho del panel gráfico
                    self.view.anotacion.set_position((-80, 15)) # Desplaza el cuadro informativo hacia la izquierda impidiendo que sea cortado por el borde
                else: # Si el cursor opera libremente sobre el tramo inicial o central de la pantalla gráfica
                    self.view.anotacion.set_position((15, 15)) # Desplaza el cuadro a la derecha manteniendo el espaciado por defecto respecto al puntero
                self.view.linea_cursor.set_xdata([x_idx, x_idx]) # Modifica las coordenadas horizontales de la línea vertical guía para enfocar el índice
                self.view.linea_cursor.set_visible(True) # Hace visible sobre el plano coordenado la línea guía vertical
                self.view.anotacion.set_visible(True) # Modifica la propiedad de visualización de la caja emergente a activa
                self.view.lbl_total.config(text=f"{precio_hover:,.2f} €") # Sincroniza el balance de la cabecera mostrando la cotización del punto enfocado
                self.view.canvas.draw_idle() # Solicita un refresco diferido atenuado de la interfaz gráfica optimizando el uso de CPU
        else: # Si el cursor del ratón abandona los límites geométricos de los ejes cartesianos del gráfico de Matplotlib
            if hasattr(self.view, 'linea_cursor') and self.view.linea_cursor.get_visible(): # Comprueba si los componentes interactivos siguen expuestos
                self.view.linea_cursor.set_visible(False) # Oculta la línea guía vertical del plano cartesiano de la vista
                self.view.anotacion.set_visible(False) # Desactiva de la vista la visualización del cuadro de texto flotante informativo
                precio_actual_real = float(self.valores_grafico[-1]) # Extrae el último elemento del vector que representa el balance actual genuino
                self.view.lbl_total.config(text=f"{precio_actual_real:,.2f} €") # Restaura el valor patrimonial actual exacto en la etiqueta principal de cabecera
                self.view.canvas.draw_idle() # Genera una orden diferida de redibujado de bajo impacto en el procesador del sistema

    def actualizar_textos_variacion(self): # Gestiona el cómputo matemático de rendimiento y actualiza las propiedades cromáticas y textuales de la vista
        if not hasattr(self, 'valor_inicial'): return # Aborta el proceso si el cálculo base no ha determinado aún la inversión inicial base
        diferencia = self.valor_final - self.valor_inicial # Calcula la diferencia neta absoluta restando el costo base de la tasación actual
        porcentaje = (diferencia / self.valor_inicial) * 100 if self.valor_inicial != 0 else 0 # Calcula el rendimiento porcentual protegiendo divisiones por cero
        color = "#2ecc71" if diferencia >= 0 else "#ff4c4c" # Asigna verde hexadecimal ante ganancias o rojo hexadecimal ante saldos negativos
        signo = "+" if diferencia >= 0 else "" # Determina el prefijo matemático aditivo para dar un formato contable natural
        if self.modo_porcentaje: # Evalúa si el presentador se encuentra configurado para inyectar métricas relativas porcentuales
            texto = f"{signo}{porcentaje:.2f}%" # Compone la cadena de texto aplicando el formato porcentual de dos decimales fijados
        else: # Si el esquema de visualización exige la representación monetaria absoluta de la fluctuación
            texto = f"{signo}{diferencia:,.2f} €" # Crea el string asociando el símbolo de euro y formateando separadores de miles
        self.view.lbl_variacion.config(text=texto, fg=color) # Modifica simultáneamente el texto y el color del widget en la interfaz gráfica