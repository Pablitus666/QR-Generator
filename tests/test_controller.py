import pytest
from unittest.mock import MagicMock, patch, ANY
from QRApp.controllers.qr_controller import QRController
from QRApp.core.exceptions import QRImageLoadError
from PIL import Image
import os

@pytest.fixture
def mock_view():
    view = MagicMock()
    # Mockear el splitlist de tkinterdnd2 que usa el controller
    view.tk.splitlist.side_effect = lambda x: [x] if x and not x.startswith('{') else []
    return view

@pytest.fixture
def mock_config():
    config = MagicMock()
    config.t.side_effect = lambda key: key # Retorna la clave como traducción
    return config

@pytest.fixture
def controller(mock_view, mock_config):
    with patch('QRApp.controllers.qr_controller.QRGenerator'), \
         patch('QRApp.controllers.qr_controller.QRReader'), \
         patch('QRApp.controllers.qr_controller.FileManager'):
        return QRController(mock_view, mock_config)

def test_controller_clear(controller, mock_view):
    """Verifica que el método clear llame a la limpieza de la vista."""
    controller.clear()
    mock_view.clear_display.assert_called_once()

def test_generate_qr_dynamic_size_small(controller, mock_view):
    """Verifica el tamaño estándar para textos cortos."""
    with patch('threading.Thread') as mock_thread:
        controller.generate_qr("Short text")
        assert mock_thread.called
        target_func = mock_thread.call_args[1]['target']
        args = mock_thread.call_args[1]['args']
        target_func(*args)
        controller.generator.generate.assert_called_with("Short text", size=(1200, 1200))

def test_generate_qr_dynamic_size_large(controller, mock_view):
    """Verifica el aumento de tamaño para textos muy largos."""
    long_text = "X" * 1600
    with patch('threading.Thread') as mock_thread:
        controller.generate_qr(long_text)
        target_func = mock_thread.call_args[1]['target']
        target_func(*mock_thread.call_args[1]['args'])
        controller.generator.generate.assert_called_with(long_text, size=(2000, 2000))

def test_handle_drop_text(controller, mock_view):
    """Verifica que si se suelta texto, se actualice el entry y se genere el QR."""
    with patch.object(controller, 'generate_qr') as mock_gen:
        with patch('os.path.exists', return_value=False):
            controller.handle_drop("https://mi-url.com")
            mock_view.set_data_entry_text.assert_called_with("https://mi-url.com")
            mock_gen.assert_called_with("https://mi-url.com")

def test_handle_drop_image(controller, mock_view):
    """Verifica que si se suelta una imagen, se inicie el proceso de lectura."""
    with patch('os.path.exists', return_value=True), \
         patch('threading.Thread') as mock_thread:
        controller.handle_drop("test_qr.png")
        mock_view.set_status_loading.assert_called()
        assert mock_thread.called
        assert mock_thread.call_args[1]['target'] == controller.process_image_path

def test_save_qr_success(controller, mock_view, mock_config):
    """Verifica el flujo de guardado exitoso."""
    mock_view.has_qr_image.return_value = True
    mock_view.ask_save_directory.return_value = "/fake/path"
    mock_view.get_current_qr_image.return_value = MagicMock(spec=Image.Image)
    controller.file_manager.save_image.return_value = True
    controller.save_qr()
    # Usamos ANY en lugar de any_str
    mock_view.show_message.assert_called_with("msg_success", ANY)

def test_process_image_path_error(controller, mock_view):
    """Verifica que los errores del Core se muestren correctamente en la vista."""
    # Capturamos las llamadas a view.after para ejecutarlas manualmente
    def mock_after(ms, func, *args):
        func(*args)
    mock_view.after.side_effect = mock_after

    controller.reader.read.side_effect = QRImageLoadError("Error simulado")
    controller.process_image_path("bad_file.png")
    
    mock_view.set_status_error.assert_called()
    mock_view.show_message.assert_called_with("msg_error", "Error simulado")
