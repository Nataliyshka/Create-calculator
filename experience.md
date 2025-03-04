# Создание калькулятора на Python с использованием библиотеки Tkinter

1. **Файл config**

   Первое что мы делаем - создаем файл config.py

   Для чего он необходим?

   Данный файл необходим для хранения основных настроек пользовательского интерфейса таких как:
   \- используемые цвета;

   \- размеры;

   \- параметры.

```python
CONFIG = {
    'COLORS': {
        'BG': '#000',
        'BTN_BG': '#FFF',
        'TEXT': '#FFF',
        'HISTORY_TEXT': '#888'
    },
    'FONTS': {
        'MAIN': ("Times New Roman", 21, "bold"),
        'HISTORY': ("Times New Roman", 12),
        'BUTTONS': ("Times New Roman", 15)
    },
    'LAYOUT': {
        'WINDOW_SIZE': '500x700+200+200',
        'BUTTON_WIDTH': 115,
        'BUTTON_HEIGHT': 79,
        'BUTTON_SPACING': 117
    }
}
```


2. **Файл model**

Следующим действием для нашего калькулятора будет создание фала model.py. 
Обычно его создают для чистоты кода, с помощью разделения кода классами.

```python
from tkinter import *
from config import CONFIG
import math
from decimal import Decimal, getcontext
from tkinter import Frame
```
Разберем каждый импорт по порядку:

- from tkinter import * - импорт всех функций из библиотеки tkinter;

- from config import CONFIG - импорт конфигурации из файла config.py;

- import math - импорт математических функций;

- from decimal import Decimal, getcontext - импорт Decimal для высокой точности вычислений и getcontext для установки точности;

- from tkinter import Frame - импорт класса Frame из библиотеки tkinter.

Создаем класс Calculator:

```python
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
```
В пером методе мы заменяем операторы на безопасные эквиваленты, чтобы избежать ошибок при вычислении. Устанаваливаем точность вычислений в 10 знаков после запятой.

Второй метод calculate вычисляет результат математического выражения. А точнее использует встроенную функцию eval для вычисления выражения и проверку на применение допустимых символов перед вычислением.

Третий метод format_result форматирует результат для красивого отображения. Если боллее точно, то он проверяет тип результата и его значение, и если оно больше 1e10 или меньше 1e-10 и не равно 0, то форматирует его в экспоненциальной форме. Иначе форматирует в 10 знаков после запятой.

Класс HistoryManager:

```pythonclass HistoryManager:
    """Класс для управления историей вычислений"""
    def __init__(self):
        self.history = []
        
    def add_calculation(self, expression, result):
        """Добавляет новое вычисление в историю"""
        self.history.append((expression, result))
        
    def clear(self):
        """Очищает историю вычислений"""
        self.history = []
```
В первом методе мы создаем пустой список для хранения истории вычислений. Каждый элемент будет кортежем из выражения и результата.

Во втором методе мы добавляем новое вычисление в историю. Метод принимает два аргумента: выражение и результат вычисления.

В третьем методе мы очищаем всю историю вычислений и создаем новый пустой список.

Класс CalculatorError:

```python
class CalculatorError(Exception):
    """Пользовательское исключение для ошибок калькулятора"""
    pass
```
В данном классе мы создаем пользовательское исключение для ошибок калькулятора.

Класс CalculatorUI:

```python
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
```
В этом методе мы создаем визуальный интерфейс калькулятора, инициализируем необходимые компоненты, подготовливаем обработку событи клавиатуры и связываем логику с интерфейсом.

```python
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
```
Здесь мы определяем кнопки и их расположение на интерфейсе.

```python
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
```
В этом методе мы привязываем клавиши к функциям калькулятора. По сути, это позволяет пользователю работать с калькулятором не только мышкой, но и с клавиатуры.

```python
 def handle_backspace(self, event):
        """Обработка нажатия клавиши Backspace"""
        if len(self.formula) > 0:
            self.formula = self.formula[:-1]
            if not self.formula:
                self.formula = "0"
            self.update()
```
Этот метод обрабатывает нажатие клавиши Backspace. Если в поле для вывода выражения есть символы, то удаляем последний символ. Если выражение пустое, то устанавливаем значение "0".

```python
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
```
Метод logicalc обрабатывает нажатие кнопок. Если нажата кнопка "C", то очищаем поле для вывода выражения и истории. Если нажата кнопка "CE", то очищаем поле для вывода выражения. Если нажата кнопка "√", то вычисляем квадратный корень из выражения. Если нажата кнопка "x^y", то добавляем "^" к выражению. Если нажата кнопка "lg", то вычисляем десятичный логарифм из выражения. Если нажата кнопка "ln", то вычисляем натуральный логарифм из выражения. Если нажата кнопка "=", то вычисляем результат выражения. Если нажата любая другая кнопка, то добавляем ее к выражению.

```python
    def update(self):
        if self.formula == "":
            self.formula = "0"
        display_text = self.formula
        if len(display_text) > 20:
            display_text = "..." + display_text[-17:]
        self.lbl.configure(text=display_text)
```
Метод update обновляет поле для вывода выражения. Если выражение пустое, то устанавливаем значение "0". Если длина выражения больше 20 символов, то обрезаем его и добавляем "...".


3. **Файл main**

Создаем файл main.py для запуска программы.

Основные функции:
- Создание главного окна приложения (root)
- Инициализация интерфейса калькулятора
- Запуск главного цикла событий

```python
from tkinter import Tk
from model import CalculatorUI
from config import CONFIG

def main():
    """Основная функция запуска калькулятора"""
    root = Tk()
    root.title("Калькулятор")
    root.resizable(False, False)
    
    # Устанавливаем размер и позицию окна из конфига
    root.geometry(CONFIG['LAYOUT']['WINDOW_SIZE'])
    root.configure(bg=CONFIG['COLORS']['BG'])  # Добавляем цвет фона
    
    # Создаем основной интерфейс калькулятора
    calculator_ui = CalculatorUI(root)
    calculator_ui.pack(expand=True, fill='both')  # Изменяем параметры pack
    
    # Запускаем главный цикл приложения
    root.mainloop()

if __name__ == "__main__":
    main()
```

Импортируем необходимые библиотеки и запускаем главный цикл приложения.








