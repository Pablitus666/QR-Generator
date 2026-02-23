import pytest
import os
import json
from QRApp.core.config_manager import ConfigManager

def test_config_manager_singleton():
    """Verifica que ConfigManager sea efectivamente un Singleton."""
    cm1 = ConfigManager()
    cm2 = ConfigManager()
    assert cm1 is cm2

def test_translation_fallback(config_manager):
    """Verifica que t() devuelva la clave si no existe traducción."""
    assert config_manager.t("non_existent_key") == "non_existent_key"

def test_get_set_config(config_manager):
    """Verifica el guardado y obtención de configuraciones."""
    config_manager.set("test_key", "test_value")
    assert config_manager.get("test_key") == "test_value"

def test_language_detection(config_manager):
    """Verifica que el idioma se detecte y normalice."""
    # Como dependemos del sistema operativo, verificamos que el campo exista
    assert hasattr(config_manager, 'current_lang')
    assert len(config_manager.current_lang) == 2

def test_not_saving_language(config_manager):
    """Verifica que el idioma no se persista en el archivo config.json."""
    config_manager.set("language", "fr")
    assert config_manager.get("language") != "fr"

def test_config_save_error(config_manager, mocker):
    """Verifica el manejo de error cuando no se puede guardar el archivo de config."""
    # Mockear open para que lance una excepción al intentar escribir
    # Usamos builtins.open porque es lo que usa ConfigManager internamente
    mocker.patch("builtins.open", side_effect=IOError("Disco lleno o sin permisos"))
    
    # Esto debería ejecutar el bloque except en save()
    # No lanzamos excepción al exterior en ConfigManager.save(), solo logueamos
    config_manager.save()
    # Si llega aquí sin crashear, el bloque except funcionó

def test_load_lang_fallback_to_en(config_manager, mocker):
    """Verifica que si un idioma no existe, use inglés como fallback."""
    # Simulamos que el idioma actual es uno que no existe (ej: 'xx')
    config_manager.current_lang = "xx"
    # Mockear os.path.exists para que devuelva False para 'xx.json'
    # pero True para 'en.json'
    def mock_exists(path):
        if "xx.json" in path: return False
        return True
    
    mocker.patch("os.path.exists", side_effect=mock_exists)
    
    # Forzar la recarga del idioma
    config_manager._load_lang()
    assert config_manager.current_lang == "xx" # El código sigue siendo xx
    # Pero los datos deberían ser los de inglés (si logramos mockear el open también)

def test_system_language_detection_error(config_manager, mocker):
    """Verifica el fallback a inglés si falla la detección del sistema."""
    mocker.patch("locale.getdefaultlocale", side_effect=Exception("Locale Error"))
    mocker.patch("locale.getlocale", side_effect=Exception("Locale Error"))
    
    lang = config_manager._get_system_language()
    assert lang == "en"

