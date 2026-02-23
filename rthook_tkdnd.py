import os
import sys

# Este hook solo configura la variable de entorno. 
# La inyección en auto_path la hará el parche que aplicamos a TkinterDnD.py
if hasattr(sys, '_MEIPASS'):
    import platform
    p = "win64" if platform.system() == "Windows" else ("osx64" if platform.system() == "Darwin" else "linux64")
    tkdnd_root = os.path.join(sys._MEIPASS, 'tkdnd', p)
    
    if os.path.exists(tkdnd_root):
        os.environ['TKDND_LIBRARY'] = tkdnd_root
