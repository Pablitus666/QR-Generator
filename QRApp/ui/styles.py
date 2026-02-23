class QRStyles:
    BG_COLOR = "#023047"
    COLOR_BACKGROUND_DRAG_DROP = "#111E23"
    COLOR_BACKGROUND_DRAG_DROP_HOVER = "#15262D"
    COLOR_DROP_AREA_BORDER = "#3FA9C4"
    COLOR_TEXT = "#EAF6F8"
    COLOR_ACCENT = "#ffdd57"

    # Constantes para Botones (Restauradas)
    BUTTON_BG = "#023047" 
    BUTTON_FG = "white"
    BUTTON_ACTIVE_BG = "#023047"
    BUTTON_ACTIVE_FG = "#ffdd57"
    HOVER_BG = "#023047"
    HOVER_FG = "#ffdd57"

    # Tipografía (Replica de Image_Converter)
    FONT_FAMILY = "Inter"

    FONT_MAIN = (FONT_FAMILY, 12)
    FONT_BODY = (FONT_FAMILY, 10)
    FONT_BODY_BOLD = (FONT_FAMILY, 10, "bold")
    FONT_HEADER = (FONT_FAMILY, 14, "bold")
    FONT_BUTTON = (FONT_FAMILY, 10, "bold")
    FONT_STATUS_BOLD = (FONT_FAMILY, 11, "bold")

    @staticmethod
    def get_button_style(image=None):
        style = {
            'compound': 'center',
            'fg': QRStyles.BUTTON_FG,
            'font': QRStyles.FONT_BUTTON,
            'bd': 0,
            'bg': QRStyles.BUTTON_BG,
            'highlightthickness': 0,
            'relief': 'flat',
            'activebackground': QRStyles.BUTTON_ACTIVE_BG,
            'activeforeground': QRStyles.BUTTON_ACTIVE_FG,
            # Forzamos los paddings a 0 para evitar el desplazamiento del texto
            'padx': 0,
            'pady': 0,
            'borderwidth': 0
        }
        if image:
            style['image'] = image
        return style
