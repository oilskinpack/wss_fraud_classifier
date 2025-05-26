import re
from prep.preprocessing_config import valid_sys_types,invalid_sys_name,gosts_metal_pipes,bad_chars



def is_valid_sect_name(text):
    """Метод, который будет проверять корректность заполнения секции

    Parameters
    ----------
    text
        Строка с названием секции

    Returns
    -------
        Да - корректное, нет - некорректное
    """
    pattern = r'''
        ^                             # начало строки
        (                             # либо:
            Паркинг                   # точное слово "Паркинг"
        |
            Секция\s+                 # слово "Секция" и пробел(ы)
            (
                \d+                                       # одно число
                (\s*[-–]\s*\d+)?                          # или диапазон (с дефисом и пробелами)
                |                                         # или
                (\d+\s*,\s*)*\d+                          # список с запятыми: 1,2, 3
            )
            (\s*\(Стилобат\))?        # опционально: (Стилобат)
        )
        $                             # конец строки
    '''
    return bool(re.fullmatch(pattern, text, re.VERBOSE))

def extract_part_sys_type(text):
    """Проверяет есть ли значение части системы в допустимых типах, возвращая допустимый

    Parameters
    ----------
    text
        Тип системы

    Returns
    -------
        Допустимое название части системы или "Не определено"
    """
    for t in valid_sys_types:
        if t in text:
            return t
    return invalid_sys_name

#Добавляем колонку Этаж_ОК
def is_valid_floor_name(text):
    """Проверяет корректность заполнения имени уровня

    Parameters
    ----------
    text
        Имя уровня

    Returns
    -------
        Да - корректно, нет - некорректно
    """
    # floor без именованных групп
    floor = r'Этаж -?\d{2} \(отм\. (?:[+-])?\d+,\d{3}\)'
    
    # Одна секция или две через дефис
    pattern = rf'^({floor})(\s*-\s*{floor})?$'
    
    if not re.fullmatch(pattern, text):
        return False

    # Проверка: нет "-0,000"
    if '-0,000' in text:
        return False

    return True


def check_floor_elev(text):
    """Проверяет корректность отметки в имени уровня

    Parameters
    ----------
    text
        Имя уровня

    Returns
    -------
        Ниже нуля, выше нуля, Диапазон или Неверный формат
    """
    # Регулярка: Этаж -01 (отм. ±3,800) – может быть одна или две секции
    pattern_single = r'^Этаж (?P<floor_sign>-?)(?P<floor_num>\d{2}) \(отм\. [+-]?[\d]+,[\d]{3}\)$'
    pattern_range = r'^Этаж (-?\d{2}) \(отм\. [+-]?[\d]+,[\d]{3}\) ?- ?Этаж (-?\d{2}) \(отм\. [+-]?[\d]+,[\d]{3}\)$'

    if re.fullmatch(pattern_range, text):
        return "Диапазон"

    match = re.fullmatch(pattern_single, text)
    if match:
        sign = match.group('floor_sign')
        if sign == '-':
            return "Ниже нуля"
        else:
            return "Выше нуля"

    return "Неверный формат"


def extract_pipe_size(text):
    """Извлекает диаметр стенки из труб

    Parameters
    ----------
    text
        Название трубы

    Returns : (str)
    -------
        Размер трубы строкой (50, 50-50 или 50-50-50)
    """
    pattern = r'(?<!\d)(\d+(?:-\d+)*)(?=,|$)'  # ловим число или комбинацию через дефис в конце строки
    match = re.search(pattern, text)
    if match:
        return match.group(1)
    return 0

def get_accessories_size(text):
    """Достает float значение размера трубы из названия арматуры

    Parameters
    ----------
    text
        Название арматуры

    Returns : (float)
    -------
        Число или 0
    """
    values = text.split(', ')
    try:
        num = float(values[-1])
        return num
    except:
        try:
            num = float(values[-2])
            return num
        except:
            return 0
        
def extract_gost(text):
    """Достает строку с гостом из названия трубы

    Parameters
    ----------
    text
        Название трубы

    Returns
    -------
        Строка с гостом или Не определено
    """
    for gost in gosts_metal_pipes:
            if gost in text:
                return gost
    return invalid_sys_name

def extract_degrees(text):
    """Достает значение угла из названия соед детали

    Parameters
    ----------
    text
       Название соед детали

    Returns : (int)
    -------
        Угол
    """
    match = re.search(r'(\d+)\s*°', text)
    if match:
        return int(match.group(1))
    return 0

def check_bad_chars(txt):
    """Ищет символы в строке, которых быть не должно

    Parameters
    ----------
    txt
        _description_

    Returns
    -------
        _description_
    """
    for ch in bad_chars:
        if ch in txt:
            return False
    return True