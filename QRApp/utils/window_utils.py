import tkinter as tk

def centrar_ventana(ventana: tk.Toplevel | tk.Tk, ancho: int, alto: int):
    """
    Centra una ventana en la pantalla.
    """
    pantalla_ancho = ventana.winfo_screenwidth()
    pantalla_alto = ventana.winfo_screenheight()
    x = (pantalla_ancho // 2) - (ancho // 2)
    y = (pantalla_alto // 2) - (alto // 2)
    ventana.geometry(f"{ancho}x{alto}+{x}+{y}")
    ventana.update_idletasks()
