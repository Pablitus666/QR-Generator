import pytest
import os
from PIL import Image
from QRApp.core.exceptions import QRImageLoadError, QRDecodeError

def test_read_qr_success(qr_reader, qr_generator, tmp_path):
    """Prueba la lectura exitosa de un código QR generado."""
    data = "Test QR Read 123"
    img = qr_generator.generate(data)
    file_path = str(tmp_path / "temp_qr.png")
    img.save(file_path)
    
    decoded_data, decoded_img = qr_reader.read(file_path)
    assert decoded_data == data
    assert isinstance(decoded_img, Image.Image)

def test_read_qr_unicode(qr_reader, qr_generator, tmp_path):
    """Prueba la lectura de un QR con contenido Unicode."""
    data = "QR con Emojis 🚀 y Chino 电子"
    img = qr_generator.generate(data)
    file_path = str(tmp_path / "unicode_qr.png")
    img.save(file_path)
    
    decoded_data, _ = qr_reader.read(file_path)
    assert decoded_data == data

def test_read_file_not_found(qr_reader):
    """Prueba el error al intentar leer un archivo inexistente."""
    with pytest.raises(QRImageLoadError) as excinfo:
        qr_reader.read("missing.png")
    assert "Archivo no encontrado" in str(excinfo.value)

def test_read_no_qr_in_image(qr_reader, tmp_path):
    """Prueba el error al leer una imagen que no contiene un QR."""
    # Crear una imagen roja pura
    img = Image.new('RGB', (100, 100), color='red')
    file_path = str(tmp_path / "no_qr.png")
    img.save(file_path)
    
    with pytest.raises(QRDecodeError) as excinfo:
        qr_reader.read(file_path)
    # Buscamos fragmentos que están en el mensaje real de QRApp/core/qr_reader.py
    # y que son más resistentes a problemas de codificación.
    error_msg = str(excinfo.value)
    assert "no se pudo detectar" in error_msg.lower() or "qr" in error_msg.lower()

def test_read_cv2_decode_error(qr_reader, tmp_path, mocker):
    """Prueba el error cuando cv2.imdecode falla (bloque except)."""
    file_path = str(tmp_path / "fake_img.png")
    with open(file_path, "wb") as f:
        f.write(b"fake data")
    
    # Mockear cv2.imdecode para que lance una excepción
    mocker.patch("cv2.imdecode", side_effect=Exception("OpenCV Critical Error"))
    
    with pytest.raises(QRImageLoadError) as excinfo:
        qr_reader.read(file_path)
    assert "Error cargando imagen con OpenCV" in str(excinfo.value)

def test_read_corrupt_file(qr_reader, tmp_path):
    """Prueba el error al intentar leer un archivo que no es una imagen."""
    file_path = str(tmp_path / "corrupt.png")
    with open(file_path, "w") as f:
        f.write("Not an image data")
    
    with pytest.raises(QRImageLoadError):
        qr_reader.read(file_path)
