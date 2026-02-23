import os
from PIL import Image
from QRApp.core.exceptions import QRError

class FileManager:
    def save_image(self, image: Image.Image, path: str) -> bool:
        """
        Guarda una imagen PIL en la ruta especificada.
        Lanza QRError si falla.
        """
        try:
            image.save(path)
            return True
        except Exception as e:
            raise QRError(f"Error al guardar imagen en {path}: {str(e)}")

    def load_image(self, path: str) -> Image.Image:
        """
        Carga una imagen PIL desde la ruta especificada.
        """
        if not os.path.exists(path):
            raise FileNotFoundError(f"El archivo {path} no existe.")
        try:
            return Image.open(path)
        except Exception as e:
            raise QRError(f"Error al cargar imagen: {str(e)}")
