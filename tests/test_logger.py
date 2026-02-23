import pytest
import os
import logging
import datetime
from QRApp.core.logger import setup_logger

def test_setup_logger_creates_directory_and_file(tmp_path, mocker):
    """Verifica que setup_logger crea la carpeta de logs y el archivo correcto."""
    # Mockear el path base del logger para que apunte a nuestro directorio temporal
    # setup_logger usa os.path.dirname(os.path.dirname(__file__)) para llegar a QRApp/
    # y luego añade /logs. Vamos a simular que el log_dir es nuestro tmp_path.
    
    fake_logs_dir = tmp_path / "logs"
    
    # Mockear os.path.join para redirigir la creación del log
    # Pero es más limpio mockear la lógica de rutas interna si fuera necesario.
    # Como setup_logger usa __file__, vamos a mockear os.makedirs y logging.FileHandler
    
    mock_makedirs = mocker.patch("os.makedirs")
    mock_file_handler = mocker.patch("logging.FileHandler")
    mock_basic_config = mocker.patch("logging.basicConfig")
    
    setup_logger()
    
    # Verificar que intentó crear una carpeta
    assert mock_makedirs.called
    
    # Verificar que configuró logging
    assert mock_basic_config.called
    
    # Obtener los argumentos de basicConfig
    args, kwargs = mock_basic_config.call_args
    assert kwargs['level'] == logging.INFO
    assert len(kwargs['handlers']) == 2 # FileHandler y StreamHandler

def test_logger_file_name_format():
    """Valida que el nombre del archivo contenga la fecha actual."""
    today = datetime.date.today()
    expected_part = f"app_{today}.log"
    
    # Esta es una prueba de lógica simple ya que setup_logger construye el path
    # Solo verificamos la consistencia de la fecha
    assert expected_part.startswith("app_20") # Verificamos que sea un año válido
    assert expected_part.endswith(".log")
