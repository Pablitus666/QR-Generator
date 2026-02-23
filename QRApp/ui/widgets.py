import tkinter as tk
from QRApp.ui.styles import QRStyles

class HoverButton(tk.Button):
    def __init__(self, master=None, **kwargs):
        if 'bg' not in kwargs:
            kwargs['bg'] = QRStyles.BUTTON_BG
        if 'fg' not in kwargs:
            kwargs['fg'] = QRStyles.BUTTON_FG
        if 'activebackground' not in kwargs:
            kwargs['activebackground'] = QRStyles.BUTTON_ACTIVE_BG
        if 'activeforeground' not in kwargs:
            kwargs['activeforeground'] = QRStyles.BUTTON_ACTIVE_FG
        
        # Bloqueamos el salto de texto y centramos
        kwargs['relief'] = 'flat'
        kwargs['borderwidth'] = 0
        kwargs['bd'] = 0
        kwargs['padx'] = 0
        kwargs['pady'] = 0
        kwargs['highlightthickness'] = 0
        kwargs['takefocus'] = 0
        kwargs['anchor'] = "center" # Asegura el centrado absoluto
        
        super().__init__(master, **kwargs)
        self.bind("<Enter>", self.on_enter)
        self.bind("<Leave>", self.on_leave)

    def on_enter(self, e):
        self.config(bg=QRStyles.HOVER_BG, fg=QRStyles.HOVER_FG)

    def on_leave(self, e):
        self.config(bg=QRStyles.BUTTON_BG, fg=QRStyles.BUTTON_FG)
