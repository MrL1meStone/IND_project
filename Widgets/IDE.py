import tokenize
import keyword
import io

from tkinter import END, INSERT, TclError
from typing import Final, final

from Widgets.StylishText import StylishText
from tokenize import TokenError

def disable_scroll(event):
    return "break"


BUILTINS : Final = tuple(set(__builtins__) - set(keyword.kwlist))

QUOTES : Final = ("'", '"')

CLEANERS : Final = ("BackSpace", "Delete", "Return")

BRACKET_EVENTS : Final = ('<KeyPress-parenleft>',
                  '<KeyPress-bracketleft>',
                  '<KeyPress-braceleft>')

BRACKETS : Final = {'(': ')', '[': ']', '{': '}'}

KEYS : Final = ("<Button-4>", "<Button-5>", "<MouseWheel>",
        "<Prior>", "<Next>")

PASTE_EVENTS: Final = ("<<Paste>>", "<Control-v>", "<Control-V>", "<Button-2>", "<Button-3>")

OPERATIONS : Final = ('+', '-', '/', '//', '%', '*',
              '**', '=', '==', '!=', '>',
              '<', '>=', '<=', '[', ']',
              '{', '}', '(', ')', '"', "'", ' ')


class IDE(StylishText):
    def __init__(self, widget, style):
        super().__init__(widget, height=15,
                         width=70, fg=style.fg,
                         style=style, disabled=False)

        self.style = style

        self.bind("<Return>", self.indents)
        self.bind("<Tab>", self.move_right)
        self.bind("<KeyPress>", self.on_key)
        self.bind("<KeyPress>", self.trigger_highlight, add=True)

        self.bind("<KeyPress-ISO_Left_Tab>", self.move_left)
        self.bind("<KeyPress-BackSpace>", self.delete_spaces)
        self.bind("<KeyPress-quotedbl>", self.replace_quotes, add=True)
        self.bind("<KeyPress-apostrophe>", self.replace_quotes, add=True)
        self.bind("<KeyPress-quotedbl>", self.wrap_selected, add=True)
        self.bind("<KeyPress-apostrophe>", self.wrap_selected, add=True)

        for event in PASTE_EVENTS:
            self.bind(event, self.trigger_highlight)

        for event in BRACKET_EVENTS:
            self.bind(event, self.wrap_selected, add=True)
            self.bind(event, self.pair_brackets, add=True)

        for event in KEYS:
            self.bind(event, disable_scroll)

    @final
    def _insert_index(self):
        return tuple(map(int, self.index(INSERT).split(".")))

    @final
    def _get_selection(self):
        sel_start = self.index("sel.first")
        sel_end = self.index("sel.last")

        start_line = int(sel_start.split('.')[0])
        end_line = int(sel_end.split('.')[0])

        selection = self.get(sel_start, sel_end)
        return sel_start, sel_end, start_line, end_line, selection

    def highlight(self, event=None):
        code = self.get("1.0", "end-1c")
        for tag in ("keyword", "str", "comment", "int", "builtin", "func"):
            self.tag_remove(tag, "1.0", "end")
        try:
            tokens = tokenize.generate_tokens(io.StringIO(code).readline)
            for tok_type, tok_str, start, end, _ in tokens:
                if tok_str == "\n":
                    continue
                tag = None
                if tok_str in BUILTINS:
                    tag = "builtin"
                elif tok_str in keyword.kwlist:
                    tag = "keyword"
                elif tok_type == tokenize.STRING:
                    tag = "str"
                elif tok_type == tokenize.NUMBER:
                    tag = "int"
                elif tok_type == tokenize.COMMENT:
                    tag = "comment"
                else:
                    continue
                start = f"{start[0]}.{start[1]}"
                end = f"{end[0]}.{end[1]}"

                self.tag_add(tag, start, end)
                self.tag_configure(tag, foreground=self.style.get_color(tag))
        except TokenError as e:
            pass

    def trigger_highlight(self, event=None):
        self.after_idle(self.highlight, ())

    def indents(self, event):
        """ Автоматически создает отступы """
        line = self._insert_index()[0]
        if line >= 20:
            return "break"
        rows = self.get('1.0', END).split("\n")
        last_row = rows[line-1]
        indent = "    " * last_row.count("    ")
        extra_indent = (":" == last_row[-1]) * "    " if len(last_row)!=0 else ""
        self.insert(INSERT, "\n" + extra_indent + indent)
        return "break"

    def on_key(self, event):
        """ Ограничивает прокрутку в рамках 20 строк """
        line = self._insert_index()[0]
        if event.keysym not in CLEANERS and line >= 21:
            return "break"
        return None

    def replace_quotes(self, event):
        try:
            sel_start, sel_end, _ , _ , selection = self._get_selection()

            #Под чем я писал прошлую версию? Абсолютно нечитабельно
            types = (f'"{selection[1:-1]}"', f'"{selection[1:-1]}"')
            if selection in types:
                self.replace(sel_start, sel_end, types[types.index(selection) - 1])
            else:
                self.replace(sel_start, sel_end, f'{event.char}{selection}{event.char}')

        except TclError:
            self.insert(INSERT, event.char)
            line, char = self._insert_index()
            next_char = self.get(INSERT, f'{line}.{char + 1}')

            if not next_char or next_char in OPERATIONS:
                self.insert(INSERT, event.char)
                self.mark_set(INSERT, f'{line}.{char}')

        self.highlight()
        return "break"

    def pair_brackets(self, event):
        self.insert(INSERT, event.char)
        line, char = self._insert_index()
        next_char = self.get(INSERT, f'{line}.{char + 1}')

        if not next_char or next_char in OPERATIONS:
            self.insert(INSERT, BRACKETS[event.char])
            self.mark_set(INSERT, f'{line}.{char}')

        return "break"

    def move_right(self, event):
        try:
            _, _, start_line, end_line, _ = self._get_selection()
            for line in range(start_line, end_line + 1):
                self.insert(f"{line}.0", "    ")
        except TclError:
            self.insert(INSERT, "    ")

        return "break"

    def move_left(self, event):
        try:
            _, _, start_line, end_line, _ = self._get_selection()

            for line in range(start_line, end_line + 1):
                self.delete(f"{line}.0", f"{line}.4")
        finally:
            return "break"

    def delete_spaces(self, event):
        line, char = self._insert_index()
        if char < 4:
            return
        if self.get(f'{line}.{char - 4}', f'{line}.{char}') == "    ":
            self.delete(f"{line}.{char - 3}", f"{line}.{char}")

    def wrap_selected(self, event):
        try:
            sel_start, sel_end, _, _, selection  = self._get_selection()

            if event.char in BRACKETS.keys():
                self.replace(sel_start, float(sel_end) + 0.2,
                             f"{event.char}{selection}{BRACKETS[event.char]}")
                self.highlight()

        except TclError:
            return None
        return "break"