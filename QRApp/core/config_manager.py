import json
import os
import logging
import sys
from typing import Dict, Any, Tuple, Optional
from QRApp.utils.path_utils import get_resource_path

class ConfigManager:
    _instance = None
    _config = {}
    _lang_data = {}

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(ConfigManager, cls).__new__(cls)
            cls._instance._load_config()
            cls._instance._load_lang()
        return cls._instance

    def _get_system_language(self) -> str:
        """Detecta el idioma del sistema operativo de forma robusta."""
        try:
            # Intentar obtener el locale por defecto (ej: 'es_ES')
            import locale
            # getdefaultlocale() suele ser más fiable para códigos ISO cortos en Windows
            # aunque esté marcado como deprecated en versiones muy nuevas.
            lang_tuple = locale.getdefaultlocale()
            system_locale = lang_tuple[0] if lang_tuple else None
            
            if not system_locale:
                # Fallback a getlocale() si el anterior falla
                system_locale = locale.getlocale()[0]

            if system_locale:
                # Manejar formatos tipo 'es_ES' o 'es-ES'
                lang_code = system_locale.split('_')[0].split('-')[0].lower()
                
                # Mapeo de nombres largos a códigos ISO si es necesario
                mapping = {
                    'spanish': 'es', 'english': 'en', 'german': 'de', 
                    'french': 'fr', 'italian': 'it', 'japanese': 'ja', 
                    'portuguese': 'pt', 'russian': 'ru', 'chinese': 'zh'
                }
                
                # Si el código detectado es un nombre largo, lo traducimos
                if lang_code in mapping:
                    lang_code = mapping[lang_code]
                
                # Si es un código ISO pero más largo de 2 caracteres (ej: 'spa'), 
                # tomamos los primeros 2 si coinciden con nuestros locales.
                if len(lang_code) > 2:
                    lang_code = lang_code[:2]

                logging.info(f"Idioma del sistema detectado y normalizado: {lang_code}")
                return lang_code
        except Exception as e:
            logging.warning(f"No se pudo detectar el idioma del sistema: {e}")
        return "en" 

    def _load_config(self):
        try:
            # El archivo config.json permanece en la carpeta de lógica core/
            config_path = get_resource_path(os.path.join('QRApp', 'core', 'config.json'))
            if os.path.exists(config_path):
                with open(config_path, 'r', encoding='utf-8') as f:
                    self._config = json.load(f)
            
            self.current_lang = self._get_system_language()
        except Exception as e:
            logging.error(f"Error cargando config: {e}")
            self._config = {"theme": "dark"}
            self.current_lang = self._get_system_language()

    def _load_lang(self):
        try:
            lang = self.current_lang
            # Los locales se movieron a la nueva ubicación assets/locales/
            locales_dir = get_resource_path(os.path.join('assets', 'locales'))
            lang_path = os.path.join(locales_dir, f'{lang}.json')
            
            if not os.path.exists(lang_path):
                logging.warning(f"Idioma {lang} no disponible. Usando fallback 'en'.")
                lang = "en"
                lang_path = os.path.join(locales_dir, 'en.json')

            if os.path.exists(lang_path):
                with open(lang_path, 'r', encoding='utf-8') as f:
                    self._lang_data = json.load(f)
            else:
                logging.error(f"No se encontró ningún archivo de idioma en: {lang_path}")
                self._lang_data = {}
        except Exception as e:
            logging.error(f"Error cargando idioma: {e}")
            self._lang_data = {}

    def get(self, key: str, default=None) -> Any:
        return self._config.get(key, default)

    def set(self, key: str, value: Any):
        if key == "language":
            return
        self._config[key] = value
        self.save()

    def save(self):
        try:
            config_path = get_resource_path(os.path.join('QRApp', 'core', 'config.json'))
            temp_config = self._config.copy()
            if "language" in temp_config:
                del temp_config["language"]
            with open(config_path, 'w', encoding='utf-8') as f:
                json.dump(temp_config, f, indent=4)
        except Exception as e:
            logging.error(f"Error guardando config: {e}")

    def t(self, key: str) -> str:
        """Devuelve una cadena traducida."""
        return self._lang_data.get(key, key)
