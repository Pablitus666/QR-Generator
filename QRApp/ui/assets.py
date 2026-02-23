import os
import logging
from QRApp.utils.path_utils import get_resource_path

class AssetManager:
    @classmethod
    def get_path(cls, filename: str) -> str:
        """
        Devuelve la ruta absoluta a un archivo de asset (imagen, icono).
        Busca en la nueva estructura centralizada 'assets/images/'.
        Utiliza el helper dinámico get_resource_path para máxima compatibilidad.
        """
        path = get_resource_path(os.path.join('assets', 'images', filename))
        
        if not os.path.exists(path):
            logging.warning(f"No se encontró el asset: {path}")
        return path
