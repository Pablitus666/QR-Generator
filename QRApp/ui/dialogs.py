import tkinter as tk
from tkinter import Toplevel
from PIL import Image, ImageTk
import os

from QRApp.ui.styles import QRStyles
from QRApp.ui.assets import AssetManager
from QRApp.utils.window_utils import centrar_ventana
from QRApp.ui.widgets import HoverButton
from QRApp.core.config_manager import ConfigManager

def show_custom_messagebox(parent, title, message):
    if hasattr(parent, 'custom_messagebox') and parent.custom_messagebox and parent.custom_messagebox.winfo_exists():
        parent.custom_messagebox.lift()
        return

    config_manager = ConfigManager()
    dialog = Toplevel(parent)
    # INVISIBILIDAD INMEDIATA
    dialog.withdraw()
    dialog.attributes("-alpha", 0.0)
    
    parent.custom_messagebox = dialog
    
    dialog.title(title)
    dialog.config(bg=QRStyles.BG_COLOR)
    dialog.resizable(False, False)
    
    # El icono ya se propaga desde el main app por iconbitmap(default=...)
    # Pero lo reforzamos para asegurar nitidez usando el favicon de 16x16
    try:
        icon_path = AssetManager.get_path('favicon16.ico')
        if os.path.exists(icon_path):
            dialog.iconbitmap(icon_path)
    except Exception as e:
        print(f"Error cargando icono en el diálogo: {e}")

    # CONFIGURAMOS LA GEOMETRÍA ANTES DE CREAR CONTENIDOS QUE PUEDAN FORZAR DIBUJADO
    centrar_ventana(dialog, 300, 180)

    tk.Label(dialog, text=message, bg=QRStyles.BG_COLOR, fg='white', 
             font=QRStyles.FONT_MAIN, wraplength=250).pack(pady=20)

    btn_img_tk = parent.image_manager.load(
        AssetManager.get_path('boton.png'), 
        size=(100, 40), 
        apply_shadow=True, 
        shadow_offset=(2, 2),
        shadow_alpha=120,
        preserve_aspect=False
    )
    
    btn_style = QRStyles.get_button_style(btn_img_tk)
    HoverButton(dialog, text=config_manager.t("btn_ok"), command=dialog.destroy, **btn_style).pack(pady=10)

    # REVELACIÓN ATÓMICA: Forzar el cálculo de geometría antes de mostrar
    dialog.update_idletasks()
    dialog.attributes("-alpha", 1.0)
    dialog.deiconify()

def show_info(parent, image_manager):
    """
    Muestra la ventana de información replicando la estética de Wifi_Scanner.
    """
    if hasattr(parent, 'info_window') and parent.info_window and parent.info_window.winfo_exists():
        parent.info_window.lift()
        return

    config_manager = ConfigManager()
    info_win = Toplevel(parent)
    # INVISIBILIDAD TOTAL INMEDIATA
    info_win.withdraw()
    info_win.attributes("-alpha", 0.0)
    
    parent.info_window = info_win
    
    info_win.title(config_manager.t("info_title"))
    info_win.config(bg=QRStyles.BG_COLOR)
    info_win.resizable(False, False)

    # El icono ya se propaga desde el main app por iconbitmap(default=...)
    try:
        icon_path = AssetManager.get_path('favicon16.ico')
        if os.path.exists(icon_path):
            info_win.iconbitmap(icon_path)
    except Exception as e:
        print(f"Error cargando icono en la ventana de información: {e}")

    # Frame principal con la misma configuración de Wifi_Scanner
    frame = tk.Frame(info_win, bg=QRStyles.BG_COLOR)
    frame.pack(padx=10, pady=10, fill="both", expand=True)

    # Configuración de Grid
    frame.grid_rowconfigure(0, weight=1)
    frame.grid_rowconfigure(1, weight=1)
    frame.grid_rowconfigure(2, weight=1)
    frame.grid_columnconfigure(0, weight=1)
    frame.grid_columnconfigure(1, weight=1)

    # Robot: 150x150
    robot_photo = image_manager.load(
        AssetManager.get_path('robot.png'), 
        size=(150, 150), 
        apply_shadow=False, 
        preserve_aspect=True
    )
    
    if robot_photo:
        img_label = tk.Label(frame, image=robot_photo, bg=QRStyles.BG_COLOR, bd=0, highlightthickness=0)
        img_label.image = robot_photo
        img_label.grid(row=0, column=0, rowspan=3, padx=(0, 10), pady=5, sticky="nsew")

    # Texto
    message_text = config_manager.t("info_message")
    message = tk.Label(
        frame,
        text=message_text,
        justify="center",
        bg=QRStyles.BG_COLOR,
        fg='white',
        font=QRStyles.FONT_HEADER,
        anchor="center",
        wraplength=170
    )
    message.grid(row=0, column=1, rowspan=2, padx=(0, 25), pady=(10, 10), sticky="nsew")

    # Botón Cerrar: 120x45
    btn_img_tk = image_manager.load(
        AssetManager.get_path('boton.png'), 
        size=(120, 45), 
        apply_shadow=True, 
        shadow_offset=(2, 2),
        shadow_alpha=120,
        preserve_aspect=False
    )
    btn_style = QRStyles.get_button_style(btn_img_tk)

    close_btn = HoverButton(frame, text=config_manager.t("btn_close"), command=info_win.destroy, **btn_style)
    close_btn.grid(row=2, column=1, padx=(0, 10), pady=(15, 10), sticky="s")

    # Dimensiones finales: 375 x 225
    centrar_ventana(info_win, 375, 225)
    
    # REVELACIÓN ATÓMICA: Tras haber centrado en silencio
    info_win.update_idletasks()
    info_win.attributes("-alpha", 1.0)
    info_win.deiconify()
    info_win.lift()
