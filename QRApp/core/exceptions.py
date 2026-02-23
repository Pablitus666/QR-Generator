class QRError(Exception):
    """Clase base para excepciones del QR Generator."""
    pass

class QRImageLoadError(QRError):
    """Error al cargar o procesar la imagen."""
    pass

class QRDecodeError(QRError):
    """Error al decodificar el contenido del QR."""
    pass

class QRGenerateError(QRError):
    """Error al generar el código QR."""
    pass
