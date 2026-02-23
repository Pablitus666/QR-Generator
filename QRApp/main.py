import sys
import os
import ctypes
import tkinter

# 1. High-DPI
try:
    if sys.platform == 'win32':
        ctypes.windll.shcore.SetProcessDpiAwareness(1)
        myappid = 'Pablitus.QRGenerator.1.0' 
        ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)
except Exception:
    pass

# 2. Rutas de PyInstaller
if hasattr(sys, '_MEIPASS'):
    bundle_dir = sys._MEIPASS
    if bundle_dir not in sys.path:
        sys.path.insert(0, bundle_dir)
    qrapp_path = os.path.join(bundle_dir, 'QRApp')
    if qrapp_path not in sys.path:
        sys.path.insert(0, qrapp_path)
    
    # PARCHE CRÍTICO PARA TKDND
    import platform
    arch = "win64" if platform.system() == "Windows" else ("osx64" if platform.system() == "Darwin" else "linux64")
    # Intentamos localizar la carpeta tkdnd en la raíz del bundle (como se define en el .spec)
    tkdnd_path = os.path.join(bundle_dir, 'tkdnd', arch)
    if os.path.exists(tkdnd_path):
        os.environ['TKDND_LIBRARY'] = tkdnd_path
else:
    current_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(current_dir)
    if project_root not in sys.path:
        sys.path.insert(0, project_root)
    if current_dir not in sys.path:
        sys.path.insert(0, current_dir)

# 4. Importaciones
try:
    from QRApp.ui.app import QRApp
except ImportError:
    from ui.app import QRApp

def main():
    try:
        app = QRApp()
        app.mainloop()
    except Exception as e:
        import traceback
        error_info = f"Error crítico:\n{str(e)}\n\n{traceback.format_exc()}"
        if sys.platform == 'win32':
            try:
                from tkinter import messagebox
                err_root = tkinter.Tk()
                err_root.withdraw()
                messagebox.showerror("QR Generator - Error Fatal", error_info)
                err_root.destroy()
            except:
                print(error_info)

if __name__ == "__main__":
    main()
