import tkinter as tk
from tkinter import filedialog
from tkinterdnd2 import DND_FILES, DND_TEXT, TkinterDnD
from PIL import Image, ImageTk
import os

from QRApp.ui.styles import QRStyles
from QRApp.ui.widgets import HoverButton
from QRApp.ui.dialogs import show_info, show_custom_messagebox
from QRApp.ui.assets import AssetManager
from QRApp.ui.image_enhancer import ImageManager
from QRApp.utils.window_utils import centrar_ventana
from QRApp.controllers.qr_controller import QRController
from QRApp.core.config_manager import ConfigManager
from QRApp.utils.path_utils import get_resource_path

class QRApp(TkinterDnD.Tk):
    def __init__(self):
        super().__init__()
        # 0. INVISIBILIDAD ATÓMICA: Ocultar y hacer transparente
        self.withdraw()
        self.attributes("-alpha", 0.0)
        
        # Sincronización OLE (Crítico para que el sistema reconozca el área de drop)
        # Se hace mientras la ventana está oculta e invisible
        self.update() 
        
        # Detectar factor de escala DPI
        self.scaling_factor = self.tk.call('tk', 'scaling') / 1.3333333333333333
        
        # 1. Configuración de dependencias (Single Source of Truth)
        self.config_manager = ConfigManager()
        self.image_manager = ImageManager(self.scaling_factor)
        
        # 2. Inicializar Controlador (Inyección de dependencias)
        self.controller = QRController(self, self.config_manager)
        
        # 3. Referencias de Estado UI
        self.current_qr_image = None
        self.photo_image_ref = None 

        # 4. Configuración inicial de ventana
        self.title(self.config_manager.t("app_title"))
        self.config(bg=QRStyles.BG_COLOR)
        self.resizable(False, False)
        
        self._setup_window()
        self._load_enhanced_assets()
        self._create_widgets()
        
        self.bind('<Delete>', lambda e: self.controller.clear())

        # 5. REVELACIÓN ATÓMICA: Restaurar opacidad y mostrar
        self.update_idletasks()
        self.attributes("-alpha", 1.0)
        self.deiconify()

    def _setup_window(self):
        try:
            # ICONO OPTIMIZADO PARA LA VENTANA PRINCIPAL (32x32)
            # Esto asegura nitidez en Alt+Tab y en la esquina de la ventana
            icon_path = get_resource_path(os.path.join('assets', 'images', 'favicon32.ico'))
            
            if os.path.exists(icon_path):
                # Aplicamos a la ventana principal
                self.iconbitmap(icon_path)
                # Establecemos favicon16.ico como default para que las ventanas hijas
                # se vean nítidas en su versión pequeña de 16x16
                small_icon_path = get_resource_path(os.path.join('assets', 'images', 'favicon16.ico'))
                if os.path.exists(small_icon_path):
                    self.iconbitmap(default=small_icon_path)
        except Exception as e:
            print(f"Error configurando iconos: {e}")
        
        centrar_ventana(self, 500, 640)

    def _load_enhanced_assets(self):
        """Carga los activos con mejoras visuales y caché."""
        self.button_img_tk = self.image_manager.load(
            AssetManager.get_path('boton.png'), 
            size=(100, 40), 
            apply_shadow=True, 
            shadow_offset=(2, 2),
            shadow_alpha=120,
            preserve_aspect=False
        )
        self.logo_img_tk = self.image_manager.load(
            AssetManager.get_path('logo.png'), 
            size=(100, 100), 
            apply_shadow=True, 
            shadow_offset=(3, 3),
            shadow_alpha=100,
            preserve_aspect=True
        )
        self.drag_drop_icon_photo = self.image_manager.load(
            AssetManager.get_path('drag_drop_icon.png'), 
            size=(64, 64)
        )
        hover_scale = 1.1
        hover_size = (int(64 * hover_scale), int(64 * hover_scale))
        self.drag_drop_icon_hover_photo = self.image_manager.load(
            AssetManager.get_path('drag_drop_icon.png'), 
            size=hover_size
        )

    def _create_widgets(self):
        # 1. Campo de Entrada
        tk.Label(self, text=self.config_manager.t("enter_data"), bg=QRStyles.BG_COLOR, fg='white', 
                 font=QRStyles.FONT_HEADER).grid(row=0, column=0, columnspan=2, pady=10)

        self.data_entry = tk.Entry(self, width=50, font=QRStyles.FONT_MAIN, relief='flat')
        self.data_entry.grid(row=1, column=0, columnspan=2, ipady=5, padx=20)
        self.data_entry.drop_target_register(DND_TEXT)
        self.data_entry.dnd_bind('<<Drop>>', self._on_text_drop)
        self.data_entry.bind('<KeyPress>', self._on_data_entry_typing)

        # 2. Botones de Acción
        btn_style = QRStyles.get_button_style(self.button_img_tk)
        self.btn_generate = HoverButton(self, text=self.config_manager.t("btn_generate"), command=self._on_generate_click, **btn_style)
        self.btn_generate.grid(row=2, column=0, padx=10, pady=10)

        self.btn_save = HoverButton(self, text=self.config_manager.t("btn_save"), command=self.controller.save_qr, **btn_style)
        self.btn_save.grid(row=2, column=1, padx=10, pady=10)

        self.btn_clear = HoverButton(self, text=self.config_manager.t("btn_clear"), command=self.controller.clear, **btn_style)
        self.btn_clear.grid(row=3, column=0, padx=10, pady=10)

        self.btn_exit = HoverButton(self, text=self.config_manager.t("btn_exit"), command=self.quit, **btn_style)
        self.btn_exit.grid(row=3, column=1, padx=10, pady=10)

        # 3. Logo (Acerca de)
        if self.logo_img_tk:
            logo_label = tk.Label(self, image=self.logo_img_tk, bg=QRStyles.BG_COLOR)
            logo_label.place(x=200, y=90) 
            logo_label.bind("<Button-1>", lambda e: show_info(self, self.image_manager))

        # 4. Campo de Lectura
        self.read_data_entry = tk.Entry(self, width=50, font=QRStyles.FONT_MAIN, relief='flat', state="readonly")
        self.read_data_entry.grid(row=4, column=0, columnspan=2, ipady=5, padx=20, pady=10)

        # 5. Área de Visualización QR y Drag & Drop
        self.preview_frame = tk.Frame(self, width=280, height=280, bg=QRStyles.COLOR_BACKGROUND_DRAG_DROP)
        self.preview_frame.grid(row=5, column=0, columnspan=2, pady=15)
        self.preview_frame.pack_propagate(False)

        self.drop_area = tk.Label(self.preview_frame, text=self.config_manager.t("drag_drop_text"),
                                  font=QRStyles.FONT_BODY, bg=QRStyles.COLOR_BACKGROUND_DRAG_DROP, fg=QRStyles.COLOR_TEXT,
                                  relief="ridge", bd=4, cursor="hand2", anchor="center",
                                  highlightbackground=QRStyles.COLOR_DROP_AREA_BORDER, highlightthickness=3,
                                  image=self.drag_drop_icon_photo, compound="top")
        self.drop_area.image = self.drag_drop_icon_photo
        self.drop_area.pack(fill="both", expand=True)

        # 6. Label de Estado
        self.status_label = tk.Label(self, text=self.config_manager.t("status_ready"), font=QRStyles.FONT_STATUS_BOLD,
                                     fg=QRStyles.COLOR_TEXT, bg=QRStyles.BG_COLOR, wraplength=480, height=2, anchor="n")
        self.status_label.grid(row=6, column=0, columnspan=2, pady=5)

        self._bind_drag_drop()
        self.grid_rowconfigure(5, weight=1)
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

    # --- Handlers UI (Delegación al Controlador) ---
    def _on_generate_click(self):
        self.controller.generate_qr(self.data_entry.get())

    def _bind_drag_drop(self):
        """Configura los eventos y delega el manejo al controlador."""
        self.drop_area.drop_target_register(DND_FILES, DND_TEXT)
        self.drop_area.dnd_bind("<<Drop>>", self._on_drop_event)
        
        # 1. EVENTOS DE ARRASTRE (DND) - Crítico para cuando se arrastran archivos
        self.drop_area.dnd_bind("<<DropEnter>>", self._on_drag_enter)
        self.drop_area.dnd_bind("<<DropLeave>>", self._on_drag_leave)
        
        # 2. EVENTOS DE RATÓN NORMAL - Crítico para cuando NO se arrastran archivos
        self.drop_area.bind("<Enter>", self._on_drag_enter)
        self.drop_area.bind("<Leave>", self._on_drag_leave)
        
        # 3. CLIC PARA ABRIR EXPLORADOR
        self.drop_area.bind("<Button-1>", lambda e: self.controller.read_qr())

    def _on_drop_event(self, event):
        """Delega el evento de soltar datos al controlador."""
        self.reset_drop_area_ui()
        self.controller.handle_drop(event.data)

    def _on_data_entry_typing(self, event):
        """Si el usuario escribe, limpiamos la sesión anterior."""
        if event.keysym in ('Control_L', 'Control_R', 'Shift_L', 'Shift_R', 'Alt_L', 'Alt_R', 'Left', 'Right', 'Up', 'Down'):
            return
        if self.current_qr_image is not None or self.read_data_entry.get():
             self.clear_display_results_only()

    def _on_text_drop(self, event):
        if self.current_qr_image is not None or self.read_data_entry.get():
             self.clear_display_results_only()
        data = event.data.strip('{}')
        self.set_data_entry_text(data)

    def _on_drag_enter(self, event):
        """Maneja el resaltado visual al entrar en el área."""
        if self.current_qr_image is None:
            self.drop_area.config(
                text=self.config_manager.t("drag_drop_hover"), 
                image=self.drag_drop_icon_hover_photo, 
                font=QRStyles.FONT_BODY_BOLD, 
                bg=QRStyles.COLOR_BACKGROUND_DRAG_DROP_HOVER
            )
            self.drop_area.image = self.drag_drop_icon_hover_photo

    def _on_drag_leave(self, event):
        """Maneja la restauración visual al salir del área."""
        if self.current_qr_image is None:
            self.reset_drop_area_ui()

    # --- Métodos de Soporte para el Controlador ---
    def has_qr_image(self) -> bool:
        """Indica si hay un QR cargado actualmente."""
        return self.current_qr_image is not None

    def get_current_qr_image(self) -> Image.Image:
        """Retorna la imagen del QR actual."""
        return self.current_qr_image

    def show_message(self, title: str, message: str):
        """Muestra un diálogo de mensaje (Encapsula implementación UI)."""
        show_custom_messagebox(self, title, message)

    def set_data_entry_text(self, text: str):
        """Actualiza el campo de entrada superior."""
        self.data_entry.delete(0, tk.END)
        self.data_entry.insert(0, text)

    def set_status_loading(self):
        self.status_label.config(text=self.config_manager.t("status_loading"))

    def set_status_error(self):
        self.status_label.config(text=self.config_manager.t("status_error"))

    def reset_drop_area_ui(self):
        """Restaura el estado visual original."""
        self.drop_area.config(text=self.config_manager.t("drag_drop_text"), image=self.drag_drop_icon_photo, 
                                  font=QRStyles.FONT_BODY, bg=QRStyles.COLOR_BACKGROUND_DRAG_DROP, compound="top")
        self.drop_area.image = self.drag_drop_icon_photo

    def update_qr_display(self, img: Image.Image):
        """Muestra el QR en pantalla con persistencia y redibujo."""
        try:
            self.current_qr_image = img
            display_img = img.copy()
            display_img.thumbnail((250, 250), Image.Resampling.LANCZOS)
            photo = ImageTk.PhotoImage(display_img)
            self.photo_image_ref = photo
            self.drop_area.image = photo
            self.drop_area.config(image=photo, text="", compound="center")
            self.drop_area.update_idletasks()
            self.status_label.config(text=self.config_manager.t("status_success"))
        except Exception as e:
            print(f"Error al actualizar pantalla: {e}")
            self.set_status_error()

    def set_read_data(self, data: str):
        self.read_data_entry.config(state='normal')
        self.read_data_entry.delete(0, tk.END)
        self.read_data_entry.insert(0, data)
        self.read_data_entry.config(state='readonly')

    def clear_display_results_only(self):
        """Limpia solo los resultados visuales, preservando la entrada del usuario."""
        self.photo_image_ref = None
        self.current_qr_image = None
        self.reset_drop_area_ui()
        self.read_data_entry.config(state='normal')
        self.read_data_entry.delete(0, tk.END)
        self.read_data_entry.config(state='readonly')
        self.status_label.config(text=self.config_manager.t("status_ready"))

    def clear_display(self):
        """Limpia la interfaz completa."""
        self.data_entry.delete(0, tk.END)
        self.clear_display_results_only()

    def ask_save_directory(self) -> str:
        return filedialog.askdirectory()

    def ask_open_file(self) -> str:
        return filedialog.askopenfilename(filetypes=[(self.config_manager.t("file_types"), "*.png;*.jpg;*.jpeg;*.bmp;*.gif")])
