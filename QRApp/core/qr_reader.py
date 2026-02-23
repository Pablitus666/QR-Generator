import cv2
from PIL import Image
import os
import numpy as np
from QRApp.core.exceptions import QRImageLoadError, QRDecodeError

class QRReader:
    def read(self, file_path: str) -> tuple[str, Image.Image]:
        """
        Lee una imagen QR y devuelve los datos decodificados y la imagen en formato PIL.
        Lanza excepciones en caso de error.
        Soporta rutas Unicode en Windows.
        """
        if not os.path.exists(file_path):
            raise QRImageLoadError(f"Archivo no encontrado: {file_path}")

        # Uso de imdecode para soportar rutas con caracteres especiales/Unicode en Windows
        try:
            # Leer el archivo como un array de bytes
            with open(file_path, 'rb') as f:
                file_bytes = np.frombuffer(f.read(), dtype=np.uint8)
            img = cv2.imdecode(file_bytes, cv2.IMREAD_COLOR)
        except Exception as e:
            raise QRImageLoadError(f"Error cargando imagen con OpenCV: {str(e)}")

        if img is None:
            raise QRImageLoadError("No se pudo decodificar la imagen.")

        detector = cv2.QRCodeDetector()
        data, bbox, _ = detector.detectAndDecode(img)

        if not data:
            # Intentar con una versión en escala de grises para mejorar detección
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            data, bbox, _ = detector.detectAndDecode(gray)
            
            if not data:
                raise QRDecodeError("No se pudo detectar un código QR válido en la imagen. Asegúrese de que la imagen sea nítida y el QR sea visible.")

        # Convertir a PIL Image para mostrar en la UI
        img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        img_pil = Image.fromarray(img_rgb)
        
        return data, img_pil
