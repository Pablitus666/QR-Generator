import pytest
import os
from PIL import Image
from QRApp.core.exceptions import QRError

def test_save_image_success(file_manager, tmp_path):
    """Prueba el guardado exitoso de una imagen."""
    img = Image.new('RGB', (100, 100), color='red')
    file_path = str(tmp_path / "test_qr.png")
    
    result = file_manager.save_image(img, file_path)
    assert result is True
    assert os.path.exists(file_path)

def test_save_image_error(file_manager, mocker):
    """Prueba el manejo de errores al guardar (mockeando excepción)."""
    img = Image.new('RGB', (10, 10))
    # Mockear el método save de PIL.Image para que lance error
    mocker.patch.object(Image.Image, "save", side_effect=Exception("Permiso denegado"))
    
    with pytest.raises(QRError) as excinfo:
        file_manager.save_image(img, "invalid/path/test.png")
    assert "Error al guardar imagen" in str(excinfo.value)

def test_load_image_success(file_manager, tmp_path):
    """Prueba la carga exitosa de una imagen."""
    img_orig = Image.new('RGB', (50, 50), color='blue')
    file_path = str(tmp_path / "load_test.png")
    img_orig.save(file_path)
    
    img_loaded = file_manager.load_image(file_path)
    assert isinstance(img_loaded, Image.Image)
    assert img_loaded.size == (50, 50)

def test_load_image_not_found(file_manager):
    """Prueba el error al cargar un archivo inexistente."""
    with pytest.raises(FileNotFoundError):
        file_manager.load_image("non_existent_file.png")
