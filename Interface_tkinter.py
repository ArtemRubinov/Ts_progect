from tkinter import messagebox
import datetime as dt

from For_basedata import get_data, set_schedule, set_auto_heating, get_data_auto_heating, \
    get_data_schedule, set_interface
from Interface_Functions import *
from Scrapping_weather import scrapping_weather

States_class = State_functions()


# Класс главного Интерфейса
class Main_Interface():
    def __init__(self, general_root):
        set_interface(1)
        self.root = general_root

        # Сначала нужно понять состояния устройств (вкл/выкл), чтобы корректно настроить интерфейс и их работу
        # Для этого воспользуемся условиями if, чтобы корректно настроить интерфейс

        # Здесь будет указываться какой МЕТОД для кнопки будет срабатывать в зависимости от включенности устройства
        methods_slovar = {}
        # Здесь будет указываться какой ТЕКСТ в кнопке будет отображаться в зависимости от включенности устройства
        for_but_text_slovar = {}

        states = monitoring()  # Здесь состояния устройств на момент запуска программы
        # Начнем с освещения
        if states[0] == '✔️':
            # Здесь указано какой цвет фона будет использоваться в меню при запуске программы
            self.main_bg_color = '#404040'

            methods_slovar['light'] = self.light_off
            for_but_text_slovar['light_but'] = 'ВКЛ'
        else:
            self.main_bg_color = 'black'
            methods_slovar['light'] = self.light_on
            for_but_text_slovar['light_but'] = 'ВЫКЛ'

        # Затем проверим отопление
        if states[1] == '✔️':
            methods_slovar['heating'] = self.heating_off
            for_but_text_slovar['heating_but'] = 'ВКЛ'
        else:
            methods_slovar['heating'] = self.heating_on
            for_but_text_slovar['heating_but'] = 'ВЫКЛ'

        # Состояния авто отопления и расписания можно не проверять так как у них по одному методу, путаницы не будет
        methods_slovar['auto_heating'] = self.auto_heating_settings
        methods_slovar['schedule'] = self.schedule_settings

        # Теперь в main_bg_color хранится информация о цвете фона, которую код будет использовать в начале,
        # в словаре methods_slovar лежат методы, которые будут срабатывать при нажатии на кнопку,
        # а в словаре for_but_text_slovar лежат тексты для кнопок освещения и отопления.

        self.root['bg'] = self.main_bg_color

        # Создаю главные объекты интерфейса
        # Создаю надпись ОСВЕЩЕНИЕ
        self.light_text = Label(self.root, text='ОСВЕЩЕНИЕ', fg='white', font=('TkCaptionFont', 20),
                                bg=self.main_bg_color)
        self.light_text.place(x=25, y=25)

        # Создаю кнопку ВКЛ/ВЫКЛ для надписи ОСВЕЩЕНИЕ
        self.light_but = Button(self.root, text=for_but_text_slovar['light_but'], font='Arial', bg='white')
        self.light_but.place(x=250, y=25)
        self.light_but.bind('<Button-1>', methods_slovar['light'])

        # Создаю надпись ОТОПЛЕНИЕ
        self.heating_text = Label(self.root, text='ОТОПЛЕНИЕ', fg='white', font=('TkCaptionFont', 20),
                                  bg=self.main_bg_color)
        self.heating_text.place(x=25, y=100)

        # Создаю кнопку ВКЛ/ВЫКЛ для надписи ОТОПЛЕНИЕ
        self.heating_but = Button(self.root, text=for_but_text_slovar['heating_but'], font='Arial', bg='white')
        self.heating_but.place(x=250, y=100)
        self.heating_but.bind('<Button-1>', methods_slovar['heating'])

        # Создаю надпись автоматической настройки отопления (АВТО ОТОПЛЕНИЕ)
        self.auto_heating_text = Label(self.root, text='АВТО ОТОПЛЕНИЕ', fg='white', font=('TkCaptionFont', 20),
                                       bg=self.main_bg_color)
        self.auto_heating_text.place(x=25, y=250)

        # Создаю кнопку для надписи автоматического отопления
        self.auto_heating_but = Button(self.root, text='настроить', font='Arial', bg='white')
        self.auto_heating_but.place(x=300, y=250)
        self.auto_heating_but.bind('<Button-1>', methods_slovar['auto_heating'])

        # Создаю надпись РАСПИСАНИЕ
        self.set_schedule_text = Label(self.root, text='РАСПИСАНИЕ', fg='white', font=('TkCaptionFont', 20),
                                       bg=self.main_bg_color)
        self.set_schedule_text.place(x=25, y=325)

        # Создаю кнопку для надписи НАСТРОИТЬ РАСПИСАНИЕ
        self.set_schedule_but = Button(self.root, text='настроить', font='Arial', bg='white')
        self.set_schedule_but.place(x=300, y=325)
        self.set_schedule_but.bind('<Button-1>', self.schedule_settings)

        # Создаю кнопку обновить
        self.update_but = Button(self.root, text='Обновить', font='Arial', bg='white', height=2, width=10)
        self.update_but.place(x=35, y=160)
        self.update_but.bind('<Button-1>', self.update)

        # Создаю кнопку Выход
        self.exit_but = Button(self.root, text='Выход', font='Arial', bg='white')
        self.exit_but.place(x=710, y=350)
        self.exit_but.bind('<Button-1>', self.exit)

        # Создание надписей состояний
        self.monitoring_light = Label(self.root, text='Освещение:', fg='white', font=('TkCaptionFont', 17),
                                      bg=self.main_bg_color)
        self.monitoring_light.place(x=525, y=25)

        self.monitoring_heating = Label(self.root, text='Отопление:', fg='white', font=('TkCaptionFont', 17),
                                        bg=self.main_bg_color)
        self.monitoring_heating.place(x=525, y=75)

        self.monitoring_auto_heating = Label(self.root, text='АВТО Отопление:', fg='white', font=('TkCaptionFont', 17),
                                             bg=self.main_bg_color)
        self.monitoring_auto_heating.place(x=525, y=125)

        self.monitoring_schedule = Label(self.root, text='Расписание:', fg='white', font=('TkCaptionFont', 17),
                                         bg=self.main_bg_color)
        self.monitoring_schedule.place(x=525, y=175)

        # Создание эмоджи состояний
        self.vidget_spis = set_status_monitoring(self.root, self.main_bg_color)

        # Соберу все нужные Надписи и Кнопки интрфейса в два спика для удобной работы с ними
        self.labels_spis = [self.root, self.light_text, self.heating_text, self.auto_heating_text,
                            self.set_schedule_text, self.monitoring_light, self.monitoring_heating,
                            self.monitoring_auto_heating, self.monitoring_schedule]
        self.buttons_spis = [self.light_but, self.heating_but, self.auto_heating_but, self.set_schedule_but,
                             self.exit_but]

        # Создание отображения данных о настройках авто отопления и расписания
        if states[2] == '✔️':
            self.trait = Label(self.root, text='___' * 12, fg='white', font=('TkCaptionFont', 13),
                               bg=self.main_bg_color)
            self.trait.place(x=455, y=200)

            # Получаю данные из бд
            data_spis_auto_heating = get_data_auto_heating()

            # Создание надпись отображения данных авто отопления
            self.auto_heating_text_monitoring = Label(self.root, text='АВТО ОТОПЛЕНИЕ', fg='white',
                                                      font=('TkCaptionFont', 13),
                                                      bg=self.main_bg_color)
            self.auto_heating_text_monitoring.place(x=625, y=240)

            # Создание надпись город:
            self.city_text = Label(self.root, text=f'Город: {data_spis_auto_heating[0]}', fg='white',
                                   font=('TkCaptionFont', 11),
                                   bg=self.main_bg_color)
            self.city_text.place(x=630, y=270)

            # Создание надпись При температуре:
            self.temperature_text = Label(self.root, text=f'При температуре: {data_spis_auto_heating[1]}°', fg='white',
                                          font=('TkCaptionFont', 11),
                                          bg=self.main_bg_color)
            self.temperature_text.place(x=630, y=295)
            self.labels_spis += [self.trait, self.auto_heating_text_monitoring,
                                 self.city_text, self.temperature_text]

        if states[3] == '✔️':
            self.trait1 = Label(self.root, text='___' * 12, fg='white', font=('TkCaptionFont', 13),
                                bg=self.main_bg_color)
            self.trait1.place(x=455, y=200)

            # Получаю данные из бд
            data_spis_schedule = get_data_schedule()

            # Создание надпись отображения данных авто отопления
            self.schedule_text = Label(self.root, text='РАСПИСАНИЕ', fg='white', font=('TkCaptionFont', 13),
                                       bg=self.main_bg_color)
            self.schedule_text.place(x=460, y=240)

            # Создание надпись освещение
            self.light_text_schedule = Label(self.root, text='освещение:', fg='white', font=('TkCaptionFont', 12),
                                             bg=self.main_bg_color)
            self.light_text_schedule.place(x=460, y=270)

            # Создание надпись отопление
            self.heating_text_schedule = Label(self.root, text='отопление:', fg='white', font=('TkCaptionFont', 12),
                                               bg=self.main_bg_color)
            self.heating_text_schedule.place(x=460, y=330)

            # Создаю надписи С и До
            # для освещения
            self.from_text_schedule = Label(self.root, text=f'с: {data_spis_schedule[0]}', fg='white',
                                            font=('TkCaptionFont', 11),
                                            bg=self.main_bg_color)
            self.from_text_schedule.place(x=460, y=300)

            self.befor_text_schedule = Label(self.root, text=f'до: {data_spis_schedule[1]}', fg='white',
                                             font=('TkCaptionFont', 11),
                                             bg=self.main_bg_color)
            self.befor_text_schedule.place(x=520, y=300)
            # для отопления
            self.from_text_schedule1 = Label(self.root, text=f'c: {data_spis_schedule[2]}', fg='white',
                                             font=('TkCaptionFont', 11),
                                             bg=self.main_bg_color)
            self.from_text_schedule1.place(x=460, y=360)

            self.befor_text_schedule1 = Label(self.root, text=f'до: {data_spis_schedule[3]}', fg='white',
                                              font=('TkCaptionFont', 11),
                                              bg=self.main_bg_color)
            self.befor_text_schedule1.place(x=520, y=360)

            self.labels_spis += [self.trait1, self.schedule_text,
                                 self.light_text_schedule, self.heating_text_schedule, self.from_text_schedule,
                                 self.befor_text_schedule, self.from_text_schedule1, self.befor_text_schedule1]

        self.root.mainloop()

    # Метод включения света
    def light_on(self, event):
        self.light_but['text'] = 'ВКЛ'
        self.light_but.bind('<Button-1>', self.light_off)

        # Нужно изменить цвет интерфейса
        self.main_bg_color = '#404040'

        # добавляю статус включения освещения в базу данных = 1
        States_class.set_state_light(flag=True)

        # Меняю цвета главного интерфейса на более яркий
        for item in self.labels_spis:
            item['bg'] = self.main_bg_color

        # Создаю новый статусы мониторгинга устройств
        destroy_status_vidgets(self.vidget_spis)
        self.vidget_spis = set_status_monitoring(self.root, self.main_bg_color)

    # Метод выключения света
    def light_off(self, event):
        self.light_but['text'] = 'ВЫКЛ'
        self.light_but.bind('<Button-1>', self.light_on)

        # Нужно изменить цвет интерфейса
        self.main_bg_color = 'black'

        # добавляю статус включения освещения = 0
        States_class.set_state_light(flag=False)

        # Меняю цвета главного интерфейса на более тусклый
        for item in self.labels_spis:
            item['bg'] = self.main_bg_color

        # Создаю новые статусы мониторгинга устройств
        destroy_status_vidgets(self.vidget_spis)
        self.vidget_spis = set_status_monitoring(self.root, self.main_bg_color)

    # Метод включения отопления
    def heating_on(self, event):
        self.heating_but['text'] = 'ВКЛ'
        self.heating_but.bind('<Button-1>', self.heating_off)

        # добавляю статус включения отопления = 1
        States_class.set_state_heating(flag=True)

        # Создаю новые статусы мониторгинга устройств
        destroy_status_vidgets(self.vidget_spis)
        self.vidget_spis = set_status_monitoring(self.root, self.main_bg_color)

    # Метод выключения отопления
    def heating_off(self, event):
        self.heating_but['text'] = 'ВЫКЛ'
        self.heating_but.bind('<Button-1>', self.heating_on)

        # добавляю статус включения отопления = 1
        States_class.set_state_heating(flag=False)

        # Создаю новые статусы мониторгинга устройств
        destroy_status_vidgets(self.vidget_spis)
        self.vidget_spis = set_status_monitoring(self.root, self.main_bg_color)

    # Метод включения авто отопления
    def auto_heating_settings(self, event):
        delete_vidgets(self.root)
        Settings_Auto_Heating(self.root, self.main_bg_color)

    # Метод настроек расписания
    def schedule_settings(self, event):
        delete_vidgets(self.root)
        Settings_Schedule(self.root, self.main_bg_color)

    def update(self, event):
        start_pend(self.root)

    # Метод выхода из приложения
    def exit(self, event):
        self.root.destroy()
        self.root.quit()
        exit()


class Settings_Schedule():
    def __init__(self, general_root, bg_color):
        self.root_set_schedule = general_root

        # Создание кнопки Назад у окна настроек расписания
        self.back = Button(self.root_set_schedule, width=5, height=1, text='Назад', font='Arial', bg='white')
        self.back.place(x=600, y=350)
        self.back.bind('<Button-1>', self.back_menu)

        # Создание кнопки Сохранить у окна настроек расписания
        self.save = Button(self.root_set_schedule, width=9, height=1, text='Сохранить', font='Arial', bg='white')
        self.save.place(x=675, y=350)
        self.save.bind('<Button-1>', self.save_settings_schedule)

        # Создание кнопки Отключить у окна настроек расписания
        if get_data()[3]:
            self.disable = Button(self.root_set_schedule, width=9, height=1, text='Отключить', font='Arial', bg='white')
            self.disable.place(x=15, y=350)
            self.disable.bind('<Button-1>', self.shutdown_settings_schedule)

        # Надписи
        # Создаю надпись ОСВЕЩЕНИЕ
        self.light_schedule_text = Label(self.root_set_schedule, text='ОСВЕЩЕНИЕ', fg='white',
                                         font=('TkCaptionFont', 30),
                                         bg=bg_color)
        self.light_schedule_text.place(x=60, y=20)

        # Создаю надпись ОТОПЛЕНИЕ
        self.heating_schedule_text = Label(self.root_set_schedule, text='ОТОПЛЕНИЕ', fg='white',
                                           font=('TkCaptionFont', 30),
                                           bg=bg_color)
        self.heating_schedule_text.place(x=450, y=20)

        # Создаю по две надписи Со скольких и До скольких
        # Со скольких
        self.from_time = Label(self.root_set_schedule, text='С', fg='white',
                               font=('TkCaptionFont', 23),
                               bg=bg_color)
        self.from_time.place(x=30, y=110)
        self.from_time1 = Label(self.root_set_schedule, text='С', fg='white',
                                font=('TkCaptionFont', 23),
                                bg=bg_color)
        self.from_time1.place(x=420, y=110)

        # До скольких
        self.befor_time = Label(self.root_set_schedule, text='До', fg='white',
                                font=('TkCaptionFont', 23),
                                bg=bg_color)
        self.befor_time.place(x=30, y=220)
        self.befor_time1 = Label(self.root_set_schedule, text='До', fg='white',
                                 font=('TkCaptionFont', 23),
                                 bg=bg_color)
        self.befor_time1.place(x=420, y=220)

        # Создаю поля для ввода Со скольких и До скольких
        # Со скольких
        self.enter_from_time = Entry(self.root_set_schedule, fg='black', font=('Arial', 20), width=16)
        self.enter_from_time.place(x=80, y=115)
        self.enter_from_time1 = Entry(self.root_set_schedule, fg='black', font=('Arial', 20), width=16)
        self.enter_from_time1.place(x=470, y=115)

        # До скольких
        self.enter_befor_time = Entry(self.root_set_schedule, fg='black', font=('Arial', 20), width=16)
        self.enter_befor_time.place(x=80, y=225)
        self.enter_befor_time1 = Entry(self.root_set_schedule, fg='black', font=('Arial', 20), width=16)
        self.enter_befor_time1.place(x=470, y=225)

    # Метод перехода обратно в меню
    def back_menu(self, event):
        delete_vidgets(self.root_set_schedule)  # Удаляем все виджеты
        Main_Interface(self.root_set_schedule)  # Создаем новый начальный интерфейс

    # Метод проверки и сохранения настроек
    def save_settings_schedule(self, event):
        flag = True
        # Сначала проверям введенное время на корректность
        data_text = [self.enter_from_time.get(), self.enter_befor_time.get(), self.enter_from_time1.get(),
                     self.enter_befor_time1.get()]  # Собираем все, введённые пользователем, тексты в список.
        # Проверка на правильность ввода
        try:

            for item_text in data_text:
                item = item_text.split(':')
                if int(item[0]) in [i for i in range(0, 24)] and int(item[1]) in [i for i in
                                                                                  range(0, 60)] and len(item[1]) == 2:
                    pass
                else:
                    flag = False
                    messagebox.showerror('Ошибка', 'Некорректный ввод данных.')

            if flag and data_text[0] == data_text[1] or data_text[2] == data_text[3]:

                flag = False
                messagebox.showerror('Ошибка', 'Устройства в расписании не могу работать целый день.')
        except Exception:
            flag = False
            messagebox.showerror('Ошибка', 'Некорректный ввод данных.')
        finally:
            if flag:
                set_schedule(True, data_text)  # добавление в бд расписания
                States_class.set_state_schedule(True)  # добавления состояния "включено" в мониторинг состояний

                start_pend(self.root_set_schedule)  # Создаем новый начальный интерфейс

    # Метод отключения настроек расписания
    def shutdown_settings_schedule(self, event):
        set_schedule(False, [])
        States_class.set_state_schedule(False)

        delete_vidgets(self.root_set_schedule)  # Удаляем все виджеты
        Main_Interface(self.root_set_schedule)  # Создаем новый начальный интерфейс


class Settings_Auto_Heating():
    def __init__(self, general_root, bg_color):
        set_interface(2)
        self.root_auto_heating = general_root

        # Создание кнопки Назад у окна настроек авто отопления
        self.back_auto_heating = Button(self.root_auto_heating, width=5, height=1, text='Назад', font='Arial',
                                        bg='white')
        self.back_auto_heating.place(x=600, y=350)
        self.back_auto_heating.bind('<Button-1>', self.close_window_auto_heating)

        # Создание кнопки Сохранить у окна настроек авто отопления
        self.save_auto_heating = Button(self.root_auto_heating, width=9, height=1, text='Сохранить', font='Arial',
                                        bg='white')
        self.save_auto_heating.place(x=675, y=350)
        self.save_auto_heating.bind('<Button-1>', self.save_auto_heating_method)

        if get_data()[2]:
            # Создание кнопки Отключить у окна настроек авто отопления
            self.disable_auto_heating = Button(self.root_auto_heating, width=9, height=1, text='Отключить',
                                               font='Arial',
                                               bg='white')
            self.disable_auto_heating.place(x=15, y=350)
            self.disable_auto_heating.bind('<Button-1>', self.shutdown_auto_heating)

        # Надписи
        # Создание надписи Город
        self.city = Label(self.root_auto_heating, text='Город', fg='white',
                          font=('TkCaptionFont', 30),
                          bg=bg_color)
        self.city.place(x=50, y=75)

        # Создание надписи Температура
        self.temperature = Label(self.root_auto_heating, text='Температура', fg='white',
                                 font=('TkCaptionFont', 30),
                                 bg=bg_color)
        self.temperature.place(x=50, y=200)

        # Создаю поля для ввода Город и Температуры
        # Со скольки
        self.enter_city = Entry(self.root_auto_heating, fg='black', font=('Arial', 20), width=16)
        self.enter_city.place(x=200, y=82)

        self.enter_temperature = Entry(self.root_auto_heating, fg='black', font=('Arial', 20), width=16)
        self.enter_temperature.place(x=330, y=207)

    # Метод закрытия окна настроек авто отопления
    def close_window_auto_heating(self, event):
        delete_vidgets(self.root_auto_heating)
        Main_Interface(self.root_auto_heating)

    # Метод сохранить для настроек авто отопления
    def save_auto_heating_method(self, event):
        data_city_needtemp = self.enter_city.get(), self.enter_temperature.get()  # Список с введенными городом и темп.

        result_scrapping = scrapping_weather(data_city_needtemp[0])  # Здесь результат работы сбора температуры
        if not result_scrapping:
            messagebox.showerror('Ошибка',
                                 '''Невозможно получить информацию о температуре в городе.
Если вы уверены, что ввели всё правильно, то попробуйте указать близкий к вам более крупный город''')
        else:
            try:
                set_auto_heating(data_city_needtemp[0], round(float(data_city_needtemp[1]), 1))
                States_class.set_state_auto_heating(True)  # добавления состояния "включено" в мониторинг состояний

                start_pend(self.root_auto_heating)  # Создаем новый начальный интерфейс
            except Exception as ex:
                messagebox.showerror('Ошибка', 'Не правильно введена температура.')

    # Метод отключения авто отопления
    def shutdown_auto_heating(self, event):
        States_class.set_state_auto_heating(False)

        delete_vidgets(self.root_auto_heating)  # Удаляем все виджеты
        Main_Interface(self.root_auto_heating)


# Функция обновления системы
def start_pend(main_root):
    data = get_data()
    # Проверка включено ли расписание
    if data[3]:
        now_time = int(''.join(str(dt.datetime.now().time()).split(':')[:2]))

        from_time_light, to_time_light, from_time_heating, to_time_heating = list(
            map(lambda x: int(''.join(str(x).split(':'))), get_data_schedule()))

        # Нужно настроить программу для случая если пользователь ввел - с 15:30 до 15:00.
        # Для этого просто сделаем главные проверки 2 проверки

        # Освещение
        if to_time_light < from_time_light:
            if now_time < to_time_light or now_time > from_time_light:
                States_class.set_state_light(True)
            else:
                States_class.set_state_light(False)
        else:
            if now_time >= from_time_light:
                if now_time < to_time_light:
                    States_class.set_state_light(True)

                else:
                    States_class.set_state_light(False)
            else:
                States_class.set_state_light(False)
        # Отопление
        if to_time_heating < from_time_heating:
            if now_time < to_time_light or now_time > from_time_light:
                States_class.set_state_heating(True)
            else:
                States_class.set_state_heating(False)
        else:
            if now_time >= from_time_heating:
                if now_time < to_time_heating:
                    States_class.set_state_heating(True)

                else:
                    States_class.set_state_heating(False)
            else:
                States_class.set_state_heating(False)

    # Проверка включено ли отопление
    if data[2]:
        city, need_temp = get_data_auto_heating()
        real_temp = float(scrapping_weather(city))

        if float(need_temp) > real_temp:
            States_class.set_state_heating(True)
        else:
            States_class.set_state_heating(False)

    delete_vidgets(main_root)  # Очистка оинтерфейса
    Main_Interface(main_root)  # Создание нового интерфейса
