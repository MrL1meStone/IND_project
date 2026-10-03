import tokenize
import keyword
import io

from tkinter import END, INSERT, TclError
from Widgets.StylishText import StylishText
from tokenize import TokenError


def disable_scroll(event):
    return "break"


QUOTES = ("'", '"')

CLEANERS = ("BackSpace", "Delete", "Return")

BRACKET_EVENTS = ('<KeyPress-parenleft>',
                  '<KeyPress-bracketleft>',
                  '<KeyPress-braceleft>')

BRACKETS = ('(', ')', '[', ']', '{', '}')

KEYS = ("<Button-4>", "<Button-5>", "<MouseWheel>",
        "<Up>", "<Down>", "<Prior>", "<Next>")

OPERATIONS = ('+', '-', '/', '//', '%', '*',
              '**', '=', '==', '!=', '>',
              '<', '>=', '<=', '[', ']',
              '{', '}', '(', ')', '"', "'", ' ')


class IDE(StylishText):
    def __init__(self, widget, style):
        super().__init__(widget, height=15,
                         width=70, fg=style.fg,
                         style=style, disabled=False)

        self.style = style

        self.tag_configure("keyword", foreground=self.style.keyword)
        self.tag_configure("string", foreground=self.style.str)
        self.tag_configure("comment", foreground=self.style.comment)
        self.tag_configure("number", foreground=self.style.int)

        self.bind("<Return>", self.indents)
        self.bind("<Tab>", self.move_right)
        self.bind("<KeyPress>", self.on_key)
        self.bind("<KeyPress>", self.trigger_highlight, add=True)

        self.bind("<<Paste>>", self.trigger_highlight)
        self.bind("<Control-v>", self.trigger_highlight)
        self.bind("<Control-V>", self.trigger_highlight)
        self.bind("<Button-2>", self.trigger_highlight)
        self.bind("<Button-3>", self.trigger_highlight)

        self.bind("<KeyPress-ISO_Left_Tab>", self.move_left)
        self.bind("<KeyPress-BackSpace>", self.delete_spaces)
        self.bind("<KeyPress-quotedbl>", self.replace_quotes, add=True)
        self.bind("<KeyPress-apostrophe>", self.replace_quotes, add=True)
        self.bind("<KeyPress-quotedbl>", self.wrap_selected, add=True)
        self.bind("<KeyPress-apostrophe>", self.wrap_selected, add=True)

        for i in BRACKET_EVENTS:
            self.bind(i, self.wrap_selected, add=True)
            self.bind(i, self.pair_brackets, add=True)

        for i in KEYS:
            self.bind(i, disable_scroll)

    def insert_index(self):
        return self.index(INSERT).split(".")

    def highlight(self, event=None):
        code = self.get("1.0", "end-1c")
        for tag in ("keyword", "string", "comment", "number"):
            self.tag_remove(tag, "1.0", "end")
        try:
            tokens = tokenize.generate_tokens(io.StringIO(code).readline)
            for tok_type, tok_str, start, end, _ in tokens:
                tag = None
                if tok_str in keyword.kwlist:
                    tag = "keyword"
                elif tok_type == tokenize.STRING:
                    tag = "string"
                elif tok_type == tokenize.NUMBER:
                    tag = "number"
                elif tok_type == tokenize.COMMENT:
                    tag = "comment"

                if tag is None:
                    continue

                start = f"{start[0]}.{start[1]}"
                end = f"{end[0]}.{end[1]}"

                self.tag_add(tag, start, end)
        except TokenError:
            pass

    def trigger_highlight(self, event=None):
        self.after_idle(self.highlight, ())

    def indents(self, event):
        """ Автоматически создает отступы в
         соответствии с требованиями python """
        line = self.insert_index()[0]
        if int(line) >= 20:
            return "break"
        rows = self.get('1.0', END)
        last_row = rows.split("\n")[-2]
        indent = "    " * last_row.count("    ")
        extra_indent = (":\n" == rows[-2:]) * "    "
        self.insert(INSERT, "\n" + extra_indent + indent)
        return "break"

    def on_key(self, event):
        line = self.insert_index()[0]
        if event.keysym not in CLEANERS and int(line) >= 21:
            return "break"
        return None

    def replace_quotes(self, event):
        try:
            sel_start = self.index("sel.first")
            sel_end = self.index("sel.last")
            selection = self.get(sel_start, sel_end)
            if selection == f'"{selection[1:-1]}"':
                self.replace(sel_start, sel_end, f"'{selection[1:-1]}'")
            elif selection == f"'{selection[1:-1]}'":
                self.replace(sel_start, sel_end, f'"{selection[1:-1]}"')
            else:
                self.replace(sel_start, sel_end, f'{event.char}{selection}{event.char}')
        except TclError:
            self.insert(INSERT, event.char)
            line, char = self.insert_index()
            next_char = self.get(INSERT, f'{line}.{int(char) + 1}')

            if not next_char or next_char in OPERATIONS:
                self.insert(INSERT, event.char)
                self.mark_set(INSERT, f'{line}.{int(char)}')

        self.highlight()
        return "break"

    def pair_brackets(self, event):
        self.insert(INSERT, event.char)
        line, char = self.insert_index()
        next_char = self.get(INSERT, f'{line}.{int(char) + 1}')

        if not next_char or next_char in OPERATIONS:
            for i in range(0, 6, 2):
                if BRACKETS[i] == event.char:
                    self.insert(INSERT, BRACKETS[i + 1])
            self.mark_set(INSERT, f'{line}.{int(char)}')

        return "break"

    def move_right(self, event):
        try:
            sel_start = self.index("sel.first")
            sel_end = self.index("sel.last")

            start_line = int(sel_start.split('.')[0])
            end_line = int(sel_end.split('.')[0])
            for line in range(start_line, end_line + 1):
                self.insert(f"{line}.0", "    ")
        except TclError:
            self.insert(INSERT, "    ")

        return "break"

    def move_left(self, event):
        try:
            sel_start = self.index("sel.first")
            sel_end = self.index("sel.last")

            start_line = int(sel_start.split('.')[0])
            end_line = int(sel_end.split('.')[0])
            for line in range(start_line, end_line + 1):
                self.delete(f"{line}.0", f"{line}.4")
        finally:
            return "break"

    def delete_spaces(self, event):
        line, char = map(int, self.index("insert").split('.'))
        if char < 4:
            return
        if self.get(f'{line}.{char - 4}', f'{line}.{char}') == "    ":
            self.delete(f"{line}.{char - 3}", f"{line}.{char}")

    def wrap_selected(self, event):
        try:
            sel_start = self.index("sel.first")
            sel_end = self.index("sel.last")
            selection = self.get(sel_start, sel_end)

            for i in range(0, 6, 2):
                if event.char == BRACKETS[i]:
                    self.replace(sel_start, float(sel_end) + 0.2, f"{event.char}{selection}{BRACKETS[i + 1]}")
                    self.highlight()

        except TclError:
            return None
        return "break"