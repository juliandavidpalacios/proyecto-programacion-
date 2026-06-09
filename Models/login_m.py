# Importamos el módulo os para tener acceso a las funciones del sistema de archivos y directorios
import os


# Definimos la clase LoginModel que representará la capa de datos en el patrón MVP
class LoginModel:
    # Definimos el constructor de la clase Modelo, el cual no requiere parámetros iniciales obligatorios
    def __init__(self):
        # El constructor se inicializa vacío ya que la base de datos se lee de archivos físicos en el disco duro
        pass

    # Método encargado de buscar, leer y verificar si las credenciales coinciden con algún archivo registrado
    def validar_credenciales(self, correo_ingresado, pass_ingresada):
        # Asignamos a la variable carpeta el nombre del directorio raíz donde se guardan los datos de los usuarios
        carpeta = "informacion_cliente"

        # Comprobamos de manera lógica si la carpeta principal no existe o si se encuentra completamente vacía
        if not os.path.exists(carpeta) or not os.listdir(carpeta):
            # Retornamos un estado falso, ninguna ruta de usuario y un código de error específico para este caso
            return False, None, "no_usuarios"

        # Inicializamos la bandera booleana usuario_valido en False indicando que por ahora no se ha autenticado
        usuario_valido = False
        # Inicializamos la variable encargada de guardar la ubicación exacta del archivo perfil en None
        ruta_usuario = None

        # Iniciamos un ciclo para recorrer cada elemento o subcarpeta que se encuentre dentro de informacion_cliente
        for subcarpeta in os.listdir(carpeta):
            # Construimos la ruta absoluta uniendo el nombre de la carpeta raíz con el de la subcarpeta del bucle
            ruta_subcarpeta = os.path.join(carpeta, subcarpeta)

            # Verificamos mediante una validación del sistema que la ruta actual corresponda realmente a un directorio
            if os.path.isdir(ruta_subcarpeta):
                # Construimos la ruta completa apuntando directamente al fichero interno denominado perfil.txt
                ruta_completa = os.path.join(ruta_subcarpeta, "perfil.txt")

                # Evaluamos si el archivo físico perfil.txt existe de verdad dentro de esa subcarpeta analizada
                if os.path.exists(ruta_completa):
                    try:
                        # Abrimos el archivo de texto en modo de solo lectura ("r") y con codificación universal UTF-8
                        with open(ruta_completa, "r", encoding="utf-8") as f:
                            # Leemos todas las líneas de texto del archivo y las guardamos organizadas dentro de una lista
                            lineas = f.readlines()

                        # Colocamos una variable de control para el correo en False antes de inspeccionar las líneas
                        email_ok = False
                        # Colocamos una variable de control para la contraseña en False antes de inspeccionar las líneas
                        pass_ok = False

                        # Recorremos de manera secuencial cada línea de texto almacenada en la lista de líneas del fichero
                        for linea in lineas:
                            # Evaluamos si la cadena de texto de la línea actual comienza exactamente con la etiqueta indicada
                            if linea.startswith("Correo Electrónico:"):
                                # Dividimos la cadena por los dos puntos, tomamos la parte derecha y removemos sus espacios vacíos
                                if linea.split(":")[1].strip() == correo_ingresado:
                                    # Activamos la bandera de email_ok a True ya que el correo coincide a la perfección
                                    email_ok = True
                            # Evaluamos si la cadena de texto de la línea actual empieza con la etiqueta de la clave
                            elif linea.startswith("Contraseña:"):
                                # Dividimos la cadena por los dos puntos, extraemos el valor derecho y limpiamos sus espacios laterales
                                if linea.split(":")[1].strip() == pass_ingresada:
                                    # Activamos la bandera de pass_ok a True ya que la clave ingresada es matemáticamente idéntica
                                    pass_ok = True

                        # Si ambas banderas de control (email_ok y pass_ok) resultaron verdaderas de forma simultánea
                        if email_ok and pass_ok:
                            # Cambiamos la variable de validez general del inicio de sesión a True
                            usuario_valido = True
                            # Copiamos la ruta completa del archivo de perfil validado a nuestra variable de salida
                            ruta_usuario = ruta_completa
                            # Rompemos por completo el ciclo for de las subcarpetas puesto que el usuario ya fue localizado
                            break
                    # Capturamos cualquier error imprevisto de lectura, codificación o bloqueo de archivos
                    except Exception as e:
                        # Imprimimos de manera informativa en la terminal del sistema el error detallado del archivo dañado
                        print(f"Error leyendo {ruta_completa}: {e}")

        # Retornamos el estado de validez, la ruta del archivo perfil hallado y None en la variable de error
        return usuario_valido, ruta_usuario, None