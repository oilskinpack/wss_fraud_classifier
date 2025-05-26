import re
from prep.preprocessing_config import default_numeric_value

def try_to_float_parse(text):
    """Безопасно превращает текст в число float

    Parameters
    ----------
    text
        Текстовое представление числа

    Returns : (float)
    -------
        Число или 0 если не удалось распарсить
    """
    try:
        num = float(text)
        return num
    except:
        return default_numeric_value
    
def сheck_degree(degree):
    """Проверка кратности 5

    Returns : (str)
    -------
        Кратно или Некратно
    """
    if (degree % 5) == 0 and (degree != 0):
        return "Кратно"
    return "Некратно"

#Функция конвертации в float
def convert_to_double(value):
    """Метод перевода числовых колонок в float

    Parameters
    ----------
    value
        Колонка

    Returns
    -------
        Double, если успех, value - если неуспех
    """
    try:
        return value.astype(float)
    except:
            return value