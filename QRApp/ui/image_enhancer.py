from PIL import Image, ImageChops, ImageTk
import os
import tkinter as tk
from typing import Optional, Tuple, Dict

def add_shadow(image: Image.Image, offset: Tuple[int, int] = (2, 2), shadow_color: Tuple[int, int, int, int] = (0, 0, 0, 90)) -> Image.Image:
    """
    Añade un efecto de sombra a una imagen PIL creando un lienzo equilibrado
    para que el contenido original permanezca en el centro exacto.
    """
    if image.mode != 'RGBA':
        image = image.convert('RGBA')

    # Crear la máscara de sombra
    alpha_mask = image.split()[-1]
    r, g, b, alpha_value = shadow_color
    shadow_img_rgb = Image.new('RGB', image.size, (r, g, b))
    target_alpha = Image.new('L', alpha_mask.size, color=alpha_value)
    scaled_alpha_mask = ImageChops.darker(alpha_mask, target_alpha)
    final_shadow_image = shadow_img_rgb.copy()
    final_shadow_image.putalpha(scaled_alpha_mask)

    # Lógica de Lienzo Equilibrado:
    # Para que el botón esté en el centro, añadimos el offset en ambos lados
    abs_x = abs(offset[0])
    abs_y = abs(offset[1])
    
    canvas_width = image.width + abs_x * 2
    canvas_height = image.height + abs_y * 2
    
    # Crear lienzo transparente
    enhanced_image = Image.new('RGBA', (canvas_width, canvas_height), (0, 0, 0, 0))

    # Pegar la imagen original exactamente en el centro
    original_paste_x = abs_x
    original_paste_y = abs_y

    # Pegar la sombra desplazada desde el centro
    shadow_paste_x = original_paste_x + offset[0]
    shadow_paste_y = original_paste_y + offset[1]

    enhanced_image.paste(final_shadow_image, (shadow_paste_x, shadow_paste_y), final_shadow_image)
    enhanced_image.paste(image, (original_paste_x, original_paste_y), image)

    return enhanced_image

class ImageManager:
    def __init__(self, scaling_factor: float = 1.0):
        self._cache: Dict[tuple, ImageTk.PhotoImage] = {}
        self._refs = []
        self.scaling_factor = scaling_factor

    def clear_cache(self):
        """Limpia el caché de imágenes y libera referencias."""
        self._cache.clear()
        self._refs.clear()

    def load(self, path: str, size: Optional[Tuple[int, int]] = None, 
             apply_shadow: bool = False, shadow_offset: Tuple[int, int] = (3, 3),
             shadow_alpha: int = 100, preserve_aspect: bool = True) -> Optional[ImageTk.PhotoImage]:
        
        cache_key = (path, size, apply_shadow, shadow_offset, shadow_alpha, preserve_aspect)
        if cache_key in self._cache:
            return self._cache[cache_key]

        if not os.path.exists(path):
            return None

        try:
            image = Image.open(path).convert("RGBA")

            if size:
                # Escalado inteligente basado en el DPI del monitor
                target_w = int(size[0] * self.scaling_factor)
                target_h = int(size[1] * self.scaling_factor)
                
                if preserve_aspect:
                    orig_w, orig_h = image.size
                    ratio = min(target_w / orig_w, target_h / orig_h)
                    new_size = (int(orig_w * ratio), int(orig_h * ratio))
                    image = image.resize(new_size, Image.Resampling.LANCZOS)
                else:
                    image = image.resize((target_w, target_h), Image.Resampling.LANCZOS)

            if apply_shadow:
                image = add_shadow(image, offset=shadow_offset, shadow_color=(0, 0, 0, shadow_alpha))

            photo = ImageTk.PhotoImage(image)
            self._cache[cache_key] = photo
            self._refs.append(photo)
            
            return photo

        except Exception as e:
            print(f"Error procesando imagen {path}: {e}")
            return None
