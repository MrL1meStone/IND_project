from tkinter import Tk, Toplevel

from Widgets.CustomStyle import CustomStyle


class BaseWindow(Toplevel):
    def __init__(self, weight_percent, height_percent):
        super().__init__()
        screen_weight, screen_height = self.wm_maxsize()
        size = (int(screen_weight * weight_percent), int(screen_height * height_percent))
        self.size = size
        self.geometry(f"{size[0]}x{size[1]}"
                      f"+{(screen_weight - size[0]) // 2}"
                      f"+{(screen_height - size[1]) // 2}")

        self.style = CustomStyle()
        self.configure(bg=self.style.bg)
