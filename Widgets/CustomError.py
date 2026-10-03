from tkinter import ttk
from Widgets.StylishText import StylishText
from Widgets.CustomStyle import CustomStyle
from Widgets.BaseWindow import BaseWindow

class CustomError(BaseWindow):
    def __init__(self, text: str, style : CustomStyle):
        super().__init__(0.7,0.4)
        self.title("Ошибка!")
        StylishText(self,style, height=15, width=100,
                    fg=style.error, bg=style.second_bg, disabled=True, text=text).pack(fill='both', expand=True,padx=10, pady=10)
        ttk.Button(self,text="Ок",
                   command=self.destroy, width=15, style='Custom.TButton').pack(pady=10)