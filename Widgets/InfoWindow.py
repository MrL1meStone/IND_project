from tkinter import PhotoImage, ttk
from Widgets.BaseWindow import BaseWindow


class InfoWindow(BaseWindow):
    def __init__(self, name : str, text: str,  warning : bool = False):
        super().__init__(0.35, 0.25)
        self.title(name)

        main_frame = ttk.Frame(self)
        if warning:
            self.image = PhotoImage(file="pics/warning.png")
        else:
            self.image = PhotoImage(file="pics/info.png")

        ttk.Label(text=text, font=self.style.header, master=main_frame, image = self.image).pack(side="left", padx=10)
        ttk.Label(text=text, font=self.style.header, master=main_frame).pack(side="left", padx=10)
        main_frame.pack(pady=(100, 70))
        ttk.Button(self, text="Ок",
                   command=self.destroy, width=15, style='Custom.TButton').pack(pady=10)
