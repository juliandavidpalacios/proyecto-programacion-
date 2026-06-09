import re
import os

# Definimos la clase RegistroModel que representará la capa de datos en el patrón MVP
class RegistroModel:
    # Definimos el constructor de la clase para inicializar el diccionario de países de forma centralizada
    def __init__(self):
        # Diccionario estático masivo de países con sus prefijos internacionales y banderas descriptivas
        self.paises = {
            "Afganistán": {"prefijo": "+93", "bandera": "🇦🇫"}, "Alemania": {"prefijo": "+49", "bandera": "🇩🇪"},
            "Argentina": {"prefijo": "+54", "bandera": "🇦🇷"}, "Colombia": {"prefijo": "+57", "bandera": "🇨🇴"},
            "España": {"prefijo": "+34", "bandera": "🇪🇸"}, "Estados Unidos": {"prefijo": "+1", "bandera": "🇺🇸"},
            "Francia": {"prefijo": "+33", "bandera": "🇫🇷"}, "México": {"prefijo": "+52", "bandera": "🇲🇽"},
            "Perú": {"prefijo": "+51", "bandera": "🇵🇪"}, "Reino Unido": {"prefijo": "+44", "bandera": "🇬🇧"},
            "Venezuela": {"prefijo": "+58", "bandera": "🇻🇪"}
        }
        # Guardamos la expresión regular estándar para comprobar la estructura sintáctica de correos electrónicos
        self.patron_correo = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'

    # >>> NUEVO MÉTODO AÑADIDO PARA SOLUCIONAR EL ERROR DEL PRESENTADOR <<<
    # Método lógico encargado de validar si una dirección de correo electrónico cumple con el patrón Regex establecido
    def validar_correo(self, email):
        # Ejecuta la comprobación del patrón sobre la cadena recibida y devuelve un valor booleano implícito (True o False)
        return bool(re.match(self.patron_correo, email))

    # Método encargado de estructurar y almacenar de forma física la información bancaria en un archivo de texto
    def registrar_usuario(self, nombre, apellidos, dni, fecha, email, prefijo, telefono, pass1):
        # Definimos el nombre de la carpeta raíz encargada de centralizar la información de los clientes
        carpeta = "informacion_cliente"

        # Reemplazamos los espacios del nombre y apellidos por guiones bajos para generar un nombre de carpeta seguro
        nombre_usuario_seguro = f"{nombre}_{apellidos}".replace(" ", "_")
        # Unimos de forma absoluta la carpeta contenedora con la subcarpeta del usuario específico
        carpeta_usuario = os.path.join(carpeta, nombre_usuario_seguro)
        # Forzamos la creación del árbol de directorios físico en el disco si este no existiese previamente
        os.makedirs(carpeta_usuario, exist_ok=True)

        # Establecemos la ruta final combinando la subcarpeta específica con el archivo estático perfil.txt
        ruta_completa = os.path.join(carpeta_usuario, "perfil.txt")

        # Iniciamos un bloque de control de excepciones para reportar fallos de permisos o de escritura en disco
        try:
            # Abrimos el archivo perfil.txt en modo de escritura destructiva ("w") con codificación universal UTF-8
            with open(ruta_completa, "w", encoding="utf-8") as archivo:
                # Escribimos los caracteres delimitadores superiores del bloque del reporte
                archivo.write("=======================================\n")
                # Escribimos el título institucional centrado del reporte bancario
                archivo.write("       INFORMACIÓN BANCARIA DEL CLIENTE\n")
                # Escribimos los caracteres delimitadores inferiores de la cabecera
                archivo.write("=======================================\n")
                # Grabamos la concatenación formateada del nombre y apellidos dentro del archivo físico
                archivo.write(f"Nombre Completo:      {nombre} {apellidos}\n")
                # Grabamos la clave identificadora única del DNI o Pasaporte del cliente
                archivo.write(f"DNI / NIE:            {dni}\n")
                # Escribimos la cadena correspondiente a la fecha de nacimiento ingresada
                archivo.write(f"Fecha de Nacimiento:  {fecha}\n")
                # Escribimos el correo electrónico validado del usuario para su inicio de sesión posterior
                archivo.write(f"Correo Electrónico:   {email}\n")
                # Almacenamos el teléfono de contacto anteponiendo el prefijo internacional recuperado
                archivo.write(f"Teléfono:             {prefijo} {telefono}\n")
                # Escribimos de forma plana la contraseña definida para la cuenta del cliente
                archivo.write(f"Contraseña:           {pass1}\n")

                # Escribimos las propiedades de diseño de la interfaz como el color hexadecimal de fondo por defecto
                archivo.write(f"Color Fondo Menu:     #2D033B\n")
                # Escribimos de igual forma el color del botón por defecto para la consistencia visual de la app
                archivo.write(f"Color Boton Menu:     #482673\n")

                # Concluimos el bloque del archivo escribiendo la línea de cierre perimetral
                archivo.write("=======================================\n")
            # Si el archivo se redactó y cerró sin problemas, devolvemos un estado exitoso (True) al presentador
            return True, None
        # Atrapamos cualquier error físico del sistema de archivos que impida la creación del archivo
        except Exception as e:
            # Retornamos un estado fallido acoplado al objeto de error para que el presentador lo muestre en pantalla
            return False, e