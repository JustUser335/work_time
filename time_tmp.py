# import datetime as dt 
# основное внимание в реализации уделяется эффективному извлечению атрибутов для форматирования и обработки выходных данных.

# для начала выведем все доступные методы
# сигнатуры методов?

#Общие свойства 
#Типы date, datetime, time, и timezoneобладают следующими общими характеристиками:
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

    def accomulate_value(current_timedelta: dt.timedelta):
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
    tuple(str, data) 
    str = "work_time"
    data = dt.timedelta
    """
    time_difference = delta_time(pt(start_hours,start_minutes),pt(end_hours,end_minutes))
    return time_difference

accomulate_value = set_accomulate_value()

def cli():
    # проверок надо целый вагон
    type_answer = {"n","no","н","нет"}
    while True:
        h_start = int(input("Час начала работы: " ))
        m_start = int(input("Минуты начала работы: " ))
        h_end = int(input("Час завершения работы: " ))
        m_end = int(input("Минуты завершения работы: " ))
        wt = calc_time(h_start,m_start,h_end,m_end)
        print("[bold][black]Вы работали:[black] [green]{x}[green][/bold]".format(x = wt))
        all_time = accomulate_value(wt)
        answer = input("Продолжим? Y = yes/N = no. Default Y: " )
        if answer in type_answer:
            print(f"{str(all_time):*^21}")
            return

cli()

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