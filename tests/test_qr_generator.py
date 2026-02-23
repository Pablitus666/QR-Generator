import pytest
from PIL import Image

def test_generate_basic(qr_generator):
    """Prueba la generación básica de un QR."""
    img = qr_generator.generate("https://google.com")
    assert isinstance(img, Image.Image)
    assert img.size == (1200, 1200)

def test_generate_unicode(qr_generator):
    """Prueba la generación con caracteres Unicode complejos."""
    data = "Hola Mundo! 🌎 日本語 QR"
    img = qr_generator.generate(data)
    assert isinstance(img, Image.Image)

def test_generate_long_text(qr_generator):
    """Prueba la generación con una gran cantidad de datos."""
    data = "X" * 2000
    # Usamos un tamaño mayor para texto largo como definimos en el controller
    img = qr_generator.generate(data, size=(2000, 2000))
    assert isinstance(img, Image.Image)
    assert img.size == (2000, 2000)

def test_generate_custom_colors(qr_generator):
    """Prueba la generación con colores personalizados."""
    img = qr_generator.generate("Test Colors", fill_color="red", back_color="yellow")
    assert isinstance(img, Image.Image)
    # Verificamos que sea RGB tras la conversión
    assert img.mode == "RGB"

def test_generate_no_resize(qr_generator):
    """Prueba la generación sin redimensionado (tamaño nativo)."""
    img = qr_generator.generate("Native Size", size=None)
    assert isinstance(img, Image.Image)
    # El tamaño nativo de un QR v1 con border 6 y box 10 es (21+12)*10 = 330
    assert img.size[0] == img.size[1]
