# Models/registro_m.py
import re
import os

class RegistroRepository:
    """Patrón Repository: Encargado exclusivo de crear carpetas y escribir archivos.
    Oculta los detalles de implementación (disco duro, txt, carpetas)."""
    
    def __init__(self, carpeta_raiz="informacion_cliente", nombre_fichero="perfil.txt"):
        self._carpeta_raiz = carpeta_raiz
        self._nombre_fichero = nombre_fichero

    def guardar_nuevo_usuario(self, dni, datos_usuario):
        """Recibe un diccionario con datos y los escribe físicamente en el disco."""
        try:
            # Crea la ruta de la carpeta usando el DNI como identificador único
            ruta_carpeta = os.path.join(self._carpeta_raiz, dni)
            
            # Comprueba si el usuario ya existe
            if os.path.exists(ruta_carpeta):
                return False, "El usuario con este DNI ya se encuentra registrado."

            # Crea la carpeta
            os.makedirs(ruta_carpeta)
            ruta_archivo = os.path.join(ruta_carpeta, self._nombre_fichero)

            # Escribe los datos en el archivo
            with open(ruta_archivo, "w", encoding="utf-8") as archivo:
                archivo.write("=======================================\n")
                archivo.write(f"Nombre:               {datos_usuario['nombre']}\n")
                archivo.write(f"Apellidos:            {datos_usuario['apellidos']}\n")
                archivo.write(f"DNI:                  {dni}\n")
                archivo.write(f"Fecha de Nacimiento:  {datos_usuario['fecha']}\n")
                archivo.write(f"Correo Electrónico:   {datos_usuario['email']}\n")
                archivo.write(f"Teléfono:             {datos_usuario['prefijo']} {datos_usuario['telefono']}\n")
                archivo.write(f"Contraseña:           {datos_usuario['password']}\n")
                archivo.write(f"Color Fondo Menu:     #2D033B\n")
                archivo.write(f"Color Boton Menu:     #482673\n")
                archivo.write("=======================================\n")
                
            return True, None
        except Exception as e:
            return False, str(e)


class RegistroModel:
    """Capa de Negocio. Valida reglas (emails, formato) y usa el repositorio para guardar."""
    
    def __init__(self):
        self.repository = RegistroRepository()
        self.patron_correo = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        
        # Volvemos a añadir el diccionario de países en el modelo (su lugar arquitectónico correcto)
        self._paises = {
            "Afganistán": {"prefijo": "+93", "bandera": "🇦🇫"}, "Alemania": {"prefijo": "+49", "bandera": "🇩🇪"},
            "Argentina": {"prefijo": "+54", "bandera": "🇦🇷"}, "Colombia": {"prefijo": "+57", "bandera": "🇨🇴"},
            "España": {"prefijo": "+34", "bandera": "🇪🇸"}, "Estados Unidos": {"prefijo": "+1", "bandera": "🇺🇸"},
            "Francia": {"prefijo": "+33", "bandera": "🇫🇷"}, "México": {"prefijo": "+52", "bandera": "🇲🇽"},
            "Perú": {"prefijo": "+51", "bandera": "🇵🇪"}, "Reino Unido": {"prefijo": "+44", "bandera": "🇬🇧"},
            "Venezuela": {"prefijo": "+58", "bandera": "🇻🇪"}
        }

    def obtener_paises(self):
        """Devuelve el diccionario protegido de países."""
        return self._paises

    def registrar_usuario(self, nombre, apellidos, dni, fecha, email, telefono, prefijo, password):
        """Aplica reglas lógicas antes de permitir la persistencia."""
        
        # 1. Regla de Negocio: Validar formato del correo
        if not re.match(self.patron_correo, email):
            return False, "El formato del correo electrónico no es válido."
            
        # 2. Regla de Negocio: Validar que el DNI/Teléfono no contenga anomalías graves
        if not dni.isalnum() or not telefono.isdigit():
             return False, "El DNI o Teléfono contienen caracteres no válidos."

        # 3. Preparar Entidad/Diccionario de datos limpios
        datos_usuario = {
            "nombre": nombre.title(),
            "apellidos": apellidos.title(),
            "fecha": fecha,
            "email": email.lower(),
            "telefono": telefono,
            "prefijo": prefijo,
            "password": password
        }

        # 4. Delegar la persistencia física al repositorio
        return self.repository.guardar_nuevo_usuario(dni, datos_usuario)