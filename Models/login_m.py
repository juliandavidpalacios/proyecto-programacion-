# Models/login_m.py
import os

class Usuario:
    """Clase de Dominio (Entidad). Representa a un usuario del sistema en memoria.
    Cero conocimiento de infraestructura (archivos, rutas, etc.)."""
    def __init__(self, id_usuario, email, password):
        self.id_usuario = id_usuario  
        self.email = email
        self.password = password


class UsuarioRepository:
    """Patrón de Diseño: Repository.
    Único responsable de interactuar con el sistema de archivos (informacion_cliente)."""
    
    def __init__(self, carpeta_raiz="informacion_cliente", nombre_fichero="perfil.txt"):
        # Hacemos las propiedades privadas (con guion bajo) para denotar encapsulamiento
        self._carpeta_raiz = carpeta_raiz
        self._nombre_fichero = nombre_fichero

    def existe_almacenamiento(self):
        """Verifica si la base de datos física existe y tiene datos."""
        return os.path.exists(self._carpeta_raiz) and os.listdir(self._carpeta_raiz)

    def obtener_ruta_perfil(self, id_usuario):
        """
        NUEVO MÉTODO ENCAPSULADO:
        Cualquier necesidad de construir rutas físicas se resuelve aquí dentro.
        Nadie fuera de esta clase sabe cómo se compone la ruta de un usuario.
        """
        return os.path.join(self._carpeta_raiz, id_usuario, self._nombre_fichero)

    def obtener_todos(self):
        """Navega por los ficheros y los transforma en una lista de Objetos Usuario."""
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
        """Método privado: Se encarga exclusivamente del parseo del archivo de texto."""
        try:
            with open(ruta_archivo, "r", encoding="utf-8") as f:
                lineas = f.readlines()

            email = None
            password = None

            for linea in lineas:
                if linea.startswith("Correo Electrónico:"):
                    email = linea.split(":")[1].strip()
                elif linea.startswith("Contraseña:"):
                    password = linea.split(":")[1].strip()

            if email and password:
                return Usuario(id_usuario=id_usuario, email=email, password=password)
        except Exception as e:
            print(f"Error crítico en repositorio leyendo {ruta_archivo}: {e}")
        return None


class LoginModel:
    """Capa de Negocio. Aplica reglas de negocio interactuando únicamente 
    con abstracciones, respetando el ocultamiento de información."""
    
    def __init__(self):
        self.repository = UsuarioRepository()

    def validar_credenciales(self, correo_ingresado, pass_ingresada):
        """Valida las credenciales sin violar el encapsulamiento del repositorio."""
        
        # 1. Regla de negocio: Verificar si hay usuarios
        if not self.repository.existe_almacenamiento():
            return False, None, "no_usuarios"

        # 2. Obtenemos entidades puras
        lista_usuarios = self.repository.obtener_todos()

        # 3. Procesamos la lógica de negocio en base a objetos
        for usuario in lista_usuarios:
            if usuario.email == correo_ingresado and usuario.password == pass_ingresada:
                # ÉXITO: Le pedimos educadamente la ruta al repositorio. 
                # El modelo ya no "adivina" ni manipula variables internas ajenas.
                ruta_usuario = self.repository.obtener_ruta_perfil(usuario.id_usuario)
                return True, ruta_usuario, None

        return False, None, None