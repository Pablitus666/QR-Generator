import qrcode
from PIL import Image

class QRGenerator:
    def __init__(self, version=None, error_correction=qrcode.constants.ERROR_CORRECT_M, box_size=10, border=6):
        self.version = version
        self.error_correction = error_correction
        self.box_size = box_size
        self.border = border

    def generate(self, data: str, fill_color="black", back_color="white", size: tuple[int, int] | None = (1200, 1200)) -> Image.Image:
        """
        Genera una imagen QR a partir de los datos proporcionados.
        Lanza ValueError si los datos están vacíos.
        """
        if not data or not data.strip():
            raise ValueError("Los datos para generar el QR no pueden estar vacíos.")

        qr = qrcode.QRCode(
            version=self.version,
            error_correction=self.error_correction,
            box_size=self.box_size,
            border=self.border,
        )
        qr.add_data(data)
        qr.make(fit=True)

        img = qr.make_image(fill_color=fill_color, back_color=back_color)
        
        # Convertir a imagen PIL para asegurar compatibilidad
        img = img.convert("RGB")
        
        # Solo redimensionar si se proporciona un tamaño específico
        if size:
            # Asegurar que el tamaño sean enteros
            target_size = (int(size[0]), int(size[1]))
            # Usamos NEAREST para códigos QR porque es instantáneo y mantiene los bordes afilados
            img = img.resize(target_size, Image.Resampling.NEAREST)
        
        return img
