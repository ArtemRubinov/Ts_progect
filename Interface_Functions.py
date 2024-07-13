from tkinter import *

from For_basedata import monitoring, State_functions

States_class = State_functions()


# Функция удаляющая все виджеты окна
def delete_vidgets(base_root):
    for widget in base_root.winfo_children():
        widget.destroy()


# Функция создающая эмоджи состояний устройсв для интерфейса
def set_status_monitoring(main_root, bg_color):
    light, heating, auto_heating, schedule = monitoring()

    monitoring_light_status = Label(main_root, text=light, fg='red', font=('TkCaptionFont', 17),
                                    bg=bg_color)
    monitoring_light_status.place(x=750, y=25)

    monitoring_heating_status = Label(main_root, text=heating, fg='red', font=('TkCaptionFont', 17),
                                      bg=bg_color)
    monitoring_heating_status.place(x=750, y=75)

    monitoring_auto_heating_status = Label(main_root, text=auto_heating, fg='red',
                                           font=('TkCaptionFont', 17),
                                           bg=bg_color)
    monitoring_auto_heating_status.place(x=750, y=125)

    monitoring_schedule_status = Label(main_root, text=schedule, fg='red', font=('TkCaptionFont', 17),
                                       bg=bg_color)
    monitoring_schedule_status.place(x=750, y=175)

    # Если галочка, то цвет зеленый.
    if light == '✔️':
        monitoring_light_status['fg'] = 'green'
    if heating == '✔️':
        monitoring_heating_status['fg'] = 'green'
    if auto_heating == '✔️':
        monitoring_auto_heating_status['fg'] = 'green'
    if schedule == '✔️':
        monitoring_schedule_status['fg'] = 'green'

    return [monitoring_light_status, monitoring_heating_status, monitoring_auto_heating_status,
            monitoring_schedule_status]


# Функция удаления виджетов - состояний устройств
def destroy_status_vidgets(vidgets):
    for item in vidgets:
        item.destroy()
