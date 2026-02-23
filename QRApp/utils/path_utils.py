import sys
import os

def get_resource_path(relative_path: str) -> str:
    """
    Obtiene la ruta absoluta compatible con PyInstaller.
    Funciona tanto en el entorno de desarrollo como en el ejecutable empaquetado.
    """
    if hasattr(sys, "_MEIPASS"):
        # PyInstaller crea una carpeta temporal y almacena su ruta en _MEIPASS
        base_path = sys._MEIPASS
    else:
        # En desarrollo, buscamos la carpeta raíz que contiene la carpeta 'assets'
        # Empezamos desde la ubicación de este archivo y subimos niveles hasta encontrarla
        current_dir = os.path.dirname(os.path.abspath(__file__))
        # Subimos desde 'QRApp/utils/' hasta la raíz del proyecto
        base_path = os.path.abspath(os.path.join(current_dir, '..', '..'))
        
        # Validación de seguridad: si no existe assets en esa base_path, 
        # probamos un nivel arriba (por si acaso se ejecuta de forma inusual)
        if not os.path.exists(os.path.join(base_path, 'assets')):
            base_path = os.path.abspath(os.path.join(base_path, '..'))

    return os.path.join(base_path, relative_path)
