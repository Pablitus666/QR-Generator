import os
import threading
from QRApp.core.qr_generator import QRGenerator
from QRApp.core.qr_reader import QRReader
from QRApp.core.file_manager import FileManager
from QRApp.core.config_manager import ConfigManager
from QRApp.core.exceptions import QRError

class QRController:
    def __init__(self, view, config_manager: ConfigManager):
        self.view = view
        self.config_manager = config_manager
        self.generator = QRGenerator()
        self.reader = QRReader()
        self.file_manager = FileManager()
        
        # Sincronización y control de flujo
        self._lock = threading.Lock()
        self._is_processing = False

    def handle_drop(self, raw_data: str):
        """Lógica de negocio para manejar el arrastre inteligente de datos."""
        if not raw_data or self._is_processing:
            return

        files = self.view.tk.splitlist(raw_data)
        
        if len(files) == 1:
            clean_path = files[0].strip('{}')
            if os.path.exists(clean_path):
                if clean_path.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp', '.gif')):
                    self.view.set_status_loading()
                    threading.Thread(target=self.process_image_path, args=(clean_path,), daemon=True).start()
                else:
                    self.view.set_status_error()
                    self.view.show_message(
                        self.config_manager.t("msg_error"), 
                        self.config_manager.t("msg_unsupported_format")
                    )
                return
        
        text_to_generate = raw_data.strip('{}')
        self.view.set_data_entry_text(text_to_generate)
        self.generate_qr(text_to_generate)

    def generate_qr(self, data: str):
        """Inicia la generación de QR en un hilo separado con control de flujo."""
        if not data:
            self.view.show_message(self.config_manager.t("msg_input_error"), self.config_manager.t("msg_no_data"))
            return

        if self._is_processing:
            return

        self.view.set_status_loading()
        threading.Thread(target=self._generate_worker, args=(data,), daemon=True).start()

    def _generate_worker(self, data: str):
        """Worker de generación con cálculo de densidad en bytes."""
        with self._lock:
            self._is_processing = True
            try:
                # El estándar QR depende de bytes (UTF-8 es el estándar moderno)
                data_bytes_len = len(data.encode('utf-8'))
                
                target_size = (1200, 1200)
                if data_bytes_len > 1500:
                    target_size = (2000, 2000)
                elif data_bytes_len > 500:
                    target_size = (1600, 1600)

                img = self.generator.generate(data, size=target_size)
                self.view.after(0, self.view.update_qr_display, img)
            except Exception as e:
                msg = self.config_manager.t("msg_error_generate").format(str(e))
                self.view.after(0, self.view.set_status_error)
                self.view.after(0, self.view.show_message, self.config_manager.t("msg_error"), msg)
            finally:
                self._is_processing = False

    def save_qr(self):
        """Guarda la imagen QR actual usando la interfaz pública de la vista."""
        if not self.view.has_qr_image():
            self.view.show_message(self.config_manager.t("msg_save_error"), self.config_manager.t("msg_no_qr"))
            return

        directory_path = self.view.ask_save_directory()
        if directory_path:
            filename = f"{self.config_manager.t('default_filename')}.png"
            full_path = os.path.join(directory_path, filename)
            
            qr_image = self.view.get_current_qr_image()
            if self.file_manager.save_image(qr_image, full_path):
                self.view.show_message(self.config_manager.t("msg_success"), f"{self.config_manager.t('msg_saved_at')} {full_path}")
            else:
                self.view.show_message(self.config_manager.t("msg_error"), self.config_manager.t("msg_error_save"))

    def read_qr(self):
        """Lee un código QR en segundo plano."""
        if self._is_processing:
            return

        file_path = self.view.ask_open_file()
        if not file_path:
            return
            
        self.view.set_status_loading()
        threading.Thread(target=self.process_image_path, args=(file_path,), daemon=True).start()

    def process_image_path(self, file_path: str):
        """Worker de lectura con protección de estado."""
        with self._lock:
            self._is_processing = True
            try:
                data, img = self.reader.read(file_path)
                self.view.after(0, lambda: self._finalize_reading(data, img))
            except QRError as e:
                self.view.after(0, self.view.set_status_error)
                self.view.after(0, self.view.show_message, self.config_manager.t("msg_error"), str(e))
            except Exception as e:
                msg = self.config_manager.t("msg_error_process").format(str(e))
                self.view.after(0, self.view.set_status_error)
                self.view.after(0, self.view.show_message, self.config_manager.t("msg_error"), msg)
            finally:
                self._is_processing = False

    def _finalize_reading(self, data, img):
        self.view.set_read_data(data)
        self.view.update_qr_display(img)

    def clear(self):
        """Limpia la vista (Solo si no está procesando)."""
        if not self._is_processing:
            self.view.clear_display()
