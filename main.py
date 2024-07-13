from Interface_tkinter import *
from For_basedata import create_tables


def main():
    # Создаем все нужные таблицы
    create_tables()
    # Записываем в бд, что мы находимся в 1 интерфейсе
    set_interface(1)

    # Создаем главное окно
    main_root = Tk()

    # Добавляем характеристики главного окна
    main_root.title('Smart home control system')
    main_root.geometry('800x400')
    main_root.resizable(width=False, height=False)

    # Создаем интерфейс главного меню
    Main_Interface(main_root)


if __name__ == '__main__':
    main()
