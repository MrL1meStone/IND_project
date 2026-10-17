import json

from tkinter import ttk, Tk
from tkinter import StringVar, Variable, Listbox
from tkinter import END
from Testing.module_tests import check_output
from Testing.module_writer import make_module
from Questions.Easy import easy_questions
from Questions.Normal import normal_questions
from Questions.Hard import hard_questions
from Widgets.StylishText import StylishText
from Widgets.CustomError import CustomError
from Widgets.CustomStyle import CustomStyle
from Widgets.InfoWindow import InfoWindow
from Widgets.IDE import IDE

QUESTIONS = [easy_questions, normal_questions, hard_questions]


class MainWindow(Tk):
    def __init__(self):
        super().__init__()
        screen_weight, screen_height = self.wm_maxsize()
        size = (int(screen_weight * 0.5), int(screen_height * 0.6))
        self.size : tuple[int, int] = size
        self.geometry(f"{size[0]}x{size[1]}"
                      f"+{(screen_weight - size[0]) // 2}"
                      f"+{(screen_height - size[1]) // 2}")

        self.style : CustomStyle = CustomStyle()
        self.configure(bg=self.style.bg)
        self.title("Тест по знанию Python")
        self.resizable(width=False, height=False)

        # Переменные
        self.current_question : int = 0
        self.difficulty : int = 0
        self.question_text : StringVar = StringVar()
        self.summary : list[bool | None] = [None] * 10

    def menu(self) -> None:
        for widget in self.winfo_children():
            widget.destroy()

        def set_difficulty(difficulty: int) -> None:
            self.difficulty = difficulty
            self.current_question = 0
            self.summary = [None] * 10
            self.add_text()

        # Само меню
        ttk.Label(text='Выберите сложность', font=self.style.header).pack(pady=(100, 70))
        for i, text in enumerate(['Легкий', 'Средний', 'Сложный']):
            ttk.Button(self, text=text, command=lambda x= i: set_difficulty(x), width=20).pack(pady=10)

        # Выбор темы
        ttk.Label(text='Или посмотрите темы', font=self.style.header).pack(pady=(100, 70))
        ttk.Button(text='Темы', width=20, command=self.styles).pack(pady=10)

    def add_text(self):
        """Меню с вопросами."""
        for widget in self.winfo_children():
            widget.destroy()

        def move_question(step):
            """Навигация по вопросам."""
            if -1 < self.current_question + step < 10:
                self.current_question += step
                self.add_text()

        # --- Весь фрейм включая вопрос, кнопку меню и результат тестов --- #

        main_frame = ttk.Frame(self)

        technical_bar = ttk.Frame(main_frame)
        ttk.Button(technical_bar, text='< Меню', command=self.menu
                   ).grid(column=0, row=0, pady=10, padx=10)

        progress_bar = StylishText(technical_bar,
                     text=f"{'● ' * 10}\n{"  "*self.current_question}^",
                     bg=self.style.bg, style=self.style, height=2, width=20, selection=False)
        def color_progress_bar():
            for i in range(10):
                if self.summary[i]:
                    color = "#269b40"
                elif self.summary[i] == False:
                    color = self.style.error
                else:
                    color = "#FFFFFF"
                progress_bar.color_index(color=color, index1=f"1.{i * 2}",
                                         index2=f"1.{i * 2 + 1}")
        color_progress_bar()
        progress_bar.grid(column=2, row=0, pady=10, padx=10)
        technical_bar.grid_columnconfigure(1, weight=10)
        technical_bar.pack(fill='x', expand=True, padx=10)

        questions_frame = ttk.Frame(main_frame)

        # --- Редактор кода вместе с кнопками --- #
        code_space = ttk.Frame(questions_frame)

        # --- Полоса нумерации строк --- #
        code_frame = ttk.Frame(code_space)
        numbers = StylishText(code_frame, height=20,
                              width=3, style=self.style,
                              fg='gray', selection=False)
        numbers.pack(side='left', fill='y')
        numbers.configure(state='normal')
        for i in range(19):
            numbers.insert(END, f'{i + 1: ^3}\n')
        numbers.insert(END, '20 ')
        numbers.configure(state='disabled')
        # --- Полоса нумерации строк --- #

        # --- Сам редактор кода --- #
        self.question_text.set(QUESTIONS[self.difficulty][self.current_question]['text'])
        label = ttk.Label(code_space, textvariable=self.question_text, font=self.style.header)
        label.pack(pady=40)
        ide = IDE(code_frame, style=self.style)
        ide.pack(anchor='center', side='left', fill="both")
        # --- Сам редактор кода --- #

        code_frame.pack()
        # --- Редактор кода вместе с кнопками --- #

        # --- Полоса кнопок для вопросов --- #
        def check():
            """ Проверяет написанный код через stdin / stdout """
            make_module(ide.get('1.0', END))
            question = QUESTIONS[self.difficulty][self.current_question]
            right, error_text = check_output(input_func = question['args'], output_func=question['func'])
            if right and self.current_question < 11:
                self.summary[self.current_question] = True
                self.current_question += 1
                self.add_text()
                InfoWindow(name="Верный ответ!", text="Код работает!")
                return


            if error_text:
                CustomError(error_text, self.style)

            if not right and not error_text:
                InfoWindow(name="Неверный ответ!", text="Код работает, но не выполняет свою функцию",
                           warning=True)

            self.summary[self.current_question] = False
            color_progress_bar()


        button_menu = ttk.Frame(code_space)
        button_menu.columnconfigure(3)
        check_button = ttk.Button(button_menu, text='Проверить', takefocus=False,
                                  command=check, width=15, style='Green.TButton')

        next_question = ttk.Button(button_menu, text='Вперед >', takefocus=False,
                                   command=lambda: move_question(1), width=10)

        previous = ttk.Button(button_menu, text='< Назад', takefocus=False,
                              command=lambda: move_question(-1), width=10)

        previous.grid(row=0, column=0, pady=10, padx=10)
        check_button.grid(row=0, column=1, pady=10, padx=10)
        next_question.grid(row=0, column=2, pady=10, padx=10)
        button_menu.pack(ipady=10, ipadx=5, pady=0, padx=10, anchor='center')
        # --- Полоса кнопок для вопросов --- #

        code_space.pack(side='left', fill='y', expand=True, padx=10)
        questions_frame.pack(anchor='center')
        main_frame.pack(anchor='center', expand=True)
        # --- Весь фрейм включая вопрос, кнопку меню и результат тестов --- #

    def styles(self):
        """Страничка стилей: добавление стилей, управление ими, и прочее"""
        for widget in self.winfo_children():
            widget.destroy()

        def menu_wrapper():
            with open('Widgets/Styles.json', 'r', encoding='utf-8') as file:
                style_name = json.load(file)['selected']

            self.style = CustomStyle(style_name)
            self.configure(bg=self.style.bg)
            self.menu()

        def set_theme(event):
            theme = combo.get(*combo.curselection())
            if theme == self.style.name:
                return

            # --- Изменение текущей темы ---#
            with open('Widgets/Styles.json', "r") as file:
                styles = json.load(file)
                styles['selected'] = theme

            with open('Widgets/Styles.json', "w") as file:
                file.write(json.dumps(styles, indent=2))

            for i in widgets_frame.winfo_children():
                i.destroy()

            self.style = CustomStyle(theme)
            self.configure(bg=self.style.bg)
            self.styles()

        main_frame = ttk.Frame(self)
        # --- Выбор тем ---#
        ttk.Button(self, text='< Меню', command=menu_wrapper
                   ).pack(anchor='nw', pady=100, padx=100)
        style_frame = ttk.Frame(main_frame)
        themes = tuple(self.style.all_styles.keys())
        variable = Variable(value=themes[1:])
        combo = Listbox(style_frame, background=self.style.bg, font=self.style.font,
                        foreground=self.style.fg, listvariable=variable,
                        selectmode='single', height=min(4, len(themes) - 1))

        combo.bind("<<ListboxSelect>>", set_theme)
        combo.pack(pady=10)
        style_frame.pack(fill='y', side='left', padx=10)
        # --- Выбор тем ---#

        # --- Превью темы ---#
        widgets_frame = ttk.Frame(main_frame)
        StylishText(widgets_frame, text=f'\n{'Пример текста': ^20}\n',
                    style=self.style, height=3, width=20,
                    disabled=True, selection=False).pack(side='top', fill='x')

        bottom_frame = ttk.Frame(widgets_frame)
        ttk.Button(bottom_frame, text='Кнопка').pack(side='left')
        ttk.Label(bottom_frame, text='Текст').pack(side='left', padx=20)
        bottom_frame.pack(fill='x')
        widgets_frame.pack(side='left', fill='y', padx=10)
        # --- Превью темы ---#

        main_frame.pack(anchor='center')


def main():
    window = MainWindow()
    window.menu()
    window.mainloop()


if __name__ == "__main__":
    main()
