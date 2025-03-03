from tkinter import *
from config import CONFIG
import math
from decimal import Decimal, getcontext
from tkinter import Frame

# Установка точности для decimal
getcontext().prec = 10

class Calculator:
    """Класс для математических операций"""
    def __init__(self):
        getcontext().prec = 10
        
    def calculate(self, expression):
        """
        Вычисляет результат математического выражения
        
        Args:
            expression (str): Строка с математическим выражением (например, "2 + 2")
            
        Returns:
            str: Отформатированный результат вычисления
            
        Raises:
            CalculatorError: При ошибках вычисления или недопустимом выражении
        """
        try:
            # Заменяем операторы на безопасные эквиваленты
            expression = expression.replace('^', '**')
            result = eval(expression)
            return self.format_result(result)
        except ZeroDivisionError:
            raise CalculatorError("Деление на ноль!")
        except:
            raise CalculatorError("Ошибка вычисления")
            
    def format_result(self, result):
        """Форматирование результата для красивого отображения"""
        if isinstance(result, (int, float, Decimal)):
            if abs(result) > 1e10 or (abs(result) < 1e-10 and result != 0):
                return f"{result:.2e}"
            return f"{float(result):.10g}"
        return str(result)

class HistoryManager:
    """Класс для управления историей вычислений"""
    def __init__(self):
        self.history = []
        
    def add_calculation(self, expression, result):
        """Добавляет новое вычисление в историю"""
        self.history.append((expression, result))
        
    def clear(self):
        """Очищает историю вычислений"""
        self.history = []

class CalculatorError(Exception):
    """Пользовательское исключение для ошибок калькулятора"""
    pass

class CalculatorUI(Frame):
    """Класс пользовательского интерфейса"""
    def __init__(self, root):
        super().__init__(root)
        self.configure(bg=CONFIG['COLORS']['BG'])
        self.calculator = Calculator()
        self.history_manager = HistoryManager()
        self.formula = "0"
        self.build()
        self.bind_keys()
        
    def build(self):
        """Создание интерфейса калькулятора"""
        btns = [
            'x^y', 'lg', 'ln', '(', ')', 
            'C', '%', '/', 'CE', '.',
            '9', '8', '7', '6', '5',
            '4', '3', '2', '1', '0',
            '+', '-', '*', '=', '√',
        ]
        
        # Создание поля для вывода истории
        self.history = Label(self, text="", font=CONFIG['FONTS']['HISTORY'],
                           bg=CONFIG['COLORS']['BG'], foreground=CONFIG['COLORS']['HISTORY_TEXT'], 
                           anchor='e', wraplength=480)
        self.history.place(x=11, y=20, width=480)
        
        # Создание кнопок
        x = 10
        y = 140
        for bt in btns:
            com = lambda x=bt: self.logicalc(x)
            Button(self, text=bt, 
                   bg=CONFIG['COLORS']['BTN_BG'],
                   font=CONFIG['FONTS']['BUTTONS'],
                   command=com).place(x=x, y=y,
                                    width=CONFIG['LAYOUT']['BUTTON_WIDTH'],
                                    height=CONFIG['LAYOUT']['BUTTON_HEIGHT'])
            x += CONFIG['LAYOUT']['BUTTON_SPACING']
            if x > 400:
                x = 10
                y += CONFIG['LAYOUT']['BUTTON_HEIGHT']
        
        # Создание поля для вывода текущего выражения
        self.lbl = Label(self, text=self.formula, 
                         font=CONFIG['FONTS']['MAIN'],
                         bg=CONFIG['COLORS']['BG'], 
                         foreground=CONFIG['COLORS']['TEXT'])
        self.lbl.place(x=11, y=50)

    def bind_keys(self):
        """Привязка клавиш к функциям калькулятора"""
        self.master.bind('<Return>', lambda event: self.logicalc('='))
        self.master.bind('<Escape>', lambda event: self.logicalc('C'))
        self.master.bind('<BackSpace>', self.handle_backspace)
        # Цифры
        for i in range(10):
            self.master.bind(str(i), lambda event, num=i: self.logicalc(str(num)))
        # Операторы
        self.master.bind('+', lambda event: self.logicalc('+'))
        self.master.bind('-', lambda event: self.logicalc('-'))
        self.master.bind('*', lambda event: self.logicalc('*'))
        self.master.bind('/', lambda event: self.logicalc('/'))
        self.master.bind('^', lambda event: self.logicalc('x^y'))
        self.master.bind('(', lambda event: self.logicalc('('))
        self.master.bind(')', lambda event: self.logicalc(')'))

    def handle_backspace(self, event):
        """Обработка нажатия клавиши Backspace"""
        if len(self.formula) > 0:
            self.formula = self.formula[:-1]
            if not self.formula:
                self.formula = "0"
            self.update()

    def logicalc(self, operation):
        if operation == "C":
            self.formula = "0"
            self.history.configure(text="")
        elif operation == "CE":
            self.formula = "0"
        elif operation == "√":
            try:
                self.history.configure(text=f"√({self.formula})")
                result = float(eval(self.formula)) ** 0.5
                self.formula = self.calculator.format_result(result)
            except:
                self.formula = "Ошибка"
        elif operation == "x^y":
            self.formula += "^"
        elif operation == "lg":
            try:
                self.history.configure(text=f"lg({self.formula})")
                result = math.log10(float(eval(self.formula)))
                self.formula = self.calculator.format_result(result)
            except:
                self.formula = "Ошибка"
        elif operation == "ln":
            try:
                self.history.configure(text=f"ln({self.formula})")
                result = math.log(float(eval(self.formula)))
                self.formula = self.calculator.format_result(result)
            except:
                self.formula = "Ошибка"
        elif operation == "=":
            try:
                self.history.configure(text=self.formula)
                self.formula = self.calculator.calculate(self.formula)
            except CalculatorError as e:
                self.formula = str(e)
            except:
                self.formula = "Ошибка"
        else:
            if self.formula == "0" and operation not in ['.', '-']:
                self.formula = ""
            self.formula += operation
        self.update()

    def update(self):
        if self.formula == "":
            self.formula = "0"
        display_text = self.formula
        if len(display_text) > 20:
            display_text = "..." + display_text[-17:]
        self.lbl.configure(text=display_text)

