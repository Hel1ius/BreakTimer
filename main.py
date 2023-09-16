from datetime import datetime
import threading

from playsound import playsound

from functions import is_valid_number
menu = {
    1: 'Время сейчас',
    2: 'Запланировать перерыв',
    3: 'Список запланированных перерывов',
    4: 'Удалить запланированный перерыв',
    5: 'Редактировать перерыв',
    6: 'Время до ближайшего перерыва'
}

break_list = {}


def apscheduler_break():
    while True:
        current_time = datetime.now().strftime("%H:%M")
        if current_time in break_list.values():
            print('Время перерыва!')
            playsound('F:\PycharmProjects\BreakTimer\sound\htc_basic.mp3')
            key_to_remove = [key for key, value in break_list.items() if value == current_time]
            print(key_to_remove)
            if key_to_remove:
                del break_list[key_to_remove[0]]

def main_menu():
    while True:
        current_time = datetime.now().strftime("%H:%M")
        for key, value in menu.items():
            print(f'{key}. {value}')
        menu_number = int(input('Введите номер функции: '))
        if is_valid_number(menu_number):
            if menu_number not in menu.keys():
                print(f'Функции с таким номером не существует: {menu_number}')
            else:
                if menu_number == 1:
                    print(f'Время сейчас: {current_time}')
                elif menu_number == 2:
                    break_name = str(input('Введите название перерыва: '))
                    break_time = input('Введите на какое время назначить перерыв в формате "HH:MM": ')
                    break_list.update({break_name: break_time})
                elif menu_number == 3:
                    if break_list:
                        for key, value in break_list.items():
                            to_break = (int(value[0:2]) * 60 + int(value[3:5])) - int(current_time[0:2]) * 60 + int(
                                current_time[3:5])
                            print(f'{key} назначен на {value}, через {to_break // 60}ч:{to_break % 60}м')
                    else:
                        print('Список перерывов пуст')
                elif menu_number == 4:
                    while break_list:
                        for index, (key, value) in enumerate(break_list.items()):
                            print(f'{index + 1}. {key} в {value}')
                        delete_number = input("Введите номер перерыва для удаления (или 'q' для выхода): ")
                        if delete_number == 'q':
                            break
                        else:
                            try:
                                index_to_remove = int(delete_number) - 1
                                if 0 <= index_to_remove <= len(break_list):
                                    key_to_remove = list(break_list.keys())[index_to_remove]
                                    del break_list[key_to_remove]
                                else:
                                    print('Такого номера перерыва нету')
                            except ValueError:
                                print('Некорректный ввод. Попробуйте снова')
                                continue
                    else:
                        print('Список перерывов пуст')
                elif menu_number == 5:
                    print('функция еще недоступна')
                else:
                    to_break_l = []
                    for key, value in break_list.items():
                        to_break = (int(value[0:2]) * 60 + int(value[3:5])) - (int(current_time[0:2]) * 60 + int(
                            current_time[3:5]))
                        to_break_l.append(to_break)
                    min_value = sorted(to_break_l)[0]
                    print(f'Время до ближайшего перерыва {min_value // 60}ч:{min_value % 60}м({key})')
        else:
            print(f'Вы ввели некорректное число: {menu_number}')

thread1 = threading.Thread(target=main_menu)
thread2 = threading.Thread(target=apscheduler_break)

thread1.start()
thread2.start()

# Ждем завершения потоков (этот код будет ждать завершения обоих потоков)
thread1.join()
thread2.join()