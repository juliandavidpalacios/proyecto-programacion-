# Importamos el módulo os para manejar rutas y verificar la existencia de archivos
import os
# Importamos yfinance para descargar datos financieros reales del mercado
import yfinance as yf


# Definimos la clase InvertirModel que gestionará los datos y la persistencia
class InvertirModel:
    # Método constructor que inicializa la base de datos simulada
    def __init__(self):
        # Base de datos simulada de activos organizada por categorías (Acciones y Cripto) con sus detalles
        self.base_datos = {
            "Acciones": {
                "AAPL": {"nombre": "Apple Inc.", "precio": 165.20, "sector": "Tecnología",
                         "resumen": "Líder global en hardware, software y servicios. Creadores del iPhone, Mac y iPad. Considerada una de las empresas más valiosas del mundo."},
                "TSLA": {"nombre": "Tesla Inc.", "precio": 210.50, "sector": "Automoción",
                         "resumen": "Empresa enfocada en la transición a energía sostenible. Fabrica vehículos eléctricos, paneles solares y baterías gigantes."},
                "AMZN": {"nombre": "Amazon.com", "precio": 140.00, "sector": "E-commerce",
                         "resumen": "El gigante del comercio electrónico y proveedor líder de servicios en la nube (AWS)."}
            },
            "Cripto": {
                "BTC": {"nombre": "Bitcoin", "precio": 58000.00, "sector": "Criptomoneda",
                        "resumen": "La primera criptomoneda descentralizada. Creada como reserva de valor y alternativa digital al oro. Alta volatilidad."},
                "ETH": {"nombre": "Ethereum", "precio": 3100.00, "sector": "Criptomoneda",
                        "resumen": "Plataforma de código abierto basada en blockchain. Permite la creación de contratos inteligentes y aplicaciones descentralizadas (dApps)."}
            }
        }

    # Método para obtener los datos de mercado en tiempo real usando yfinance
    def obtener_datos_api(self, ticker_real, periodo, intervalo):
        # Descarga el objeto del activo a través de su ticker
        activo_api = yf.Ticker(ticker_real)
        # Retorna el historial de precios filtrado por el período e intervalo de tiempo solicitados
        return activo_api.history(period=periodo, interval=intervalo)

    # Método para calcular el saldo leyendo el archivo nativo ahorros.txt
    def calcular_saldo_ahorros(self, usuario_logueado):
        # Almacena la ruta del perfil del usuario logueado en una variable local
        perfil_path = usuario_logueado
        # Extrae la carpeta contenedora del archivo de perfil
        folder = os.path.dirname(perfil_path)
        # Define la ruta absoluta hacia el archivo general de ahorros.txt
        archivo_ahorros = os.path.join(folder, "ahorros.txt")
        # Inicializa la variable del saldo acumulado en cero
        saldo = 0.0

        # Comprueba si el archivo físico de ahorros existe en el disco duro
        if os.path.exists(archivo_ahorros):
            try:
                # Abre el archivo de texto en modo lectura con codificación universal utf-8
                with open(archivo_ahorros, "r", encoding="utf-8") as f:
                    # Itera a través de cada línea presente en el documento de texto
                    for linea in f:
                        # Limpia los espacios y rompe la línea en partes separadas por comas
                        partes = linea.strip().split(",")
                        # Verifica que la línea contenga los 3 parámetros requeridos (tipo, descripción, cantidad)
                        if len(partes) == 3:
                            # Desempaqueta los tres componentes de la línea ignorando la descripción central
                            tipo, _, cant_str = partes
                            try:
                                # Transforma el texto de la cantidad a un formato numérico flotante
                                cantidad = float(cant_str)
                                # Si la operación es una adición de fondos al saldo general
                                if tipo in ["Depósito", "Ingreso"]:
                                    # Suma de forma acumulativa la cantidad extraída al saldo general
                                    saldo += cantidad
                                # Si la operación corresponde a una salida de dinero
                                elif tipo == "Retiro":
                                    # Resta la cantidad cobrada del saldo general del usuario
                                    saldo -= cantidad
                            # Captura errores en caso de que la conversión numérica falle en la línea actual
                            except ValueError:
                                # Ignora la línea defectuosa y continúa el ciclo con la siguiente línea
                                continue
            # Captura cualquier fallo imprevisto en el proceso de apertura o lectura del fichero
            except Exception as e:
                # Imprime en la consola el error detectado durante la lectura de la hucha de ahorros
                print(f"Error al leer saldo de ahorros: {e}")
        # Devuelve una tupla que contiene el saldo calculado final y la ruta física del archivo
        return saldo, archivo_ahorros

    # Método para leer los activos financieros acumulados en el portafolio personal del usuario
    def leer_portafolio_activos(self, usuario_logueado):
        # Almacena la ruta del archivo de configuración del usuario activo en memoria
        perfil_path = usuario_logueado
        # Obtiene el directorio base donde se aloja el perfil del usuario
        folder = os.path.dirname(perfil_path)
        # Extrae el nombre del usuario sin la extensión .txt para usarlo de prefijo
        nombre_base = os.path.splitext(os.path.basename(perfil_path))[0]
        # Construye la ruta final del archivo de portafolio específico de ese usuario
        archivo_portafolio = os.path.join(folder, f"{nombre_base}_portafolio.txt")
        # Crea un diccionario vacío destinado a almacenar las acciones/criptos encontradas
        portafolio = {}

        # Comprueba de forma lógica si el archivo de portafolio ya existe en el sistema de archivos
        if os.path.exists(archivo_portafolio):
            try:
                # Abre el archivo del portafolio en modo lectura tradicional
                with open(archivo_portafolio, "r", encoding="utf-8") as f:
                    # Recorre línea por línea el archivo de inventario de activos
                    for linea in f:
                        # Elimina espacios en blanco innecesarios al inicio y final de la línea
                        linea = linea.strip()
                        # Si la línea contiene el caracter de dos puntos como separador clave
                        if ":" in linea:
                            # Divide la cadena en el símbolo del activo y su cantidad numérica
                            ticker, cant = linea.split(":")
                            # Agrega el activo al diccionario eliminando espacios y convirtiendo la cantidad a flotante
                            portafolio[ticker.strip()] = float(cant.strip())
            # Captura fallos críticos del sistema al interactuar con el archivo de portafolio
            except Exception as e:
                # Muestra un mensaje informativo en la consola con detalles del error
                print(f"Error al leer portafolio: {e}")
        # Devuelve el estado actual de los activos y la ruta de almacenamiento asignada
        return portafolio, archivo_portafolio

    # Método para sobrescribir y actualizar el archivo físico del portafolio del usuario de forma limpia
    def guardar_portafolio_activos(self, path, portafolio):
        try:
            # Abre el archivo del portafolio en modo de escritura destructiva ("w")
            with open(path, "w", encoding="utf-8") as f:
                # Recorre los pares de activo y cantidad almacenados en el diccionario de inventario
                for ticker, cant in portafolio.items():
                    # Guarda el activo solo si el usuario retiene una cantidad mayor a cero unidades
                    if cant > 0:
                        # Escribe la línea con el formato clásico guardando 6 decimales de precisión
                        f.write(f"{ticker}: {cant:.6f}\n")
        # Captura excepciones si no se tienen permisos de escritura o el archivo está bloqueado
        except Exception as e:
            # Notifica el fallo técnico por medio de la consola del sistema
            print(f"Error al guardar portafolio: {e}")