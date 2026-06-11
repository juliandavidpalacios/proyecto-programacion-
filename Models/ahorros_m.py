import os
import yfinance as yf

class AhorrosModel:
    def __init__(self):
        # Almacena la ruta del archivo de texto donde se registran los movimientos de ahorro
        self.archivo_ahorros = None

    # Método para preparar y resolver las rutas de archivos asignadas al usuario logueado
    def establecer_ruta_usuario(self, perfil_txt):
        carpeta_usuario = os.path.dirname(perfil_txt)
        # Combina la ruta de la carpeta con el nombre estándar del archivo de ahorros
        self.archivo_ahorros = os.path.join(carpeta_usuario, "ahorros.txt")
        if not os.path.exists(self.archivo_ahorros):
            with open(self.archivo_ahorros, "w", encoding="utf-8") as f:
                pass
        return self.archivo_ahorros

    # Método de lectura que consulta el precio actual de activos financieros y calcula su valor total
    def obtener_valor_portafolio(self):
        # Define de forma estricta la ruta absoluta hacia el archivo del portafolio del cliente
        ruta_perfil = r"C:\Users\santi\PycharmProjects\proyecto-programacion-\informacion_cliente\f_f\perfil_portafolio.txt"
        # Comprueba si el archivo físico del portafolio no existe en la ubicación especificada
        if not os.path.exists(ruta_perfil):
            print(f"[AVISO] No se encontró perfil_portafolio.txt en: {ruta_perfil}")
            return 0.0

        criptos_conocidas = {"BTC", "ETH", "DOGE", "ADA", "SOL", "XRP", "BNB", "LTC"}
        posiciones = {}
        try:
            # Abre el archivo del portafolio en modo lectura garantizando soporte para caracteres internacionales
            with open(ruta_perfil, "r", encoding="utf-8") as f:
                # Itera a través de cada línea presente en el flujo de texto del archivo
                for linea in f:
                    # Elimina espacios en blanco innecesarios y saltos de línea al inicio o final
                    linea = linea.strip()
                    # Salta la línea si está vacía o carece del delimitador de clave-valor ":"
                    if not linea or ":" not in linea:
                        # Continúa de inmediato con la siguiente línea del bucle
                        continue
                    partes = linea.split(":")
                    ticker = partes[0].strip().upper()
                    # Extrae la cantidad numérica convirtiendo el fragmento de texto a tipo flotante
                    cantidad = float(partes[1].strip())
                    # Acumula la cantidad en el diccionario asociándola a la clave de su respectivo ticker
                    posiciones[ticker] = posiciones.get(ticker, 0.0) + cantidad
        # Captura cualquier tipo de fallo o excepción durante el proceso de parseo y lectura del archivo
        except Exception as e:
            # Imprime en la consola el error detallado para facilitar la depuración técnica
            print(f"[ERROR] Leyendo perfil_portafolio.txt: {e}")
            # Retorna un saldo acumulado nulo debido a la interrupción del flujo
            return 0.0
        # Si el diccionario de posiciones se encuentra totalmente vacío finaliza el cálculo
        if not posiciones:
            # Devuelve cero al no existir registros de activos cargados
            return 0.0
        # Comprensión de lista para formatear tickers añadiendo el sufijo -EUR si son criptomonedas
        tickers_yf = [
            f"{t}-EUR" if t in criptos_conocidas else t
            for t in posiciones.keys()
        ]
        # Declara e inicializa la variable acumuladora para almacenar el valor monetario global en euros
        total_euros = 0.0
        try:
            # Descarga los datos de mercado más recientes para todos los tickers usando yfinance
            datos = yf.download(tickers_yf, period="1d", interval="1m", progress=False)
            # Evalúa si el dataframe retornado por la consulta web está vacío o incompleto
            if datos.empty:
                # Devuelve un valor por defecto al no disponer de cotizaciones activas
                return 0.0
            # Captura la última fila correspondiente al precio de cierre más reciente del mercado
            precios_cierre = datos["Close"].iloc[-1]
            # Recorre cada elemento guardado en el mapa de posiciones originales del cliente
            for ticker_orig, cantidad in posiciones.items():
                # Determina la clave de consulta adaptada con el sufijo de moneda según corresponda
                ticker_yf = f"{ticker_orig}-EUR" if ticker_orig in criptos_conocidas else ticker_orig
                try:
                    # En caso de que se consulte un único activo, extrae el último valor escalar directo
                    if len(tickers_yf) == 1:
                        precio = float(precios_cierre.iloc[-1])
                    # Si existen múltiples activos en el pool, filtra la serie usando la clave del ticker
                    else:
                        precio = float(precios_cierre[ticker_yf])
                    # Calcula el producto de la cantidad por su precio de mercado y lo suma al acumulador
                    total_euros += cantidad * precio
                # Intercepta fallos puntuales al recuperar la cotización de un activo específico
                except Exception as e:
                    # Imprime un mensaje informativo indicando el ticker con problemas de descarga
                    print(f"[AVISO] No se pudo obtener precio de {ticker_yf}: {e}")
        # Captura errores críticos generalizados durante la comunicación remota con yfinance
        except Exception as e:
            # Imprime un mensaje detallado del error de red o descarga en la consola
            print(f"[ERROR] Descargando precios con yfinance: {e}")
        # Retorna el cálculo consolidado del valor monetario de las inversiones en euros
        return total_euros

    # Método encargado de leer las líneas del historial de ahorros almacenadas localmente
    def leer_lineas_ahorros(self):
        # Valida que la propiedad de ruta esté configurada y que el archivo exista físicamente
        if not self.archivo_ahorros or not os.path.exists(self.archivo_ahorros):
            # Devuelve una lista vacía interrumpiendo el proceso de lectura de forma segura
            return []
        # Abre el archivo de ahorros en modo lectura compartida y codificación estandarizada
        with open(self.archivo_ahorros, "r", encoding="utf-8") as f:
            # Lee la totalidad de líneas de texto presentes devolviéndolas estructuradas en una lista
            return f.readlines()

    # Método responsable de escribir una nueva transacción o movimiento financiero en el archivo
    def guardar_movimiento(self, tipo, categoria, cantidad):
        # Abre el archivo en modo "append" ('a') para añadir contenido al final sin borrar lo previo
        with open(self.archivo_ahorros, "a", encoding="utf-8") as f:
            # Escribe los valores separados por comas siguiendo el formato CSV estructurado
            f.write(f"{tipo},{categoria},{cantidad:.2f}\n")