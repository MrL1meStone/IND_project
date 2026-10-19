from tkinter import Text
from Testing.randfuncs import randstr

from Widgets.CustomStyle import CustomStyle


class StylishText(Text):
	def __init__(self, widget,
	             style : CustomStyle,
	             height : int,
	             width : int,
	             text : str | None = None,
	             disabled : bool = True,
	             selection : bool = True,
	             fg: str | None = None,
	             bg: str | None = None):

		if not bg:
			bg=style.second_bg

		if not fg:
			fg = style.fg

		super().__init__(widget, height=height, width=width, border=0.0,
		                 bd=0, highlightthickness=0, bg=bg,
		                 font=style.font, foreground=fg, insertbackground=style.second_fg)

		self.style = style
		self.fg = fg

		if text:
			self.insert("1.0", text)

		if disabled:
			self.configure(state='disabled', exportselection=False)

		if not selection:
			def disable_selection(event):
				self.tag_remove("sel", "1.0", "end")
				return "break"

			self.bind("<<Selection>>", disable_selection)
			self.bind("<ButtonRelease-1>", disable_selection)
			self.bind("<B1-Motion>", disable_selection)
			self.bind("<Shift-Left>", disable_selection)
			self.bind("<Shift-Right>", disable_selection)
			self.bind("<Control-a>", disable_selection)

	def color_index(self, index1: str, index2: str, color) -> None:
		tag_name = f'{index1}:{index2}'
		self.tag_add(tag_name, f'{index1}', f'{index2}')
		self.tag_configure(tag_name, foreground=color)