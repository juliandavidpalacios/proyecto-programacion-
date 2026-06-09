# Importamos el módulo os para verificar rutas y manipular archivos del sistema
import os


# Definimos la clase MainModel que gestionará los datos globales de la aplicación
class MainModel:
    # Constructor del modelo, se inicializa sin variables obligatorias
    def __init__(self):
        # Usamos pass porque no requerimos instanciar propiedades de estado aquí
        pass

    # Método para leer el archivo del usuario y extraer sus colores guardados
    def obtener_colores_tema(self, ruta_archivo_usuario):
        # Definimos el color de fondo del menú por defecto si no se encuentra otro
        color_menu = "#2D033B"
        # Definimos el color de los botones por defecto si no se encuentra otro
        color_btn = "#482673"

        # Verificamos si la ruta del archivo del usuario existe físicamente en el disco
        if os.path.exists(ruta_archivo_usuario):
            try:
                # Abrimos el archivo en modo lectura ("r") con codificación UTF-8
                with open(ruta_archivo_usuario, "r", encoding="utf-8") as f:
                    # Leemos todas las líneas del archivo y las guardamos en una lista
                    lineas = f.readlines()
                # Iteramos sobre cada línea extraída del archivo
                for linea in lineas:
                    # Si la línea actual empieza con la etiqueta de color del fondo
                    if linea.startswith("Color Fondo Menu:"):
                        # Dividimos la línea por los dos puntos y extraemos el valor (el color hex) limpiando espacios
                        color_menu = linea.split(":")[1].strip()
                    # Si la línea actual empieza con la etiqueta de color del botón
                    elif linea.startswith("Color Boton Menu:"):
                        # Dividimos y extraemos el color hexadecimal correspondiente al botón
                        color_btn = linea.split(":")[1].strip()
            # Capturamos cualquier error de lectura
            except Exception as e:
                # Imprimimos en consola el error exacto para depuración
                print(f"Error al cargar el tema del usuario: {e}")

        # Retornamos ambos colores (ya sean los leídos del archivo o los por defecto)
        return color_menu, color_btn

    # Método para sobreescribir o añadir la nueva elección de color en el .txt
    def guardar_colores_tema(self, ruta_archivo_usuario, fondo, boton):
        # Validamos que haya una ruta válida y que el archivo del usuario exista
        if ruta_archivo_usuario and os.path.exists(ruta_archivo_usuario):
            try:
                # Abrimos el archivo en modo lectura para obtener su contenido actual
                with open(ruta_archivo_usuario, "r", encoding="utf-8") as f:
                    # Leemos todas las líneas y las guardamos en la variable lineas
                    lineas = f.readlines()

                # Creamos una lista vacía para almacenar el contenido actualizado
                nuevas_lineas = []
                # Bandera para saber si ya existía el registro del color de fondo
                tiene_fondo = False
                # Bandera para saber si ya existía el registro del color de botón
                tiene_boton = False

                # Recorremos el contenido original línea por línea
                for linea in lineas:
                    # Si detectamos la línea del fondo de menú
                    if linea.startswith("Color Fondo Menu:"):
                        # La reemplazamos inyectando el nuevo color de fondo formateado
                        nuevas_lineas.append(f"Color Fondo Menu:     {fondo}\n")
                        # Activamos la bandera indicando que sí se encontró y reemplazó
                        tiene_fondo = True
                    # Si detectamos la línea del color de botón
                    elif linea.startswith("Color Boton Menu:"):
                        # La reemplazamos inyectando el nuevo color del botón
                        nuevas_lineas.append(f"Color Boton Menu:     {boton}\n")
                        # Activamos la bandera indicando que sí se encontró y reemplazó
                        tiene_boton = True
                    # Si es cualquier otra línea (nombre, dni, contraseñas, etc.)
                    else:
                        # La añadimos intacta a la nueva lista
                        nuevas_lineas.append(linea)

                # Si el archivo era viejo y no tenía estas etiquetas de colores
                if not tiene_fondo or not tiene_boton:
                    # Si la última línea es la barrera estética de cierre "===="
                    if nuevas_lineas and nuevas_lineas[-1].startswith("===="):
                        # Extraemos y removemos temporalmente esa línea final
                        linea_final = nuevas_lineas.pop()
                        # Si no tenía fondo, lo agregamos antes del cierre
                        if not tiene_fondo: nuevas_lineas.append(f"Color Fondo Menu:     {fondo}\n")
                        # Si no tenía botón, lo agregamos antes del cierre
                        if not tiene_boton: nuevas_lineas.append(f"Color Boton Menu:     {boton}\n")
                        # Volvemos a colocar la línea de cierre al final
                        nuevas_lineas.append(linea_final)
                    # Si por alguna razón no hay línea de cierre
                    else:
                        # Simplemente anexamos el color de fondo al final del documento
                        if not tiene_fondo: nuevas_lineas.append(f"Color Fondo Menu:     {fondo}\n")
                        # Y anexamos el color del botón al final del documento
                        if not tiene_boton: nuevas_lineas.append(f"Color Boton Menu:     {boton}\n")

                # Abrimos el archivo en modo escritura ("w") para sobreescribir el viejo contenido
                with open(ruta_archivo_usuario, "w", encoding="utf-8") as f:
                    # Escribimos de golpe toda la lista actualizada en el disco duro
                    f.writelines(nuevas_lineas)
            # Capturamos posibles errores de permisos o escritura
            except Exception as e:
                # Imprimimos el error en consola
                print(f"Error al guardar preferencia de color: {e}")