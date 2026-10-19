import json
from tkinter import ttk
from typing import Literal

TAG_VALUE = Literal['keyword', 'int', 'str', 'func', 'error', 'comment', 'builtin']

class CustomStyle(ttk.Style):
    def __init__(self, style_name: None | str = None):
        super().__init__()

        def _get_rgb(background) -> tuple[int]:
            return tuple([int(background[i:i + 2], 16) for i in range(1, 6, 2)])

        def _get_fg(background) -> Literal["black", "white"]:
            return 'white' if sum(_get_rgb(background)) <= 256 * 3 / 2 else "black"

        with open('Widgets/Styles.json') as file:
            styles = json.load(file)

        if style_name is None:
            style_name = styles['selected']

        self.style = styles[style_name]
        font = self.style['font']
        # --- Основные поля ---#
        self.name : str = style_name
        self.all_styles = styles
        self.font : tuple[str, int] = (font['name'], font['size'])
        self.header : tuple[str, int] = (font['name'], font['size'] + 2)
        self.bg : str = self.style['bg']
        self.second_bg : str = self.style['second_bg']
        self.fg : Literal["black", "white"] = _get_fg(self.bg)
        self.second_fg : Literal["black", "white"] = _get_fg(self.second_bg)
        # --- Синтаксис и его подсветка ---#
        syntax = self.style['syntax']
        self.keyword : str = syntax['keyword']
        self.int : str = syntax['int']
        self.str : str = syntax['str']
        self.func : str = syntax['func']
        self.error : str = syntax['error']
        self.comment : str = syntax['comment']
        self.builtin : str = syntax['builtin']

        # --- Внешний вид виджетов ---#
        self.theme_use('clam')
        self.configure('.', font=self.font, bg=self.bg, foreground=self.fg)
        self.configure('TLabel', background=self.bg, font=self.font)
        self.configure('TFrame', background=self.bg)

        self.map('TButton',
                 background=[("active", self.second_bg), ("!disabled", self.bg)],
                 foreground=[("active", self.second_fg), ("!disabled", self.fg)])

        self.configure('Green.TButton', font=self.font)
        self.map(style='Green.TButton',
                 background=[("active", '#269b40'), ("!disabled", '#1c7f31')],
                 foreground=[("active", "white"), ("!disabled", "#a0a0a0")])

    def get_color(self, tag : TAG_VALUE):
        return self.style["syntax"][tag]