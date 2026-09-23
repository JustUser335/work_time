# import datetime as dt 
# основное внимание в реализации уделяется эффективному извлечению атрибутов для форматирования и обработки выходных данных.

# для начала выведем все доступные методы
# сигнатуры методов?

#Общие свойства 
#Типы date, datetime, time, и timezone обладают следующими общими характеристиками:
# - Объекты таких типов являются неизменяемыми.
# - Объекты этих типов являются хешируемыми , то есть их можно использовать в качестве ключей словаря.
# - Объекты этих типов обеспечивают эффективную сериализацию с помощью pickleмодуля.

# Определение того, является ли объект осведомленным или наивным
# class datetime.timedelta ( days = 0 , seconds = 0 , microseconds = 0 , milliseconds = 0 , minutes = 0 , hours = 0 , weeks = 0 )
# Все аргументы являются необязательными и по умолчанию равны 0
# 


# v0.01
# print(dt.date(2026,9,11)) # наверное есть форматирование вывода судя по выводу
# print(dt.time(h,m,s,ms))
# print(dt.datetime(2026,9,11,19,0,0))
# print(dt.timedelta(2026,9,11,19,0,0)) # считает от нуля
# print(dt.timedelta(hours=19,minutes=0)) # считает от нуля
# print(dt.tzinfo(dt.datetime(2026,9,11,19,0,0)))
# print(dt.timezone(dt.datetime(2026,9,11,19,0,0)))


# Давай попробуем вычитать время
# v0
# start = {
#     "hours": 10,
#     "minutes": 30
#     }
# end = {
#     "hours": 12,
#     "minutes": 40
#     }

# time_start = dt.timedelta(hours = start["hours"],minutes = start["minutes"])
# time_end = dt.timedelta(hours = end["hours"],minutes = end["minutes"])
# work_time = time_end - time_start
# print("work_time", work_time, sep=": ")


# v1
import datetime as dt
from collections import namedtuple
from typing import Callable
from functools import reduce
from rich import print
from PIL import Image
import pytesseract
import re
import os

Time_naming = namedtuple('Time_naming', ['hours', 'minutes'])

def pt(hours: int, minutes: int) -> tuple: # parameters_time
    """
    Инициализирует namedtuple.
    """
    return Time_naming(
        hours,
        minutes
    )

def delta_time(start: tuple, end: tuple) -> tuple:
    """
    Вычисляет разность между установленными часами.

    Принимает следующие аргументы:
    start: tuple, end: tuple 
    Где оба кортежа (часы: int, минуты: int )

    Возвращает:
    dt.timedelta
    """
    time_start = dt.timedelta( 
        hours = start.hours,
        minutes = start.minutes )
    time_end = dt.timedelta( 
        hours = end.hours, 
        minutes = end.minutes) 
    
    work_time = time_end - time_start
    return work_time

def set_accomulate_value() -> Callable[[dt.timedelta], dt.timedelta]:
    """
    Определяет функцию накопитель и возвращает её.

    Содержит накопительную переменную duration_list type list
    """
    duration_list = list()

    def accomulate_value(current_timedelta: dt.timedelta) -> dt.timedelta:
        """
        Суммирует время по средствам reduce.

        Принимает аргумент:
        current_timedelta type dt.timedelta

        Возвращает суммарное значение dt.timedelta
        """
        duration_list.append(current_timedelta)
        duration_work = reduce(
            lambda accomulate, current: accomulate + current, 
            duration_list, 
            dt.timedelta(hours=0,minutes=0)
            )
        return duration_work
    
    return accomulate_value


def calc_time(start_hours: int = 0, start_minutes: int = 0, end_hours: int = 0, end_minutes: int = 0) -> tuple:
    """
    Входящие параметры:

    Старт работы
    start_hours: int = 0,
    start_minutes: int = 0,

    Завершение работы
    end_hours: int = 0,
    end_minutes: int = 0

    
    Возвращает:
    tuple val type dt.timedelta
    
    """
    time_difference = delta_time(pt(start_hours,start_minutes),pt(end_hours,end_minutes))
    return time_difference

accomulate_value = set_accomulate_value()

def reading_img(path_folder: str) ->  dict: 
    if not os.path.isdir(path_folder):
        raise FileNotFoundError ('path_folder не указывает на папку')
    
    listfile = os.listdir(path_folder)
    if not listfile:
        raise FileNotFoundError('Пустая директория')
    
    pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
    text_entry_dict = {}
    for file in listfile:
        path = os.path.join(path_folder,file)
        image = Image.open(path)
        text = pytesseract.image_to_string(image, lang='eng')
        text_entry_dict[file] = text

    return text_entry_dict


def text_analysis(*, path_folder:str, reading_img: Callable[[str], dict]) -> dict:
    """
    Читает папку с изображениями, извлекает текст. 

    - path_folder путь к папке с изображениями
    - reading_img одноимённая функция для чтения изображений

    Возвращает dict форма {'имя картинки': dict{ 'user', 'labor date', 'clock in', 'clock out' }}

    Возможные баги.
    Разделитель между часами":"минутами, такой же разделитель между параметром и значением полей 'user', 'labor date'.
    Решение, последние два поля обрабатываются отдельно, в качестве разделителя используется "|".

    Особенности изображения:
        user: name
        labor date: dd/mm/yyyy
        clock in dd/mm/yyyy hh:mm
        clock out dd/mm/yyyy hh:mm
    """
    text_entry_dict = reading_img(path_folder)
    processed_data = {}
    for el in text_entry_dict.items():
        if not el[1]:
            raise ValueError(f'Вероятно пустая строка или 1. Файл {el[0]}, контент {el[1]}')
    
        text = el[1].strip().lower()
        res = re.finditer(r'(user:.*)(?=\n)|(labor\sdate:.*)(?=\n)|(clock\s[in|out].*)(?= user)', text)
        pattern = re.compile(r'\s\d+\/\d+\/\d+\s')
        dict_val = {}

        for txt_str in res:
            txt = txt_str.group()
            condition = re.search(pattern,txt)
            if not condition:
                key, val = txt.split(':')
                dict_val[key] = val.strip()
            else:
                key, val = re.sub(pattern,'|',txt).split('|')
                dict_val[key] = val
        processed_data[el[0]] = dict_val
    return processed_data

# user_data = text_analysis(path_folder = './img/', reading_img = reading_img)

def integrity_check( datas: Callable[[str], dict]):
    """
    Проверка и редактирование выходных данных из "text_analysis".
    Бывает такое что текст распознан не полностью или некорректно.
    Проверяем размеры объектов и поля.
    """
    standart_fields = ('user', 'labor date', 'clock in', 'clock out')

    for key, data in datas.items():
        data_keys = data.keys()
        print(data_keys)
        check_length = len(standart_fields) == len(data_keys)
        if not check_length:
            print(f'''Нестандартная длинна последовательности.
            data_keys = {len(data_keys)}, standart_fields = {len(standart_fields)}
            Объект: {key}
            ''')

        check_fields = all([ field in data_keys  for field in standart_fields ])
        if check_fields:
            # успешно, не прерывать
            ...
        else:
            # вставить обновление для полей
            # если подключать градио, то стои и изображение вывести, я думаю
            missing_fields = list(filter(None,[ '' if field in data.keys() else field for field in standart_fields ]))
            print(f'Объект: {key}, Отсутствующие поля {missing_fields}')
            # вывести какой объект проверить и что дополнить, пользовательский ввод
            cli(True, missing_fields)
            ...

res = integrity_check(text_analysis(path_folder = './img/', reading_img = reading_img))


# + проверку
# Добавить ручную правку, 
# добавить вывод для сравнения фото с тем что нашёл
# требования к фото
#   перпендикулярно экрану
# мысль, может обрезать фото, 
# стоит заняться обработкой изображений

print(res)

def cli(is_Edit_Mode: bool = False, val_Edit: list = [], datas: dict = {} , / ) -> None:
    """
    Ручной ввод параметров, об рабочем времени.

    Args:
        is_Edit_Mode type bool режим редактирования или стандартной работы ( Default False ):
        - True редактирует конкретный параметр
        - False стандартный режим работы, ручной ввод всех параметров

        val_Edit type list - список параметров для редактирования.
        Возможные параметры ( 'user', 'labor date', 'clock in', 'clock out' )

        datas изменяемый dict

    Return:
        None
    """
    # + проверок надо целый вагон
    type_answer = {"n","no","н","нет"}
    if is_Edit_Mode:
        ...
    else:
        while True:

            # clock in
            h_start = enter_val("Час начала работы")
            m_start = enter_val("Минуты начала работы")
            
            # clock out
            h_end = enter_val("Час завершения работы")
            m_end = enter_val("Минуты завершения работы")

            wt = calc_time(h_start,m_start,h_end,m_end)
            print("[bold][black]Вы работали:[black] [green]{x}[green][/bold]".format(x = wt))
            all_time = accomulate_value(wt)
            answer = input("Продолжим? Y = yes/N = no. ( Default Y ) : " )
            if answer in type_answer:
                print(f"{str(all_time):*^21}")
                return

def enter_val(describing_words: str,/) -> int:
    """
    Обёртка над input. Проверка на число

    Args:
        describing_words is input([prompt]) вид input(f"{describing_words}: " )

    Returns: 
        int
    """
    while True:
        input_data = input(f"{describing_words}: " )
        if input_data.isdigit():
            input_data = int(input_data)
            return input_data
        else:
            print("На вход только число!")

# cli()

# wt = calc_time(2,0,3,15)
# all_time = accomulate_value(wt)
# print(all_time)

# wt = calc_time(2,0,3,15)
# all_time = accomulate_value(wt)
# print(all_time)

############## промежуточный вывод #############
# дельту можно сложить в ручную, sum не работает
# сложности. не встретил. Наверно в описании функций

# ############### блок теста################

# ##########################################


# v2
# пока не получилось
# from collections import namedtuple

# class Working_time_calculation:
#     def __init__(self, 
#                  start_hours: int, 
#                  start_minutes: int, 
#                  end_hours: int, 
#                  end_minutes: int
#                  ):
#         self.start_hours = start_hours
#         self.start_minutes = start_minutes
#         self.end_hours = end_hours
#         self.end_minutes = end_minutes
#         self.pt = self.parameters_time()

#     @staticmethod
#     def parameters_time():
#         Time_naming = namedtuple('Time_naming', ['hours', 'minutes'])
#         def pt(hours: int, minutes: int) -> tuple: # parameters_time
#             return Time_naming(
#                 hours,
#                 minutes
#             )
#         return pt

#     @staticmethod
#     def delta_time(start: tuple, end: tuple) -> tuple:
#         time_start = dt.timedelta( 
#             hours = start.hours,
#             minutes = start.minutes )
#         time_end = dt.timedelta( 
#             hours = end.hours, 
#             minutes = end.minutes) 
        
#         work_time = time_end - time_start
#         return "work_time", work_time

#     def time_calc(self):
#         time_difference = self.delta_time(
#             self.pt(
#                 self.start_hours,
#                 self.start_minutes),
#             self.pt(
#                 self.end_hours,
#                 self.end_minutes)
#             )
#         return time_difference

#     def __str__(self):
#         return "last time {x[0]}: {x[1]}".format( x = self.time_calc())

# time_calc = Working_time_calculation(2,0,3,15)
# print(time_calc)