"""
    Предоставляет инструменты извлечения данных о времени работы из фото или консольно, 
    вычисление итоговой оплаты.

    Точки входа:
    `read_images_and_check_result()` - автоматическая обработка папки с изображениями.
    `cli()`- ручной ввод данных через консольный интерфейс (default).

    Для `read_images_and_check_result`
        Особенности изображения:
            user: name
            labor date: dd/mm/yyyy
            clock in dd/mm/yyyy hh:mm
            clock out dd/mm/yyyy hh:mm
        При изменении формата полей необходимо редактировать `text_analysis`.  
        Создать папку img в корне проекта
"""


import datetime as dt
from collections import namedtuple
from typing import Callable
from rich import print
from PIL import Image, UnidentifiedImageError
import pytesseract
import re
import os
from typing import overload

Time_naming = namedtuple('Time_naming', ['hours', 'minutes'])

def pt(hours: int, minutes: int) -> Time_naming:
    """
    Инициализирует namedtuple "Часы, минуты".

    Args:
        hours (int): Часы в 24-часовом формате (0-23)
        minutes (int): Минуты (0-59)

    Returns:
        Time_naming: Объект именованного кортежа с указанным временем

    Raises:
        ValueError: Если Часы/hours или Минуты/minutes выходят из диапазона
    """

    if not (0 <= hours <= 23):
        raise ValueError("Формат времени 'Часы' указан неверно")
    if not (0 <= minutes <= 59):
        raise ValueError("Формат времени 'Минуты' указан неверно")
    
    return Time_naming(
        hours,
        minutes
    )

def delta_time(start: Time_naming, end: Time_naming) -> dt.timedelta:
    """
    Вычисляет разность между установленным временем.
    Учитывает переход за полночь.

    Args:
        start (Time_naming): Начальное время работы
        end (Time_naming): Финальное время работы

    Returns:
        work_time (dt.timedelta): Разность между финальным и начальным временем.
    """
    time_start = dt.timedelta( 
        hours = start.hours,
        minutes = start.minutes )
    time_end = dt.timedelta( 
        hours = end.hours, 
        minutes = end.minutes) 
    
    work_time = time_end - time_start

    if work_time.days < 0:
        work_time += dt.timedelta(days=1)

    return work_time

def set_accumulate_value() -> Callable[[dt.timedelta], dt.timedelta]:
    """
    Определяет функцию накопитель и возвращает её.  
    Содержит накопительную переменную duration_list (list)

    Returns:
        accumulate_value (Callable[[dt.timedelta], dt.timedelta]): сумматор времени
    """
    duration_list = list()

    def accumulate_value(current_timedelta: dt.timedelta) -> dt.timedelta:
        """
        Суммирует дельту времени.

        Args:
            current_timedelta (dt.timedelta): текущий показатель разности времени

        Returns:
            duration_work (dt.timedelta): суммарное время работы
        """
        duration_list.append(current_timedelta)
        duration_work = sum(duration_list, dt.timedelta(hours=0, minutes=0))
        
        return duration_work
    
    return accumulate_value

def calc_time(
        start_hours: int = 0,
        start_minutes: int = 0,
        end_hours: int = 0,
        end_minutes: int = 0
        ) -> dt.timedelta:
    """
    Интерфейс ввода параметров времени напрямую.

    Args:
        start_hours (int, optional): Начальное время работы Часы (0-23). default 0
        start_minutes (int, optional): Начальное время работы Минуты (0-59). default 0
        end_hours (int, optional): Финальное время работы Часы (0-23). default 0
        end_minutes (int, optional): Финальное время работы Минуты (0-59). default 0

    Returns:
        time_difference (dt.timedelta): Разность между финальным и начальным временем.
    
    """

    time_difference = delta_time(pt(start_hours, start_minutes), pt(end_hours, end_minutes))
    return time_difference

def reading_img(path_folder: str, langs: str = 'eng' ) ->  dict[str, str]: 
    """
    Читает все изображения из папки. Язык чтения английский.  
    Поддержка библиотекой '.jpg', '.jpeg', '.png', '.bmp', '.tiff', '.webp'  
    '.jpg' 100%  
    '.jpeg', '.png', '.bmp', '.tiff', '.webp' тестов не было  

    Args:
        path_folder (str): путь к папке с изображениями
        langs (str, optional): Язык распознавания 'eng', 'osd', 'rus'. default eng  
            дополнительно смотри настройки pytesseract

    Returns:
        text_entry_dict (dict[str, str]): Сырой текст без обработки. key = filename, val = img data

    Raises:
        FileNotFoundError: Если папки нет или директория пуста, не нашёл изображений для чтения
    """

    if not os.path.isdir(path_folder):
        raise FileNotFoundError ('path_folder не указывает на папку')
    
    listfile = os.listdir(path_folder)
    if not listfile:
        raise FileNotFoundError('Пустая директория')

    if os.name == 'nt':
        pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

    valid_extensions = ('.jpg', '.jpeg', '.png', '.bmp', '.tiff', '.webp')
    text_entry_dict = {}
    for file in listfile:
        if not file.lower().endswith(valid_extensions):
            continue
        path = os.path.join(path_folder, file)
        try:
            with Image.open(path) as image:
                text = pytesseract.image_to_string(image, lang=langs)
                text_entry_dict[file] = text
        except UnidentifiedImageError:
            print(f'Возможно битое изображение {path}')
            continue

    if not text_entry_dict:
        raise FileNotFoundError(f"В папке нет поддерживаемых изображений: {path_folder}")

    return text_entry_dict

def text_analysis(*, path_folder:str, reading_img: Callable[[str], dict]) -> dict[str, dict[str, str]]:
    """
    Форматирует текст, полученный из изображения. 

    Args:
        path_folder (str): путь к папке с изображениями
        reading_img (Callable[[str], dict]): одноимённая функция для чтения изображений

    Returns:
        dict (dict[str, dict[str, str])

    Raises:
        ValueError: Вероятно пустая строка у объекта text_entry_dict.
    
    Особенности изображения:
        user: name
        labor date: dd/mm/yyyy
        clock in dd/mm/yyyy hh:mm
        clock out dd/mm/yyyy hh:mm
    """

    # Возможные баги.
    # Разделитель между часами":"минутами, такой же разделитель между параметром и значением полей 'user', 'labor date'.
    # Решение, последние два поля обрабатываются отдельно, в качестве разделителя используется "|".

    text_entry_dict = reading_img(path_folder)
    processed_data = {}

    def build_pattern(regex_query: bool) -> re.Pattern[str]:
        """
        Возвращает скомпилированный regex-шаблон для парсинга строк

        Args:
            regex_query (bool):  
                True - для выборки строк (user, labor date, clock in/out).
                False - специфичный для двух последних строк с датой 12/03/2024

        Returns:
            re.Pattern[str]: скомпилированный шаблон.
        """
            
        if regex_query:
            return re.compile(r'(user:.*)(?=\n)|(labor\sdate:.*)(?=\n)|(clock\s(in|out).*)(?= user)')
        return re.compile(r'\s\d+\/\d+\/\d+\s')     
                                                        
    for el in text_entry_dict.items():
        if not el[1]:
            raise ValueError(f'Вероятно пустая строка. Файл {el[0]}, контент {el[1]}')
    
        text = el[1].strip().lower()
        pattern_res = build_pattern(True)
        pattern = build_pattern(False)
        res = re.finditer(pattern_res, text)
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

def enter_val(describing_words: str,/) -> int:
    """
    Интерфейс над input. Проверка на число, формат. Только положительные.

    Args:
        describing_words (str): Строка приглашение к вводую. Вид input(f"{describing_words}: ")

    Returns: 
        input_data (int): Число введённое пользователем
    """
    limits = {
        "Оплата за час Базовая валюта": None,
        "Разменная монета": 100,
        "default": 3
    }
    max_len = limits.get(describing_words, limits["default"])

    while True:
        input_data = input(f"{describing_words}: ").strip()
        if not input_data.isdigit() or not input_data:
            print("На вход только число")
            continue
 
        if max_len is None or len(input_data) < max_len:
            return int(input_data)
        
        print("Длина превышает формат!")
        

@overload
def cli(is_Edit_Mode: bool = False,/) -> None: ...

@overload
def cli(is_Edit_Mode: bool = True,/, *args) -> dict[str, dict[str, str]]: ...

def cli(is_Edit_Mode = False,/, *args):
    """
    Ввод параметров, о рабочем времени и оплате.  

    Два режима работы: 
    - стандартный ввод
    - режим фото (вызов из функции integrity_check).

    Args:
        is_Edit_Mode (bool): флаг режима работы  
            стандарт ( Default False ) ввод всех параметров
            
        *args: позиционные аргументы, обязательные при is_Edit_Mode = True
            1. dict[str, dict[str, str]]: редактируемый объект
            2. str: ключ записи в словаре
            3. list[str]: список полей для редактирования.
                ( доступные поля 'user', 'labor date', 'clock in', 'clock out' )
        
    Returns:
        None | dict[str, dict[str, str]]
        - None: в стандартном режиме is_Edit_Mode = False
        - dict: модифицированный словарь для is_Edit_Mode = True
    """
    accumulate_value = set_accumulate_value()
    prompt_start = ("Час начала работы","Минуты начала работы")
    prompt_end = ("Час завершения работы","Минуты завершения работы")
    prompt_default = ("Часы","Минуты")
    prompt_hourly_pay = ("Оплата за час Базовая валюта", "Разменная монета")

    def get_valid_val(prompt: tuple[str, str]) -> tuple[int, int]:
        """
        Интерфейс обобщает приглашение часы/минуты, от enter_val 

        Args:
            prompt (tuple[str, str]): приглашение ввести часы, минуты

        Returns:
            tuple[int, int]: часы, минуты
        """
        h_prompt,m_prompt = prompt
        hours = enter_val(h_prompt)
        minutes = enter_val(m_prompt)
        return hours, minutes

    def payment_calc(*args_t: tuple[int, int], wt: dt.timedelta) -> float:
        """
        Цена за время

        Args:
            args_t (tuple[int, int]):стоимость часа
                [0] базовая валюта
                [1] разменная монета
            wt (dt.timedelta): Общее отработанное время

        Returns:
            payment (float): Сумма оплаты, округление до двух знаков.
        """
        one_hp_f, one_hp_p = args_t
        one_hp_in_minutes = round((float(one_hp_f + (one_hp_p / 100)) / 60),5)
        work_time_minutes = wt.total_seconds() / 60
        payment = round(work_time_minutes * one_hp_in_minutes,2)
        return payment
    
    type_answer = {"n","no","н","нет", "nein", "nyet"}
    if is_Edit_Mode:
        datas, key, missing_fields = args
        for missing_field in missing_fields:
            datas[key][missing_field] = "{time[0]}:{time[1]}".format(time = get_valid_val(prompt_default))
        
        one_hp = get_valid_val(prompt_hourly_pay)
        for key, val in datas.items():
            h_start, m_start = map(int, val["clock in"].split(':'))
            h_end, m_end     = map(int, val["clock out"].split(':'))

            work_time = calc_time(h_start,m_start,h_end,m_end)
            payment =  payment_calc(*one_hp, wt = work_time)
            print("[bold] [black]Вы работали:[black] [green]{x}[green]. "
                "[black]Оплата:[black] [green]{p}[green][/bold].".format(x = work_time, p = payment))
            all_time = accumulate_value(work_time)

        all_time_payment =  payment_calc(*one_hp, wt = all_time)
        print(f"{str(all_time):*^21}")
        print(f"Всего заработано: {all_time_payment}")
        return datas
    else:
        one_hp = get_valid_val(prompt_hourly_pay)
        while True:
            h_start, m_start = get_valid_val(prompt_start)
            h_end, m_end = get_valid_val(prompt_end)

            work_time = calc_time(h_start, m_start, h_end, m_end)
            payment = payment_calc(*one_hp, wt = work_time)
            print("[bold] [black]Вы работали:[black] [green]{x}[green]. "
            "[black]Оплата:[black] [green]{p}[green][/bold].".format(x = work_time, p = payment))
            all_time = accumulate_value(work_time)
            answer = input("Продолжим? Y = yes/N = no. ( Default Y = yes ) : " )
            if answer in type_answer:
                all_time_payment =  payment_calc(*one_hp, wt = all_time)
                print(f"{str(all_time):*^21}")
                print(f"Всего заработано: {all_time_payment}")
                return


def integrity_check(datas: dict[str, dict[str, str]], /) -> dict[str, dict[str, str]]:
    """
    Проверка и редактирование выходных данных из функции text_analysis

    Args:
        datas (dict[str, dict[str, str]): данные из text_analysis

    Returns:
        datas (dict[str, dict[str, str]): 
    """
    standart_fields = ('user', 'labor date', 'clock in', 'clock out')
    for key, data in datas.items():
        data_keys = data.keys()
        check_length = len(standart_fields) == len(data_keys)
        if not check_length:
            print(f'''Нестандартная длина последовательности.
            data_keys = {len(data_keys)}, standart_fields = {len(standart_fields)}
            Объект: {key}
            ''')

        check_fields = all([ field in data_keys  for field in standart_fields ])
        if not check_fields:
            missing_fields = list(filter(None,[ '' if field in data.keys() else field for field in standart_fields ]))
            print(f'Объект: {key}, Отсутствующие поля {missing_fields}')
            updated_val = cli(True, datas, key, missing_fields)
            datas.update(updated_val)
    return datas

def read_images_and_check_result(path: str = './img/', /) -> dict[str, dict[str, str]]:
    """
        Читает изображения из папки, проверка целостности данных.

        Args:
            path (str): путь к папке с изображениями (default './img/').

        Returns:
            dict[str, dict[str, str]]: имя изображения и его данные.
    """
    raw_analysis = text_analysis(path_folder = path, reading_img = reading_img)
    return integrity_check(raw_analysis)


if __name__ == "__main__":
    # read_images_and_check_result()
    cli()

