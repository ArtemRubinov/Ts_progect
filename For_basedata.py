import sqlite3


# Функция создания всех нужных таблиц если их нет
def create_tables():
    # Коннект с базой данных
    db = sqlite3.connect('database.db')
    cursor = db.cursor()
    # Проверка есть ли таблица
    if 'interface' not in [table_name[1] for table_name in
                           cursor.execute("SELECT * FROM sqlite_master WHERE type='table'").fetchall()]:
        cursor.execute(
            """CREATE TABLE IF NOT EXISTS interface(count INTEGER)""")
        cursor.execute('INSERT INTO interface VALUES (1)')
        db.commit()
    # Проверка есть ли таблица
    if 'states_of_system' not in [table_name[1] for table_name in
                                  cursor.execute("SELECT * FROM sqlite_master WHERE type='table'").fetchall()]:
        cursor.execute(
            """CREATE TABLE IF NOT EXISTS states_of_system(light INTEGER,
            heating INTEGER,
            auto_heating INTEGER,
            schedule INTEGER)""")
        cursor.execute('INSERT INTO states_of_system VALUES (0, 0, 0, 0)')
        db.commit()

    # Проверка есть ли таблица
    if 'schedule_table' not in [table_name[1] for table_name in
                                cursor.execute("SELECT * FROM sqlite_master WHERE type='table'").fetchall()]:
        cursor.execute(
            """CREATE TABLE IF NOT EXISTS schedule_table(from_light TEXT,
            befor_light TEXT,
            from_heating TEXT,
            befor_heating TEXT)""")
        cursor.execute("INSERT INTO schedule_table VALUES ('0', '0', '0', '0')")
        db.commit()

    # Проверка есть ли таблица
    if 'auto_heating_table' not in [table_name[1] for table_name in
                                    cursor.execute("SELECT * FROM sqlite_master WHERE type='table'").fetchall()]:
        cursor.execute(
            """CREATE TABLE IF NOT EXISTS auto_heating_table(city TEXT,
            temperature TEXT)""")
        cursor.execute("INSERT INTO auto_heating_table VALUES ('None', 'None')")
        db.commit()


def set_interface(count_):
    # Коннект с базой данных
    db = sqlite3.connect('database.db')
    cursor = db.cursor()
    cursor.execute(f"UPDATE interface SET count = {count_}")
    db.commit()


# Класс функций состояний устройств системы (включить/выключить)
class State_functions():
    def __init__(self):
        # Коннект с базой данных
        self.db = sqlite3.connect('database.db')
        self.cursor = self.db.cursor()

    # Метод записывания состояния освещения
    def set_state_light(self, flag: bool):

        try:
            # Если Метод передан со значением True, то будет записываться что свет горит - 1
            # в противном случае - 0.
            if flag:
                self.cursor.execute("UPDATE states_of_system SET light = 1")
            else:
                self.cursor.execute("UPDATE states_of_system SET light = 0")
            self.db.commit()
        except Exception as ex:
            print(ex)

    # Метод записывания состояния отопления
    def set_state_heating(self, flag: bool):

        try:
            # Если Метод передан со значением True, то будет записываться что отопление работает - 1
            # в противном случае - 0.
            if flag:
                self.cursor.execute("UPDATE states_of_system SET heating = 1")
            else:
                self.cursor.execute("UPDATE states_of_system SET heating = 0")
            self.db.commit()
        except Exception as ex:
            print(ex)

    # Метод записывания состояния авто отопления
    def set_state_auto_heating(self, flag: bool):

        try:
            # Если Метод передан со значением True, то будет записываться что авто отопление работает - 1
            # в противном случае - 0.
            if flag:
                self.cursor.execute("UPDATE states_of_system SET auto_heating = 1")
            else:
                self.cursor.execute("UPDATE states_of_system SET auto_heating = 0")
            self.db.commit()
        except Exception as ex:
            print(ex)

    # Метод записывания состояния расписания
    def set_state_schedule(self, flag: bool):

        try:
            # Если Метод передан со значением True, то будет записываться что расписание работает - 1
            # в противном случае - 0.
            if flag:
                self.cursor.execute("UPDATE states_of_system SET schedule = 1")
            else:
                self.cursor.execute("UPDATE states_of_system SET schedule = 0")
            self.db.commit()
        except Exception as ex:
            print(ex)

# Функция мониторинга состояний устройств
def monitoring():
    # Коннект с базой данных
    db = sqlite3.connect('database.db')
    cursor = db.cursor()

    # Функция будет возвращать список эмоджи, которые будут показывать состояния устройств

    spis = list()
    for item in cursor.execute('SELECT * FROM states_of_system').fetchall()[0]:
        if item:
            spis.append('✔️')
        else:
            spis.append('❌')
    return spis


# Техническая функция, которая возвращает данные состояний (для кода).
def get_data():
    # Коннект с базой данных
    db = sqlite3.connect('database.db')
    cursor = db.cursor()

    return cursor.execute('SELECT * FROM states_of_system').fetchall()[0]  # => example: (1, 0, 0, 0)


# Функция записи данных в таблицу расписания
def set_schedule(flag, data_spis):
    # Коннект с базой данных
    db = sqlite3.connect('database.db')
    cursor = db.cursor()

    # Добавление записей в зависимости от включенности расписания flag = True/False => вкл/выкл.
    if flag:
        cursor.execute(f"UPDATE schedule_table SET from_light = '{data_spis[0]}'")
        db.commit()
        cursor.execute(f"UPDATE schedule_table SET befor_light = '{data_spis[1]}'")
        db.commit()
        cursor.execute(f"UPDATE schedule_table SET from_heating = '{data_spis[2]}'")
        db.commit()
        cursor.execute(f"UPDATE schedule_table SET befor_heating = '{data_spis[3]}'")
        db.commit()
    else:
        cursor.execute(f"UPDATE schedule_table SET from_light = '0'")
        db.commit()
        cursor.execute(f"UPDATE schedule_table SET befor_light = '0'")
        db.commit()
        cursor.execute(f"UPDATE schedule_table SET from_heating = '0'")
        db.commit()
        cursor.execute(f"UPDATE schedule_table SET befor_heating = '0'")
        db.commit()


# Функция записи данных в таблицу авто отопления
def set_auto_heating(city, need_temp):
    # Коннект с базой данных
    db = sqlite3.connect('database.db')
    cursor = db.cursor()

    # Редактирование записей.
    cursor.execute(f"UPDATE auto_heating_table SET city = '{city}'")
    db.commit()
    cursor.execute(f"UPDATE auto_heating_table SET temperature = '{str(need_temp)}'")
    db.commit()


# Техническая функция, которая возвращает данные авто отопления.
def get_data_auto_heating():
    # Коннект с базой данных
    db = sqlite3.connect('database.db')
    cursor = db.cursor()

    return cursor.execute('SELECT * FROM auto_heating_table').fetchall()[0]  # ==> example: ('Воронеж', '35.0')


# Техническая функция, которая возвращает данные авто отопления.
def get_data_schedule():
    # Коннект с базой данных
    db = sqlite3.connect('database.db')
    cursor = db.cursor()

    return cursor.execute('SELECT * FROM schedule_table').fetchall()[
        0]  # => example ('13:30', '13:31', '13:30', '13:31')


# Техническая функция, которая возвращает данные о том, какой интерфейс был открыт.
def get_interface_data():
    # Коннект с базой данных
    db = sqlite3.connect('database.db')
    cursor = db.cursor()

    return cursor.execute('SELECT * FROM interface').fetchall()[0][0]
