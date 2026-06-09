import os  # Importación del módulo de sistema operativo para resolver y validar rutas físicas de archivos locales
import \
    yfinance as yf  # Librería externa encargada de conectar y descargar datos reales de mercados financieros globales
from datetime import \
    datetime  # Módulo encargado de gestionar el parsing de cadenas y manipulación estructural de fechas


class AccionesModel:  # Declaración de la clase del Modelo depositaria de las reglas matemáticas de datos de inversión
    def __init__(self):  # Constructor por defecto del componente del modelo de datos
        pass  # No requiere instanciar propiedades persistentes iniciales en este nivel estructural

    def calcular_portafolio(self, perfil_path, filtro_activo,
                            periodo_actual):  # Método nuclear que parsea el archivo e interactúa con el API remoto bursátil
        folder = os.path.dirname(
            perfil_path)  # Extrae el subdirectorio contenedor a partir del string de ruta de autenticación del usuario
        archivo_historial = os.path.join(folder,
                                         "historial_inversiones.txt")  # Resuelve el enlace del archivo que almacena el historial de compras
        transacciones = []  # Inicializa la matriz vacía que contendrá las estructuras limpias de órdenes de compra ejecutadas
        if os.path.exists(
                archivo_historial):  # Comprueba la presencia física real del documento contable dentro del almacenamiento local
            with open(archivo_historial, "r",
                      encoding="utf-8") as f:  # Abre el flujo del archivo en modo lectura segura bajo codificación UTF-8
                for linea in f:  # Itera secuencialmente línea por línea sobre el bloque completo del documento de texto
                    try:  # Bloque de aislamiento para procesar cada renglón mitigando cierres por líneas corruptas
                        if "COMPRA" in linea:  # Descarta los registros de auditoría conservando exclusivamente operaciones de compra
                            partes = linea.split(
                                "|")  # Fragmenta la cadena de texto utilizando el carácter delimitador pipe como separador
                            fecha_str = partes[0].split("]")[0].replace("[",
                                                                        "").strip()  # Extrae la cadena cronológica removiendo corchetes de control
                            fecha = datetime.strptime(fecha_str,
                                                      "%Y-%m-%d %H:%M:%S")  # Convierte el texto cronológico en un objeto nativo datetime
                            ticker = partes[1].split(":")[
                                1].strip()  # Extrae y limpia el código identificador bursátil asignado al activo adquirido
                            dinero_usado = float(partes[2].split(":")[1].strip().replace("€",
                                                                                         "").strip())  # Parsea el desembolso exacto en dinero a tipo flotante
                            acciones = float(partes[3].split(":")[1].strip().replace("+",
                                                                                     ""))  # Parsea el volumen de unidades adquiridas a tipo flotante
                            transacciones.append({"fecha": fecha, "ticker": ticker, "acciones": acciones,
                                                  "dinero_usado": dinero_usado})  # Guarda el diccionario de orden
                    except Exception as e:  # Intercepta cualquier excepción provocada por desalineación de campos en la lectura
                        print(
                            f"Error leyendo línea del historial: {e}")  # Envía un reporte del fallo de lectura a la consola del sistema
                        continue  # Prosigue el bucle for analizando de forma resiliente el resto de líneas del documento

        if not transacciones:  # Si tras procesar el archivo el pool de órdenes de compra se encuentra totalmente vacío
            return "VACIO"  # Devuelve un indicador de control en formato de cadena para instruir blanqueo en el presentador

        criptos_conocidas = ["BTC", "ETH", "DOGE", "ADA", "SOL",
                             "XRP"]  # Array que cataloga los identificadores clasificados como criptomonedas
        if filtro_activo == "Acciones":  # Si los criterios del usuario exigen la visualización exclusiva de renta variable tradicional
            transacciones = [t for t in transacciones if t[
                "ticker"] not in criptos_conocidas]  # Filtra removiendo todas las transacciones vinculadas a criptoactivos
        elif filtro_activo == "Cripto":  # Si la estrategia de visualización se enfoca únicamente en el ecosistema cripto descentralizado
            transacciones = [t for t in transacciones if t[
                "ticker"] in criptos_conocidas]  # Retiene únicamente las operaciones que concuerden con los tickers cripto

        if not transacciones:  # Valida si la matriz de órdenes quedó sin elementos disponibles tras aplicar los filtros de tipo de activo
            return None  # Retorna None para desactivar y limpiar los componentes gráficos de visualización del presentador

        tickers_unicos = list(set([t["ticker"] for t in
                                   transacciones]))  # Condensa una lista libre de duplicados de todos los instrumentos financieros poseídos
        tickers_yf = [f"{t}-EUR" if t in criptos_conocidas else t for t in
                      tickers_unicos]  # Adapta la nomenclatura añadiendo el sufijo EUR para cotizar en euros

        mapeo_tiempo = {
            # Diccionario indexador que asocia los horizontes del panel con las variables nativas requeridas por yfinance
            "1D": {"periodo": "1d", "intervalo": "2m"},
            # Datos del día de hoy distribuidos en muestras finas de dos minutos
            "1S": {"periodo": "5d", "intervalo": "5m"},
            # Rango comercial de cinco días laborables segmentado cada cinco minutos
            "1M": {"periodo": "1mo", "intervalo": "30m"},
            # Datos mensuales consolidados en bloques analíticos de treinta minutos
            "1A": {"periodo": "1y", "intervalo": "1d"},
            # Recorrido anual agrupado con base en cotizaciones de cierre de día completo
            "MAX": {"periodo": "max", "intervalo": "1d"}
            # Historial comercial total disponible unificado por cotizaciones diarias de cierre
        }
        config = mapeo_tiempo.get(periodo_actual, {"periodo": "1mo",
                                                   "intervalo": "1d"})  # Obtiene la matriz de configuración o aplica un fallback mensual

        try:  # Bloque de seguridad de comunicación remota para aislar peticiones HTTP externas al API de Yahoo Finance
            datos = yf.download(tickers_yf, period=config["periodo"], interval=config["intervalo"],
                                progress=False)  # Lanza la consulta y descarga masiva de cotizaciones
            if datos.empty: return None  # Aborta el procesamiento si el dataframe web carece de información estructurada explotable

            precios = datos[
                'Close'].ffill().bfill()  # Completa de forma perfecta huecos comerciales o cierres festivos arrastrando cotizaciones lógicas

            if hasattr(precios,
                       'to_frame'):  # Evalúa si la respuesta simplificada es una Serie lineal en lugar de una estructura bidimensional DataFrame
                precios = precios.to_frame(name=tickers_yf[
                    0])  # Convierte forzosamente la estructura unidimensional a DataFrame bautizando la columna con el ticker

            precios.index = precios.index.tz_localize(
                None)  # Remueve la codificación de zona horaria del índice de marcas para igualar cálculos nativos

            ahora = datetime.now()  # Captura una marca de tiempo con la hora exacta local para sincronizar las transacciones del día de hoy
            if ahora not in precios.index and periodo_actual in ["1D", "1S",
                                                                 "1M"]:  # Si el instante de hoy falta en la matriz intradía descargada
                precios.loc[ahora] = precios.iloc[
                    -1].copy()  # Acopla una fila temporal duplicando de forma segura los últimos valores de cierre disponibles
                precios = precios.sort_index()  # Reordena cronológicamente la matriz para resguardar la consistencia lineal del índice temporal

            fechas = precios.index  # Captura el índice temporal consolidado definitivo para usarlo como el eje horizontal cronológico
            valores = []  # Inicializa la lista que almacenará el valor económico total ponderado del portafolio por cada punto temporal
            es_grafico_diario = periodo_actual in ["1A",
                                                   "MAX"]  # Bandera discriminatoria para discernir lógica de calendario frente a horas exactas

            for fecha_merc in fechas:  # Bucle cronológico principal que avanza punto por punto sobre la cuadrícula temporal del mercado
                valor_momento = 0.0  # Resetea la tasación acumulada de riqueza para la marca de tiempo actualmente evaluada

                for i, ticker in enumerate(
                        tickers_unicos):  # Recorre la lista filtrada de activos individuales que integran el portafolio
                    ticker_yf = tickers_yf[
                        i]  # Recupera la nomenclatura homologada para yfinance asociada a la posición iterada

                    if es_grafico_diario:  # Si se está calculando un gráfico macro de largo plazo con granularidad de días naturales completos
                        acciones_acumuladas = sum([tr["acciones"] for tr in transacciones if
                                                   tr["ticker"] == ticker and tr[
                                                       "fecha"].date() <= fecha_merc.date()])  # Consolida la tenencia sumando unidades cuyas fechas de compra precedan o igualen al día bursátil
                    else:  # Si se está computando una trayectoria intradía sensible a minutos y horas exactas del reloj
                        acciones_acumuladas = sum([tr["acciones"] for tr in transacciones if
                                                   tr["ticker"] == ticker and tr[
                                                       "fecha"] <= fecha_merc])  # Suma las acciones adquiridas antes o en el instante preciso evaluado en el bucle

                    if acciones_acumuladas > 0:  # Si el balance de acciones del activo bursátil da un volumen positivo para este momento de la historia
                        precio_activo = float(precios[ticker_yf].loc[
                                                  fecha_merc])  # Extrae el precio de cotización unitario en esa marca de tiempo específica
                        valor_momento += acciones_acumuladas * precio_activo  # Calcula el peso patrimonial de la posición y lo inyecta al acumulador

                valores.append(
                    valor_momento)  # Inserta el valor patrimonial integrado calculado al vector de trayectoria lineal de riqueza

        except Exception as e:  # Captura fallos de desbordamiento, indexación o fallas críticas de red durante las operaciones matemáticas
            print(
                f"Error descargando portafolio real: {e}")  # Escribe el detalle exacto de la traza de error en la consola para depuración
            return None  # Retorna None dando por cancelado el procesamiento ante inestabilidad de los datos financieros

        valor_final = valores[
            -1] if valores else 0  # Establece la última muestra del vector calculado como la valuación patrimonial final actual
        coste_base = sum(tr["dinero_usado"] for tr in transacciones if tr.get(
            "dinero_usado") is not None)  # Consolida el desembolso total de dinero sumando los costos exactos leídos

        if coste_base == 0:  # Mecanismo de contingencia si el campo de dinero usado se encuentra ausente o nulo en el archivo histórico
            for tr in transacciones:  # Itera de forma individual a través de cada una de las órdenes de compra analizadas
                ticker_yf_tr = f"{tr['ticker']}-EUR" if tr['ticker'] in criptos_conocidas else tr[
                    'ticker']  # Determina el nombre adaptado para yfinance
                try:  # Bloque de seguridad por si la fecha del archivo de compra cae fuera de los límites de la matriz temporal descargada
                    idx_compra = precios.index.searchsorted(
                        tr["fecha"])  # Localiza la ranura de posición temporal más cercana a la compra en el mercado
                    idx_compra = min(idx_compra,
                                     len(precios) - 1)  # Asegura que la posición de aproximación no desborde las dimensiones físicas del array
                    precio_en_compra = float(precios[ticker_yf_tr].iloc[
                                                 idx_compra])  # Recupera la cotización estimada de mercado en el momento de compra
                    coste_base += tr[
                                      "acciones"] * precio_en_compra  # Estima el costo base multiplicando el volumen de activos por el precio de cotización recuperado
                except Exception:  # Ignora fallos individuales en el lazo de transacciones de contingencia
                    pass  # Continúa procesando las órdenes restantes del portafolio de manera elástica

        if coste_base == 0:  # Último recurso de contingencia matemática si los algoritmos de coste base previos arrojaron un saldo nulo
            primeros_no_cero = [v for v in valores if
                                v > 0]  # Filtra el vector de la gráfica aislando los primeros puntos con capitalización positiva
            coste_base = primeros_no_cero[
                0] if primeros_no_cero else valor_final  # Adopta el valor inicial del gráfico o iguala a la valoración final

        valor_inicial = coste_base  # Asigna definitivamente el coste base validado como el valor inicial consolidado de la inversión
        base_comparacion = valor_inicial if valor_inicial > 0 else (
                    valor_final * 0.99)  # Establece la línea de referencia técnica para evaluar plusvalías/minusvalías
        color_linea = "#2ecc71" if valor_final >= base_comparacion else "#ff4c4c"  # Elige verde si el balance es favorable o rojo si registra pérdidas

        num_ticks = 4  # Determina la cantidad máxima fija de marcas o divisiones cronológicas deseadas en el eje horizontal
        etiquetas_ticks = []  # Inicializa el vector encargado de almacenar las cadenas textuales de rotulado de fecha para el eje X
        indices_ticks = []  # Inicializa el vector de posiciones de índice numérico sobre el cual se estamparán las marcas X

        if len(valores) > 1:  # Verifica que la cantidad de puntos de datos sea suficiente para estructurar divisiones cronológicas visuales
            indices_ticks = [int(i * (len(valores) - 1) / (num_ticks - 1)) for i in
                             range(num_ticks)]  # Distribuye uniformemente los índices numéricos de las marcas

            if periodo_actual == "1D":  # Si la escala temporal comprende exclusivamente la sesión comercial de las últimas 24 horas
                etiquetas_ticks = [fechas[idx].strftime('%H:%M') for idx in
                                   indices_ticks]  # Traduce los índices temporales a texto detallando solo hora y minutos
            elif periodo_actual in ["1S",
                                    "1M"]:  # Si el portafolio evalúa tendencias de mediano plazo abarcando una semana o un mes entero
                etiquetas_ticks = [fechas[idx].strftime('%d %b') for idx in
                                   indices_ticks]  # Traduce los rótulos a texto exponiendo número de día y nombre corto de mes
            else:  # Para despliegues macro de largo plazo que evalúan la evolución patrimonial en años o histórico máximo
                etiquetas_ticks = [fechas[idx].strftime('%b %Y') for idx in
                                   indices_ticks]  # Estructura los nombres de las marcas mostrando el mes abreviado y año completo

        return valores, fechas, valor_final, valor_inicial, base_comparacion, color_linea, etiquetas_ticks, indices_ticks  # Devuelve la tupla completa empaquetada lista para el presentador