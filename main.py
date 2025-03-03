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

