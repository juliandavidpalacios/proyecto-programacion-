import os
import tkinter as tk
# Importamos el módulo de alertas e interfaces emergentes estándar de tkinter
from tkinter import messagebox
# Importamos la clase datetime para capturar e imprimir marcas de tiempo reales en los logs
from datetime import datetime



# Definimos la clase InvertirPresenter que coordinará la comunicación entre el modelo y la vista
class InvertirPresenter:
    # Constructor que inicializa el presentador enlazando las instancias del modelo y la vista de la app
    def __init__(self, view, model):
        # Guarda la instancia de la vista para poder actualizar sus componentes de interfaz
        self.view = view
        # Guarda la instancia del modelo para acceder a las funciones lógicas de datos y ficheros
        self.model = model

        # Inicializa el lapso temporal de visualización por defecto a 1 Mes
        self.periodo_actual = "1M"
        # Inicializa la variable de estado del activo seleccionado en vacío
        self.activo_seleccionado = None
        # Inicializa la propiedad que define la categoría activa del explorador en vacío
        self.categoria_seleccionada = None
        # Crea la variable para almacenar la colección de precios numéricos cargados en la gráfica
        self.valores_grafico = None
        # Crea la variable para retener la lista de objetos de fecha emparejados con los precios
        self.fechas_grafico = None
        # Inicializa la propiedad para almacenar la referencia visual de la línea vertical del cursor
        self.linea_cursor = None
        # Inicializa la propiedad para almacenar la referencia visual del cartel informativo flotante
        self.anotacion = None
        # Inicializa el ID del evento de escucha del movimiento del puntero del ratón en vacío
        self.evento_hover = None

    # Método de utilidad para que la vista conozca las llaves de activos cargadas en el modelo
    def obtener_activos_por_categoria(self, categoria):
        # Retorna las claves primarias (tickers) contenidas bajo la categoría solicitada
        return self.model.base_datos[categoria].keys()

    # Método de utilidad para extraer el precio base configurado en la base de datos simulada
    def obtener_precio_inicial(self, categoria, ticker):
        # Accede al diccionario interno del modelo y extrae el precio preestablecido
        return self.model.base_datos[categoria][ticker]["precio"]

    # Método invocado al presionar el botón lateral de cualquier activo del explorador
    def seleccionar_activo(self, categoria, ticker):
        # Clona la estructura de datos del activo del modelo y la guarda en el estado local del presentador
        self.activo_seleccionado = self.model.base_datos[categoria][ticker].copy()
        # Inyecta de forma explícita el ticker de mercado dentro del diccionario clonado para uso futuro
        self.activo_seleccionado['ticker'] = ticker
        # Almacena el nombre de la categoría del mercado a la que pertenece el activo seleccionado
        self.categoria_seleccionada = categoria

        # Actualiza el texto de la cabecera en la vista combinando el nombre corporativo y el ticker
        self.view.lbl_nombre_activo.config(text=f"{self.activo_seleccionado['nombre']} ({ticker})")
        # Actualiza la etiqueta de precio aplicando formateo de millares y dos posiciones decimales
        self.view.lbl_precio_activo.config(text=f"{self.activo_seleccionado['precio']:,.2f} €")
        # Modifica el texto del sector mostrando la industria de procedencia del activo financiero
        self.view.lbl_sector.config(text=f"Sector: {self.activo_seleccionado['sector']}")
        # Reemplaza el texto instructivo del mensaje por la descripción de negocio del activo real
        self.view.txt_resumen.config(text=self.activo_seleccionado['resumen'])

        # Ejecuta la lógica de actualización del período forzando la recarga del gráfico a un Mes ("1M")
        self.cambiar_periodo("1M")

    # Método encargado de gestionar la conmutación de los rangos de tiempo del gráfico interactivo
    def cambiar_periodo(self, periodo):
        # Si el usuario intenta alternar el tiempo sin haber seleccionado un activo previamente
        if not self.activo_seleccionado:
            # Lanza una ventana flotante de advertencia notificando que debe elegir un activo primero
            messagebox.showwarning("Aviso", "Por favor, selecciona un activo de la lista primero.")
            # Interrumpe la ejecución del método de forma prematura
            return

        # Actualiza el estado del parámetro del rango temporal con el nuevo valor escogido
        self.periodo_actual = periodo

        # Determina de forma dinámica el color de realce consultando propiedades del controlador de la vista
        color_activo = self.view.controller.color_btn if hasattr(self.view.controller, 'color_btn') else "#482673"
        # Recorre todos los botones físicos de tiempo almacenados en la vista
        for p, btn in self.view.botones_tiempo.items():
            # Si el botón evaluado coincide exactamente con el rango seleccionado por el usuario
            if p == periodo:
                # Modifica el diseño visual del botón dándole el color destacado para denotar selección
                btn.config(bg=color_activo, fg="white")
            # Si el botón corresponde a los rangos temporales inactivos
            else:
                # Restaura el color grisáceo opaco original del botón apagado
                btn.config(bg="#333333", fg="white")

        # Lanza de forma inmediata la rutina matemática para descargar y dibujar el gráfico modificado
        self.generar_grafico_activo()

    # Método de alta complejidad destinado al procesamiento y dibujo de los históricos del mercado financiero
    def generar_grafico_activo(self):
        # Valida la existencia de un activo cargado para blindar la ejecución ante fallos imprevistos
        if not self.activo_seleccionado:
            # Aborta la función si no hay ninguna acción o criptomoneda activa
            return

        # Extrae el código identificador (ticker) de la inversión seleccionada actualmente
        ticker = self.activo_seleccionado['ticker']

        # Aplica una regla condicional para concatenar el sufijo "-EUR" requerido exclusivamente por Yahoo en Crypto
        ticker_real = f"{ticker}-EUR" if self.categoria_seleccionada == "Cripto" else ticker

        # Diccionario de mapeo técnico que empareja los botones visuales con las constantes de la API financiera
        mapeo_tiempo = {
            "1D": {"periodo": "1d", "intervalo": "2m"},
            "1S": {"periodo": "5d", "intervalo": "5m"},
            "1M": {"periodo": "1mo", "intervalo": "30m"},
            "1A": {"periodo": "1y", "intervalo": "1h"},
            "MAX": {"periodo": "max", "intervalo": "1d"}
        }

        # Extrae los parámetros de rango de datos e intervalos de consulta según la selección del usuario
        config = mapeo_tiempo.get(self.periodo_actual, {"periodo": "1mo", "intervalo": "1d"})

        try:
            # Invoca al método del modelo para descargar el DataFrame histórico oficial desde Yahoo Finance
            datos = self.model.obtener_datos_api(ticker_real, config["periodo"], config["intervalo"])

            # Si el DataFrame devuelto por la API carece por completo de registros o filas útiles
            if datos.empty:
                # Muestra un cartel de error informando que el mercado no dispone de información para ese activo
                messagebox.showerror("Error", f"No se encontraron datos en tiempo real para {ticker_real}")
                # Frena el algoritmo para impedir roturas de código al graficar vectores vacíos
                return

            # Elimina las zonas horarias asociadas al índice temporal para evitar desajustes de formato de fecha
            datos.index = datos.index.tz_localize(None)
            # Guarda la serie temporal de fechas en una variable dedicada del algoritmo
            fechas = datos.index
            # Extrae los valores numéricos correspondientes a la columna de precios de cierre del activo
            valores = datos['Close'].values

            # Captura el último precio cotizado al final del vector extraído de los mercados
            precio_real_actual = float(valores[-1])
            # Actualiza el widget de precio grande en la vista mostrando el valor monetario real e instantáneo
            self.view.lbl_precio_activo.config(text=f"{precio_real_actual:,.2f} €")

        # Captura errores de red, fallos de DNS o bloqueos por falta de conexión a Internet
        except Exception as e:
            # Despliega una alerta de error en la pantalla detallando el fallo de comunicación surgido
            messagebox.showerror("Error", f"Error de conexión con el mercado: {e}")
            # Aborta la ejecución de la función de dibujado
            return

        # Limpia de forma exhaustiva los ejes coordenados de la vista eliminando curvas anteriores
        self.view.ax.clear()
        # Habilita la rejilla de fondo configurando líneas discontinuas, opacidad baja y color blanco
        self.view.ax.grid(True, linestyle='--', alpha=0.1, color="white")

        # Evalúa si la cotización ha subido o bajado respecto al inicio para definir color verde o rojo
        color_linea = "#2ecc71" if valores[-1] >= valores[0] else "#ff4c4c"

        # Genera una lista correlativa secuencial que servirá de eje X ficticio eludiendo huecos de fin de semana
        indices = list(range(len(valores)))
        # Traza la línea continua de cotización sobre el lienzo con el color definido y grosor de 2 puntos
        self.view.ax.plot(indices, valores, color=color_linea, linewidth=2)
        # Rellena el espacio comprendido debajo de la curva aplicando una transparencia del 10% para dar estética moderna
        self.view.ax.fill_between(indices, valores, min(valores) * 0.99, color=color_linea, alpha=0.1)

        # Establece de forma rígida una distribución de 4 marcas fijas en el eje horizontal
        num_ticks = 4
        # Calcula geométricamente los índices exactos para ubicar los 4 textos de manera equidistante
        indices_ticks = [int(i * (len(valores) - 1) / (num_ticks - 1)) for i in range(num_ticks)]

        # Si el marco temporal de análisis está configurado para reflejar las cotizaciones de un solo Día
        if self.periodo_actual == "1D":
            # Formatea las etiquetas de tiempo abstrayendo exclusivamente las Horas y Minutos
            etiquetas_ticks = [fechas[idx].strftime('%H:%M') for idx in indices_ticks]
        # Si el marco temporal abarca los rangos de 1 Semana o 1 Mes de negociación
        elif self.periodo_actual in ["1S", "1M"]:
            # Formatea las etiquetas aislando el número del día y las siglas del mes de operaciones
            etiquetas_ticks = [fechas[idx].strftime('%d %b') for idx in indices_ticks]
        # Para rangos extendidos como 1 Año o el histórico Máximo registrado
        else:
            # Formatea las marcas proyectando el mes de forma abreviada acoplado al año de cotización
            etiquetas_ticks = [fechas[idx].strftime('%b %Y') for idx in indices_ticks]

        # Inyecta los puntos numéricos de anclaje calculados en el eje X del gráfico matemático
        self.view.ax.set_xticks(indices_ticks)
        # Sobrescribe los índices numéricos por las cadenas de texto legibles de fechas formateadas
        self.view.ax.set_xticklabels(etiquetas_ticks)

        # Almacena en las propiedades del presentador los vectores de cotización para que el lector los procese
        self.valores_grafico = valores
        # Almacena de igual forma el listado nativo de fechas para la lectura interactiva del hover
        self.fechas_grafico = fechas

        # Dibuja la línea discontinua vertical del cursor fijándola inicialmente en la coordenada cero oculta
        self.linea_cursor = self.view.ax.axvline(x=0, color='white', alpha=0.4, linestyle='--', visible=False)

        # Instancia la caja de texto flotante (Annotate) parametrizando colores oscuros, bordes y fuentes tipográficas
        self.anotacion = self.view.ax.annotate(
            "", xy=(0, 0), xytext=(15, 15),
            textcoords="offset points",
            bbox=dict(boxstyle="round,pad=0.4", fc="#2b2b2b", ec="gray", lw=1),
            color="white", visible=False, fontfamily="Arial", fontsize=9
        )

        # Si ya existía un evento de detección del ratón previamente enlazado al lienzo gráfico
        if self.evento_hover is not None:
            # Desconecta de forma limpia el evento antiguo para prevenir duplicaciones de memoria y consumo de CPU
            self.view.canvas.mpl_disconnect(self.evento_hover)
        # Registra el nuevo detector vinculando la acción de mover el ratón con el método hover_grafico
        self.evento_hover = self.view.canvas.mpl_connect("motion_notify_event", self.hover_grafico)

        # Aplica una rotación automatizada y acomodo estético a las fechas impresas en el eje X
        self.view.figura.autofmt_xdate()
        # Fuerza el redibujado final de los lienzos para reflejar todos los cambios visuales sobre la pantalla
        self.view.canvas.draw()

    # Método desencadenado de forma continua cada vez que el puntero del ratón sobrevuela el gráfico activo
    def hover_grafico(self, event):
        # Valida la integridad de las variables de series numéricas antes de procesar coordenadas del ratón
        if self.valores_grafico is None:
            # Si no hay datos analíticos en memoria rompe la ejecución del manejador del hover
            return

        # Evalúa si la posición actual del puntero del ratón se halla confinada dentro de los ejes coordenados
        if event.inaxes == self.view.ax:
            # Redondea y convierte a entero la coordenada flotante X del ratón obteniendo el índice más cercano
            x_idx = int(round(event.xdata))

            # Verifica rigurosamente que el índice estimado no sobrepase los límites reales del vector
            if 0 <= x_idx < len(self.valores_grafico):
                # Extrae el precio de cierre correspondiente al índice detectado por el ratón
                precio_hover = self.valores_grafico[x_idx]
                # Extrae la estampa de fecha emparejada con ese precio histórico
                fecha_hover = self.fechas_grafico[x_idx]

                # Aplica formateo específico de fecha para el cartel flotante si es periodo de 1 Día
                if self.periodo_actual == "1D":
                    # Almacena el texto procesado solo con horas y minutos
                    fecha_str = fecha_hover.strftime('%H:%M')
                # Si el periodo se corresponde con 1 Semana o 1 Mes de negociación activa
                elif self.periodo_actual in ["1S", "1M"]:
                    # Formatea la cadena incorporando fecha del día, mes corto y la hora exacta de la muestra
                    fecha_str = fecha_hover.strftime('%d %b - %H:%M')
                # Para periodos de largo alcance anuales o históricos extendidos
                else:
                    # Compone la cadena mostrando el día del mes, texto del mes y el año de cuatro dígitos
                    fecha_str = fecha_hover.strftime('%d %b %Y')

                # Estructura el mensaje final combinando la fecha procesada y el precio formateado con dos decimales
                texto = f"{fecha_str}\n{precio_hover:,.2f} €"
                # Modifica el contenido de texto interno de la caja informativa flotante
                self.anotacion.set_text(texto)
                # Reposiciona los vectores cartesianos de la caja flotante apuntando al punto matemático exacto
                self.anotacion.xy = (x_idx, precio_hover)

                # Si el cursor se ubica en el último 30% del gráfico (extremo derecho)
                if x_idx > len(self.valores_grafico) * 0.7:
                    # Desplaza la caja flotante a la izquierda de forma artificial para evitar que se corte del borde
                    self.anotacion.set_position((-80, 15))
                # Si el cursor transita por la zona centro o izquierda del gráfico
                else:
                    # Mantiene la posición estándar del cartel desplazada hacia la derecha del puntero
                    self.anotacion.set_position((15, 15))

                # Actualiza la coordenada X de la línea vertical punteada moviéndola al paso del ratón
                self.linea_cursor.set_xdata([x_idx, x_idx])

                # Fuerza la visibilidad de la línea vertical del cursor interactivo
                self.linea_cursor.set_visible(True)
                # Hace visible el cartel flotante informativo sobre los ejes del lienzo
                self.anotacion.set_visible(True)

                # Actualiza en tiempo real la etiqueta gigante superior reflejando el precio exacto bajo el cursor
                self.view.lbl_precio_activo.config(text=f"{precio_hover:,.2f} €")

                # Ordena un refresco pasivo optimizado (draw_idle) consumiendo menos potencia de procesamiento
                self.view.canvas.draw_idle()
        # Si el usuario desplaza el puntero fuera de los márgenes limitantes del gráfico matemático
        else:
            # Comprueba si los elementos interactivos se encuentran visibles actualmente en el lienzo
            if self.linea_cursor and self.linea_cursor.get_visible():
                # Oculta de inmediato la línea vertical punteada del cursor
                self.linea_cursor.set_visible(False)
                # Esconde el cartel de anotación flotante del gráfico
                self.anotacion.set_visible(False)

                # Rescata el valor de cierre real definitivo de la serie histórica actual
                precio_actual_real = float(self.valores_grafico[-1])
                # Restablece la etiqueta gigante superior de la vista devolviéndole su cotización de mercado real
                self.view.lbl_precio_activo.config(text=f"{precio_actual_real:,.2f} €")

                # Solicita la recarga asíncrona optimizada del lienzo gráfico de matplotlib
                self.view.canvas.draw_idle()

    # Método centralizado gatillado al pulsar el botón verde de ejecución de compra de activos
    def ejecutar_compra(self):
        # Valida que exista un activo financiero seleccionado en la aplicación para proceder
        if not self.activo_seleccionado:
            # Informa mediante cuadro de diálogo que falta seleccionar un elemento del explorador
            messagebox.showerror("Error", "Primero debes seleccionar un activo del explorador.")
            # Cancela el procesamiento comercial
            return

        # Verifica la integridad de la sesión del usuario a través de la propiedad del controlador general
        if not self.view.controller.usuario_logueado:
            # Lanza una alerta de error avisando que no existe un usuario activo autenticado en el sistema
            messagebox.showerror("Error", "No se ha detectado ningún usuario activo.")
            # Interrumpe la operación de compra
            return

        # Extrae la cadena de caracteres digitada por el usuario en la caja de texto de inversión
        cantidad_str = self.view.entry_inversion.get().strip()
        try:
            # Transforma el texto de entrada a un valor numérico decimal de precisión flotante
            cantidad = float(cantidad_str)
            # Si el importe monetario ingresado es igual o menor a cero euros
            if cantidad <= 0:
                # Dispara un error genérico de valor para forzar el salto al bloque de captura de excepciones
                raise ValueError
        # Atrapa los errores de casteo tipográfico o valores inválidos/negativos introducidos
        except ValueError:
            # Despliega una notificación de error exigiendo un formato numérico estrictamente positivo
            messagebox.showerror("Error", "Introduce una cantidad de dinero válida y mayor a 0 €.")
            # Frena el algoritmo comercial
            return

        # Interroga al modelo para calcular el saldo de la hucha pasándole el usuario logueado actual
        saldo_ahorros, archivo_ahorros = self.model.calcular_saldo_ahorros(self.view.controller.usuario_logueado)

        # Evalúa si el costo pretendido de la inversión supera los fondos monetarios retenidos en la hucha
        if cantidad > saldo_ahorros:
            # Lanza un cuadro modal de error detallando la carencia de fondos financieros para procesar el trade
            messagebox.showerror(
                "Fondos Insuficientes",
                f"No tienes suficiente dinero en tu hucha de ahorros.\n\n"
                f"Saldo actual en Ahorros: {saldo_ahorros:,.2f} €\n"
                f"Costo de la inversión: {cantidad:,.2f} €"
            )
            # Finaliza la ejecución del método de adquisición
            return

        # Si el presentador posee un volcado de cotizaciones vivas cargado en su memoria gráfica
        if self.valores_grafico is not None and len(self.valores_grafico) > 0:
            # Captura el precio exacto instantáneo del último cierre descargado en el gráfico
            precio_actual = float(self.valores_grafico[-1])
        # Si el gráfico aún no se ha inicializado o carece de registros históricos en tiempo real
        else:
            # Adopta de forma estática el precio de catálogo base definido en el diccionario simulado
            precio_actual = float(self.activo_seleccionado['precio'])

        # Extrae el identificador bursátil (ticker) asignado al activo objeto de la transacción
        ticker = self.activo_seleccionado['ticker']
        # Estima matemáticamente el volumen fraccionado de acciones adquiridas dividiendo capital entre precio
        acciones_adquiridas = cantidad / precio_actual

        # Consulta al modelo para cargar el mapa actual de inventario y la ubicación del archivo del portafolio
        portafolio, archivo_portafolio = self.model.leer_portafolio_activos(self.view.controller.usuario_logueado)
        # Recupera las unidades previas acumuladas de ese activo específico (retorna 0.0 si es nuevo)
        acciones_previas = portafolio.get(ticker, 0.0)
        # Consolida el inventario incrementando de forma aditiva la nueva fracción de acciones compradas
        portafolio[ticker] = acciones_previas + acciones_adquiridas

        try:
            # Abre el archivo general de ahorros en modo append ("a") para añadir la operación de retiro sin borrar nada
            with open(archivo_ahorros, "a", encoding="utf-8") as f:
                # Escribe la línea registrando la detracción de capital asignada a la categoría de inversiones
                f.write(f"Retiro,Inversiones ({ticker}),{cantidad:.2f}\n")
        # Captura fallos de hardware o restricciones del sistema al escribir sobre el archivo de ahorros
        except Exception as e:
            # Muestra el error crítico impidiendo que la acción avance si no se puede asentar el cobro base
            messagebox.showerror("Error", f"No se pudo asentar el cobro en tus Ahorros: {e}")
            # Detiene por completo la función comercial
            return

        # Ordena al modelo persistir y escribir los balances actualizados de activos dentro de su archivo txt
        self.model.guardar_portafolio_activos(archivo_portafolio, portafolio)

        # Extrae el archivo de perfil del usuario a fin de deducir el directorio de guardado del log histórico
        perfil_path = self.view.controller.usuario_logueado
        # Extrae el directorio base contenedor del archivo de perfil actual
        folder = os.path.dirname(perfil_path)
        # Resuelve la ubicación del archivo histórico detallado de movimientos bursátiles
        archivo_historial = os.path.join(folder, "historial_inversiones.txt")

        # Registra la fecha y hora precisa del reloj del sistema formateada con horas, minutos y segundos
        fecha_hora_actual = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        try:
            # Abre el log de auditoría de transacciones bursátiles en modo append ("a")
            with open(archivo_historial, "a", encoding="utf-8") as f:
                # Escribe una entrada legible y estructurada con todos los metadatos analíticos del trade ejecutado
                f.write(
                    f"[{fecha_hora_actual}] COMPRA | Activo: {ticker} | Dinero usado: {cantidad:.2f} € | Acciones obtenidas: +{acciones_adquiridas:.6f} | Precio de mercado: {precio_actual:.2f} €\n")
        # Atrapa excepciones de bajo nivel de IO sin congelar la experiencia del usuario de la app
        except Exception as e:
            # Imprime el detalle del error de forma silenciosa sobre la consola de desarrollo
            print(f"Error al guardar el historial detallado: {e}")

        # Calcula de forma matemática el remanente de saldo resultante para proyectarlo en el cuadro modal de éxito
        nuevo_saldo_simulado = saldo_ahorros - cantidad
        # Proyecta una interfaz emergente informativa anunciando la correcta ejecución del trade bursátil
        messagebox.showinfo(
            "¡Compra Realizada con Éxito!",
            f"El importe ha sido retirado de tu hucha general de ahorros.\n\n"
            f"🏢 Activo comprado: {ticker} ({self.activo_seleccionado['nombre']})\n"
            f"🛒 Fracciones adquiridas: +{acciones_adquiridas:.6f}\n"
            f"📉 Precio de mercado: {precio_actual:,.2f} €\n"
            f"💸 Fondos retirados de Ahorros: -{cantidad:,.2f} €\n"
            f"----------------------------------------\n"
            f"💰 Nuevo Saldo en Ahorros: {nuevo_saldo_simulado:,.2f} €\n"
            f"📊 Inventario total de {ticker}: {portafolio[ticker]:.6f} unidades"
        )

        # Borra de punta a punta el texto ingresado en la caja de entrada para dejar listo el formulario
        self.view.entry_inversion.delete(0, tk.END)