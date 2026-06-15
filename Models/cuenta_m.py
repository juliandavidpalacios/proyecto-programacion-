import os # Importa la librería os para interactuar de forma directa con el sistema de archivos y directorios del disco

class CuentaModel: # Declara la clase del Modelo encargada exclusivamente de la abstracción y el acceso físico a los datos del cliente
    def __init__(self): # Constructor de la clase modelo para inicializar su estructura base
        pass # Sentencia nula ya que la clase opera de forma directa con flujos funcionales sin estado interno fijo
    def cargar_lineas_perfil(self, archivo_actual): # Método para leer todo el archivo de perfil y retornar sus líneas en una lista
        if not archivo_actual or not os.path.exists(archivo_actual): # Evalúa si la ruta recibida es nula o si el archivo no existe físicamente en el almacenamiento
            return None # Devuelve un indicador nulo señalando la imposibilidad de acceder al archivo del cliente especificado
        try: # Bloque de seguridad para aislar posibles excepciones al intentar abrir flujos de datos en el sistema
            with open(archivo_actual, "r", encoding="utf-8") as f: # Abre el documento plano de perfil en modo lectura bajo codificación estandarizada UTF-8
                lineas = f.readlines() # Carga la totalidad de las líneas del archivo en una variable local estructurada como lista de strings
                return lineas # Retorna exitosamente la lista conteniendo cada renglón del documento de perfil de cliente
        except Exception: # Captura fallos de bajo nivel durante el intento de apertura o lectura del fichero plano
            return None # Retorna None indicando al llamador la ocurrencia de un error imprevisto en la lectura de datos
    def obtener_contrasena_actual(self, archivo_actual): # Método dedicado a examinar el archivo de texto y extraer la credencial vigente del usuario
        contrasena_actual = "" # Inicializa la variable de control tal como está declarada textualmente en el código fuente base
        if os.path.exists(archivo_actual): # Comprueba si la ruta al archivo plano del usuario existe en el sistema antes de abrir el flujo
            try: # Bloque de aislamiento ante posibles interrupciones en la lectura del archivo de configuración
                with open(archivo_actual, "r", encoding="utf-8") as f: # Abre el fichero del perfil en modo de lectura segura con codificación UTF-8
                    for linea in f.readlines(): # Recorre de forma cíclica y secuencial cada línea de texto recuperada del almacenamiento
                        if linea.startswith("Contraseña:"): # Comprueba si el renglón analizado inicia con la etiqueta de texto que indica la credencial
                            contrasena_actual = linea.split(":")[1].strip() # Separa el string por el delimitador de dos puntos y extrae limpiamente la clave secreta
                            break # Rompe inmediatamente el ciclo de lectura al haber obtenido con éxito la información buscada
            except Exception: # Atrapa cualquier excepción al intentar procesar el documento de datos contables
                return "ERROR" # Devuelve una bandera textual indicando un fallo en el procedimiento de extracción de seguridad
        return contrasena_actual # Retorna la contraseña limpia localizada o en su defecto una cadena vacía de inicialización
    def escribir_perfil_completo(self, archivo_actual, nombre, dni, fecha_nac, correo, telefono, contrasena_actual, color_menu, color_btn): # Método encargado de sobreescribir el archivo completo formateando los campos correspondientes
        with open(archivo_actual, "w", encoding="utf-8") as f: # Abre el archivo del cliente en modo de escritura destructiva aplicando codificación limpia UTF-8
            f.write("=======================================\n") # Escribe el borde perimetral decorativo superior del reporte estructurado de datos
            f.write("       INFORMACIÓN BANCARIA DEL CLIENTE\n") # Escribe el rótulo de cabecera centrado indicando el contenido del archivo contable
            f.write("=======================================\n") # Escribe la línea divisoria intermedia para separar la cabecera de los datos del cliente
            f.write(f"Nombre Completo:      {nombre}\n") # Escribe el campo formateado con el nuevo nombre completo consolidado del usuario
            f.write(f"DNI / NIE:            {dni}\n") # Guarda la línea formateada conteniendo el número de identificación DNI o NIE ingresado
            f.write(f"Fecha de Nacimiento:  {fecha_nac}\n") # Graba la línea estructurada con la información de la fecha de nacimiento provista
            f.write(f"Correo Electrónico:   {correo}\n") # Almacena la línea correspondiente a la dirección registrada de correo electrónico del cliente
            f.write(f"Teléfono:             {telefono}\n") # Graba el dato del número de teléfono de contacto estructurado en el archivo de texto
            f.write(f"Contraseña:           {contrasena_actual}\n") # Escribe la contraseña actual recuperada para conservarla intacta dentro de su registro correspondiente
            f.write(f"Color Fondo Menu:     {color_menu}\n") # Almacena la preferencia actual guardada para el tono cromático de fondo del menú del sistema
            f.write(f"Color Boton Menu:     {color_btn}\n") # Registra el valor hexadecimal correspondiente al color de los botones dentro de la configuración
            f.write("=======================================\n") # Escribe la línea estética final de clausura del bloque de datos estructurado
    def obtener_datos_perfil(self, archivo_actual): # Lee el perfil y devuelve un diccionario limpio con los campos del cliente
        datos = {"nombre": "", "dni": "", "fecha": "", "correo": "", "telefono": ""} # Estructura por defecto con claves canónicas independientes de la interfaz
        lineas = self.cargar_lineas_perfil(archivo_actual) # Reutiliza el método existente para leer el archivo de perfil físico
        if lineas is None: # Si el archivo no existe o falló la lectura
            return datos # Devuelve el diccionario vacío por defecto sin reventar el flujo
        mapeo = { # Tabla de traducción entre la etiqueta del archivo y la clave canónica del diccionario
            "Nombre Completo:": "nombre",
            "DNI / NIE:": "dni",
            "Fecha de Nacimiento:": "fecha",
            "Correo Electrónico:": "correo",
            "Teléfono:": "telefono",
        }
        for linea in lineas: # Recorre cada renglón del archivo de perfil
            partes = linea.split(":", 1) # Divide en clave y valor por el primer dos puntos
            if len(partes) >= 2: # Solo procesa líneas con formato clave-valor válido
                clave = (partes[0].strip() + ":") # Reconstruye la etiqueta con los dos puntos para buscarla en el mapeo
                if clave in mapeo: # Si la etiqueta es uno de los campos que nos interesan
                    datos[mapeo[clave]] = partes[1].strip() # Guarda el valor limpio bajo su clave canónica
        return datos # Retorna el diccionario poblado con los datos del cliente
    def renombrar_carpeta_usuario(self, archivo_actual, nombre): # Renombra físicamente la carpeta del usuario según su nuevo nombre completo
        nuevo_nombre_carpeta = nombre.replace(" ", "_") # Convierte el nombre en un identificador de carpeta válido sustituyendo espacios
        nueva_carpeta = os.path.join("informacion_cliente", nuevo_nombre_carpeta) # Compone la ruta destino dentro de la carpeta raíz de clientes
        carpeta_actual = os.path.dirname(archivo_actual) # Obtiene la carpeta donde reside actualmente el perfil
        if carpeta_actual == nueva_carpeta: # Si el nombre no cambió, no hay nada que renombrar
            return archivo_actual # Devuelve la ruta original intacta
        os.rename(carpeta_actual, nueva_carpeta) # Solicita al sistema operativo mover/renombrar la carpeta del cliente
        return os.path.join(nueva_carpeta, "perfil.txt") # Devuelve la nueva ruta del archivo de perfil ya reubicado
    def actualizar_contrasena(self, archivo_actual, pass_nueva): # Método específico para reescribir el archivo actualizando únicamente la línea de la credencial
        with open(archivo_actual, "r", encoding="utf-8") as f: # Abre el archivo plano del usuario logueado en modo lectura segura con soporte UTF-8
            lineas = f.readlines() # Vuelca y almacena la lista completa de líneas originales dentro de una variable local de control
        lineas_actualizadas = [] # Inicializa un arreglo vacío destinado a conformar el nuevo cuerpo de texto modificado para el archivo
        for linea in lineas: # Recorre secuencialmente cada uno de los renglones extraídos del archivo de texto original en la memoria
            if linea.startswith("Contraseña:"): # Comprueba si la línea actual representa el registro del password secreto del perfil de usuario
                lineas_actualizadas.append(f"Contraseña:           {pass_nueva}\n") # Añade a la lista el registro modificado incorporando la nueva clave secreta con su salto de línea
            else: # En caso de que la línea analizada corresponda a cualquier otro atributo de información o diseño estético del cliente
                lineas_actualizadas.append(linea) # Agrega el renglón original sin aplicar ningún tipo de alteración o modificación en su estructura
        with open(archivo_actual, "w", encoding="utf-8") as f: # Abre el archivo del cliente en modo escritura para reemplazar todo el contenido previo del documento
            f.writelines(lineas_actualizadas) # Ejecuta el volcado físico completo escribiendo la lista actualizada de líneas de texto sobre el disco local