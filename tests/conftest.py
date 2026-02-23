import pytest
import sys
import os

# Asegurar que QRApp sea importable desde el directorio raíz
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from QRApp.core.qr_generator import QRGenerator
from QRApp.core.qr_reader import QRReader
from QRApp.core.file_manager import FileManager
from QRApp.core.config_manager import ConfigManager

@pytest.fixture
def qr_generator():
    return QRGenerator()

@pytest.fixture
def qr_reader():
    return QRReader()

@pytest.fixture
def file_manager():
    return FileManager()

@pytest.fixture
def config_manager():
    # ConfigManager es un Singleton, retornamos la instancia
    return ConfigManager()
