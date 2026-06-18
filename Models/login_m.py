# Models/login_m.py
import os

# La entidad de dominio Usuario vive ahora en el paquete `domain` (ver diagram.puml).
# El Modelo de la capa de aplicación reutiliza ese objeto de negocio puro.
from domain.usuario import Usuario


class UsuarioRepository:
    """Patrón de Diseño: Repository.
    Único responsable de interactuar con el sistema de archivos (informacion_cliente).
    Traduce ficheros .txt <-> objetos de dominio `Usuario`."""

    def __init__(self, carpeta_raiz="informacion_cliente", nombre_fichero="perfil.txt"):
        # Propiedades privadas (con guion bajo) para denotar encapsulamiento.
        self._carpeta_raiz = carpeta_raiz
        self._nombre_fichero = nombre_fichero

    def existe_almacenamiento(self):
        """Verifica si la base de datos física existe y tiene datos."""
        return os.path.exists(self._carpeta_raiz) and os.listdir(self._carpeta_raiz)

    def obtener_ruta_perfil(self, id_usuario):
        """Construye la ruta física del perfil. Nadie fuera de esta clase
        necesita saber cómo se compone esa ruta (ocultamiento de información)."""
        return os.path.join(self._carpeta_raiz, id_usuario, self._nombre_fichero)

    def obtener_todos(self):
        """Navega por los ficheros y los transforma en una lista de objetos `Usuario`."""
        usuarios = []
        if not self.existe_almacenamiento():
            return usuarios

        for subcarpeta in os.listdir(self._carpeta_raiz):
            ruta_subcarpeta = os.path.join(self._carpeta_raiz, subcarpeta)

            if os.path.isdir(ruta_subcarpeta):
                ruta_completa = os.path.join(ruta_subcarpeta, self._nombre_fichero)

                if os.path.exists(ruta_completa):
                    usuario = self._parsear_archivo_perfil(subcarpeta, ruta_completa)
                    if usuario:
                        usuarios.append(usuario)
        return usuarios

    def _parsear_archivo_perfil(self, id_usuario, ruta_archivo):
        """Método privado: parseo del archivo de texto a entidad de dominio `Usuario`."""
        try:
            with open(ruta_archivo, "r", encoding="utf-8") as f:
                lineas = f.readlines()

            email = None
            password = None
            nombre = ""

            for linea in lineas:
                if linea.startswith("Correo Electrónico:"):
                    email = linea.split(":")[1].strip()
                elif linea.startswith("Contraseña:"):
                    password = linea.split(":")[1].strip()
                elif linea.startswith("Nombre"):
                    nombre = linea.split(":", 1)[1].strip()

            if email and password:
                # Devolvemos una entidad de dominio rica, no un diccionario suelto.
                return Usuario(
                    id_usuario=id_usuario,
                    nombre=nombre,
                    correo=email,
                    contrasena=password,
                )
        except Exception as e:
            print(f"Error crítico en repositorio leyendo {ruta_archivo}: {e}")
        return None


class LoginModel:
    """Capa de Negocio. Aplica reglas de negocio interactuando únicamente
    con abstracciones, respetando el ocultamiento de información."""

    def __init__(self):
        self.repository = UsuarioRepository()

    def validar_credenciales(self, correo_ingresado, pass_ingresada):
        """Valida las credenciales delegando la regla en la propia entidad `Usuario`."""

        # 1. Regla de negocio: verificar si hay usuarios registrados.
        if not self.repository.existe_almacenamiento():
            return False, None, "no_usuarios"

        # 2. Obtenemos entidades de dominio puras.
        lista_usuarios = self.repository.obtener_todos()

        # 3. Cada Usuario sabe validar sus propias credenciales (comportamiento, no datos).
        for usuario in lista_usuarios:
            if usuario.verificar_credenciales(correo_ingresado, pass_ingresada):
                ruta_usuario = self.repository.obtener_ruta_perfil(usuario.id_usuario)
                return True, ruta_usuario, None

        return False, None, None
