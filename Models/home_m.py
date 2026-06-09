# Importamos la librería os para interactuar con el sistema de archivos del sistema operativo
import os
# Importamos datetime para manejar formatos de fechas y tiempos del sistema
from datetime import datetime
# Importamos la librería yfinance para descargar información financiera y precios desde Yahoo Finance
import yfinance as yf
# Importamos pandas para dar formato y manipular la estructura de datos tabulares (DataFrames) de yfinance
import pandas as pd


# Definimos la clase del Modelo encargada exclusivamente de la gestión, lectura y procesamiento de los datos
class HomeModel:

    # Método para leer el nombre completo del usuario desde su archivo de perfil
    def leer_nombre(self, perfil_path):
        try:
            # Abrimos el archivo de perfil en modo lectura con codificación UTF-8
            with open(perfil_path, "r", encoding="utf-8") as f:
                # Iteramos línea por línea sobre el archivo de perfil
                for linea in f:
                    # Si la línea actual inicia con la etiqueta "Nombre Completo:"
                    if linea.startswith("Nombre Completo:"):
                        # Dividimos la línea por los dos puntos, tomamos la segunda parte y eliminamos espacios en blanco
                        return linea.split(":", 1)[1].strip()
        except Exception:
            # Si ocurre un error inesperado al leer el archivo, omitimos la excepción de forma segura
            pass
        # Retornamos un valor por defecto si no se pudo encontrar o leer el nombre
        return "Usuario"

    # Método para extraer y calcular los datos de ahorros del usuario desde su archivo local
    def leer_ahorros(self, folder):
        # Construimos la ruta absoluta hacia el archivo de ahorros del usuario
        archivo = os.path.join(folder, "ahorros.txt")
        # Inicializamos la variable acumuladora para el saldo total ahorrado
        total = 0.0
        # Inicializamos la variable acumuladora para lo aportado durante el mes corriente
        mes = 0.0
        # Creamos una lista vacía para almacenar cronológicamente los movimientos financieros encontrados
        movs = []
        # Si el archivo físico de ahorros no existe en el directorio especificado
        if not os.path.exists(archivo):
            # Retornamos los valores inicializados en cero y la lista vacía
            return total, mes, movs
        try:
            # Abrimos el archivo de ahorros en modo lectura garantizando soporte para caracteres especiales
            with open(archivo, "r", encoding="utf-8") as f:
                # Leemos todas las líneas del archivo de manera secuencial en una lista
                lineas = f.readlines()
            # Recorremos de manera individual cada línea extraída del archivo
            for linea in lineas:
                # Removemos los espacios adicionales y saltos de línea al inicio y final
                linea = linea.strip()
                # Si la línea analizada está completamente vacía, saltamos a la siguiente iteración
                if not linea:
                    continue
                # Segmentamos la línea por comas para separar los atributos del movimiento
                partes = linea.split(",")
                # Validamos que el formato contenga exactamente los tres campos esperados (tipo, categoría, cantidad)
                if len(partes) == 3:
                    # Desempaquetamos los tres elementos dentro de sus respectivas variables conceptuales
                    tipo, cat, cant_str = partes
                    # Convertimos el valor numérico en formato de cadena a un tipo flotante de precisión decimal
                    cantidad = float(cant_str)
                    # Evaluamos si el tipo de registro corresponde a una entrada de fondos ("Ingreso")
                    if tipo == "Ingreso":
                        # Incrementamos el acumulador global de ahorros con la cantidad procesada
                        total += cantidad
                        # Sumamos la cantidad al acumulador mensual (criterio simplificado de ingresos)
                        mes += cantidad
                    else:
                        # Restamos la cantidad del acumulador total en caso de tratarse de un egreso o retiro
                        total -= cantidad
                    # Añadimos el registro completo estructurado como tupla a nuestra colección de movimientos
                    movs.append((tipo, cat, cantidad))
        except Exception as e:
            # Imprimimos en la consola de depuración el mensaje de error capturado al leer los ahorros
            print(f"[Home] Error leyendo ahorros: {e}")
        # Retornamos el saldo total, el mensual y una lista invertida limitada a los últimos 5 movimientos
        return total, mes, list(reversed(movs))[:5]

    # Método para computar la sumatoria de capital inyectado en compras dentro del historial transaccional
    def leer_total_invertido(self, folder):
        # Definimos la ruta de acceso al archivo con el registro histórico de operaciones de inversión
        archivo = os.path.join(folder, "historial_inversiones.txt")
        # Colocamos en cero el contador acumulativo de dinero invertido
        total = 0.0
        # Verificamos si el archivo de historial de inversiones no está disponible en el disco
        if not os.path.exists(archivo):
            # Retornamos el valor inicial de cero al no haber registros previos
            return total
        try:
            # Abrimos el archivo de texto en modo lectura utilizando codificación estándar UTF-8
            with open(archivo, "r", encoding="utf-8") as f:
                # Recorremos secuencialmente cada línea del log de inversiones
                for linea in f:
                    # Si la línea documenta una operación de COMPRA y registra la etiqueta "Dinero usado:"
                    if "COMPRA" in linea and "Dinero usado:" in linea:
                        # Dividimos el texto de la línea basándonos en el carácter separador de tubería
                        partes = linea.split("|")
                        # Examinamos cada segmento individual de la línea fragmentada
                        for p in partes:
                            # Comprobamos si el segmento actual contiene el patrón buscado
                            if "Dinero usado:" in p:
                                # Extraemos la cantidad aislando el texto, removiendo el símbolo de euro y limpiando espacios
                                valor_str = p.split("Dinero usado:")[1].strip().replace("€", "").strip()
                                # Convertimos la cadena limpia en un número flotante y lo acumulamos en el total
                                total += float(valor_str)
        except Exception as e:
            # Reportamos mediante salida estándar cualquier anomalía producida durante la lectura del archivo
            print(f"[Home] Error leyendo historial: {e}")
        # Devolvemos la sumatoria total del dinero real utilizado en las inversiones
        return total

    # Método para extraer los activos actuales que integran el portafolio del usuario
    def leer_portafolio(self, perfil_path):
        # Obtenemos la ruta del directorio contenedor a partir del archivo del perfil
        folder = os.path.dirname(perfil_path)
        # Extraemos el nombre base del archivo del perfil excluyendo su extensión para estructurar ficheros relacionados
        nombre_base = os.path.splitext(os.path.basename(perfil_path))[0]
        # Consolidamos la ruta del archivo específico que describe la composición de activos del portafolio
        archivo = os.path.join(folder, f"{nombre_base}_portafolio.txt")
        # Inicializamos un diccionario vacío para indexar las llaves del ticker y sus balances
        portafolio = {}
        # Si el archivo del portafolio no existe físicamente en el sistema
        if not os.path.exists(archivo):
            # Devolvemos el diccionario de portafolio sin elementos
            return portafolio
        try:
            # Abrimos el archivo con los datos del portafolio para iniciar su lectura
            with open(archivo, "r", encoding="utf-8") as f:
                # Leemos cíclicamente cada línea del archivo de portafolio
                for linea in f:
                    # Removemos los espacios innecesarios al inicio y final de la línea actual
                    linea = linea.strip()
                    # Validamos que la línea disponga del carácter de asignación de dos puntos
                    if ":" in linea:
                        # Fragmentamos la línea en dos secciones: identificador del activo y cantidad acumulada
                        ticker, cant = linea.split(":", 1)
                        # Guardamos en el diccionario el par clave (ticker en mayúsculas) y valor (cantidad flotante)
                        portafolio[ticker.strip().upper()] = float(cant.strip())
        except Exception as e:
            # Exponemos el error en consola si surge algún fallo abriendo o interpretando el portafolio
            print(f"[Home] Error leyendo portafolio: {e}")
        # Retornamos el diccionario mapeado con los activos y cantidades vigentes
        return portafolio

    # Método para mapear los costos agregados de compra asociados a cada ticker individual
    def leer_coste_por_ticker(self, folder):
        # Construimos la ruta del archivo que compila el historial de inversiones
        archivo = os.path.join(folder, "historial_inversiones.txt")
        # Inicializamos un diccionario vacío destinado a asociar tickers con montos financieros invertidos
        coste = {}
        # Evaluamos la presencia física del documento transaccional en el directorio
        if not os.path.exists(archivo):
            # Devolvemos el diccionario de costos vacío en caso de ausencia del archivo
            return coste
        try:
            # Aperturamos el archivo transaccional en modo lectura usando UTF-8
            with open(archivo, "r", encoding="utf-8") as f:
                # Analizamos línea por línea el contenido total del archivo
                for linea in f:
                    # Si la instrucción descrita en la línea no representa un evento de compra, la descartamos
                    if "COMPRA" not in linea:
                        continue
                    # Segmentamos la fila informativa en partes separadas por el carácter de barra vertical
                    partes = linea.split("|")
                    # Corroboramos que existan al menos tres bloques informativos para evitar errores de índice
                    if len(partes) < 3:
                        continue
                    try:
                        # Extraemos y limpiamos las cadenas para aislar la clave identificadora del ticker
                        ticker = partes[1].split(":")[1].strip()
                        # Extraemos y depuramos la cadena monetaria eliminando el signo de euros y espacios extras
                        dinero_str = partes[2].split("Dinero usado:")[1].strip().replace("€", "").strip()
                        # Convertimos el residuo textual limpio a su representación numérica flotante
                        dinero = float(dinero_str)
                        # Acumulamos el valor en el diccionario sumándolo al coste previo registrado para ese ticker
                        coste[ticker] = coste.get(ticker, 0.0) + dinero
                    except Exception:
                        # Ignoramos líneas corruptas o fallos de parseo puntuales dentro de los bloques
                        continue
        except Exception as e:
            # Notificamos el error surgido durante el procesamiento secuencial del coste por ticker
            print(f"[Home] Error leyendo coste por ticker: {e}")
        # Retornamos el mapa consolidado de inversiones monetarias indexadas por activo financiero
        return coste

    # Método para contactar con Yahoo Finance y extraer las cotizaciones de precios más recientes
    def descargar_precios(self, tickers_yf):
        # Instanciamos un diccionario vacío para almacenar las cotizaciones correspondientes a cada símbolo
        precios = {}
        # Validamos si la lista de símbolos provista no se encuentra vacía antes de hacer la llamada
        if not tickers_yf:
            return precios
        try:
            # Descargamos los datos intradía de Yahoo Finance configurando un intervalo ágil de dos minutos
            datos = yf.download(tickers_yf, period="1d", interval="2m", progress=False, auto_adjust=True)
            # Validamos que el DataFrame devuelto por el API de yfinance contenga información válida
            if not datos.empty:
                # Si el DataFrame usa un índice de columnas compuesto (MultiIndex), extraemos la jerarquía de cierre
                if isinstance(datos.columns, pd.MultiIndex):
                    cierre = datos["Close"]
                else:
                    # De lo contrario, adaptamos la serie simple de precios de cierre a una estructura DataFrame
                    cierre = datos["Close"].to_frame(name=tickers_yf[0])
                # Iteramos por cada cadena de ticker solicitada en los parámetros de la función
                for t_yf in tickers_yf:
                    try:
                        # Eliminamos valores nulos de la columna asociada a la cotización bursátil
                        col = cierre[t_yf].dropna()
                        # Si localizamos registros válidos de precios dentro de la serie temporal
                        if not col.empty:
                            # Registramos la última posición numérica de la columna como precio de cotización actual
                            precios[t_yf] = float(col.iloc[-1])
                    except Exception:
                        # En caso de fallo con un símbolo individual asignamos un valor de cero por seguridad
                        precios[t_yf] = 0.0
        except Exception as e:
            # Registramos en consola errores vinculados a la conectividad de red o fallos en el API de yfinance
            print(f"[Home] Error descargando precios: {e}")
        # Devolvemos el diccionario mapeado con las cotizaciones de mercado vigentes
        return precios