from sklearn.base import TransformerMixin, BaseEstimator
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
import pandas as pd
import numpy as np
from Utils.string_utils import (is_valid_sect_name
                                ,extract_part_sys_type
                                ,is_valid_floor_name
                                ,check_floor_elev
                                ,extract_pipe_size
                                ,extract_gost
                                ,extract_degrees
                                ,check_bad_chars)
from Utils.numeric_utils import try_to_float_parse,сheck_degree,convert_to_double
from prep.preprocessing_config import (prefab_part_sys_name
                                       ,valid_sys_names
                                       ,invalid_sys_name
                                       ,default_string_value
                                       ,default_numeric_value
                                       ,metal_pipe_names
                                       ,metal_sdt_names
                                       ,pp_pipe_names
                                       ,pp_sdt_names
                                       ,prefab_names
                                       ,pipe_accessories_names
                                       ,equipment_names
                                       ,insulation_names
                                       ,sk_names_map_dict
                                       ,valid_types
                                       ,prop_col_names)


#Класс-трансформер для добавления колонок по секции
class SectionCheck(BaseEstimator, TransformerMixin):
    """Класс-трансформер для добавления колонок по секции

    Parameters
    ----------
    BaseEstimator
        Базовый класс для Estimators
    TransformerMixin
        Базовый класс для Transformers
    """
    def __init__(self):
        self.n_features_in_ = None  # Добавляем обязательный атрибут
    def fit(self,X,y=None):
        # Сохраняем количество фичей
        self.n_features_in_ = X.shape[1]
        return self
    def transform(self,X):
        df = X.copy()

        #Создание колонку с информацией по среднему расположению полостей
        df['Секция_ОК'] = df['Единица приемки (ЕП), Секция'].apply(is_valid_sect_name)
        df['Секция_Стилобат'] = df['Единица приемки (ЕП), Секция'].str.contains('Стилобат') == True
        df['Секция_Паркинг'] = df['Единица приемки (ЕП), Секция'].str.contains('Паркинг') == True

        return df
    

class SplitEPSection(BaseEstimator, TransformerMixin):
    """Класс-трансформер для деления колонки ЕП этаж на 2 колонки

    Parameters
    ----------
    BaseEstimator
        Базовый класс для Estimators
    TransformerMixin
        Базовый класс для Transformers
    """
    def __init__(self):
        self.n_features_in_ = None  # Добавляем обязательный атрибут
    def fit(self,X,y=None):
        # Сохраняем количество фичей
        self.n_features_in_ = X.shape[1]
        return self
    def transform(self,X):
        df = X.copy()

        #Создание колонку с информацией по среднему расположению полостей
        df['Часть системы'] = np.where(df['Единица приемки (ЕП), Этаж'].str.split(', ').apply(lambda x: len(x)) < 2
                                       , prefab_part_sys_name
                                       , df['Единица приемки (ЕП), Этаж'].str.split(', ').str[0])
        df['Этаж'] = np.where(df['Единица приемки (ЕП), Этаж'].str.split(', ').apply(lambda x: len(x)) < 2
                                       , df['Единица приемки (ЕП), Этаж'].str.split(', ').str[0]
                                       , df['Единица приемки (ЕП), Этаж'].str.split(', ').str[1])
        return df
    
#Добавляем колонку ЧастьСистемы_ОК
class CheckPartSysName(BaseEstimator, TransformerMixin):
    """Класс-трансформер для добавления колонки ЧастьСистемы_ОК

    Parameters
    ----------
    BaseEstimator
        Базовый класс для Estimators
    TransformerMixin
        Базовый класс для Transformers
    """
    def __init__(self):
        self.n_features_in_ = None  # Добавляем обязательный атрибут
    def fit(self,X,y=None):
        # Сохраняем количество фичей
        self.n_features_in_ = X.shape[1]
        return self
    def transform(self,X):
        df = X.copy()

        df['ЧастьСистемы_ОК'] = np.where(df['Часть системы'].isin(valid_sys_names)
                                         ,True
                                        #  ,df['Часть системы'].str.split(' ').str[0].isin(valid_sys_names)
                                        ,False
                                         )
        df['Часть системы_Регл'] = np.where(df['ЧастьСистемы_ОК'] == True
                                         ,df['Часть системы']
                                         ,invalid_sys_name)
                                         
        return df
    
class CheckPartSysType(BaseEstimator, TransformerMixin):
    """Класс-трансформер для добавления колонки ЧастьСистемы_Тип

    Parameters
    ----------
    BaseEstimator
        Базовый класс для Estimators
    TransformerMixin
        Базовый класс для Transformers
    """
    def __init__(self):
        self.n_features_in_ = None  # Добавляем обязательный атрибут
    def fit(self,X,y=None):
        # Сохраняем количество фичей
        self.n_features_in_ = X.shape[1]
        return self
    def transform(self,X):
        df = X.copy()

        df['ЧастьСистемы_Тип'] = df['Часть системы'].apply(extract_part_sys_type)
        return df
    
#Добавляем колонку Этаж_ОК
class CheckFloorName(BaseEstimator, TransformerMixin):
    """Класс-трансформер для добавления колонки Этаж_ОК

    Parameters
    ----------
    BaseEstimator
        Базовый класс для Estimators
    TransformerMixin
        Базовый класс для Transformers
    """
    def __init__(self):
        self.n_features_in_ = None  # Добавляем обязательный атрибут
    def fit(self,X,y=None):
        # Сохраняем количество фичей
        self.n_features_in_ = X.shape[1]
        return self
    def transform(self,X):
        df = X.copy()

        df['Этаж_ОК'] = df['Этаж'].apply(is_valid_floor_name)

        return df


class CheckFloorElev(BaseEstimator, TransformerMixin):
    """Класс-трансформер для добавления колонки Этаж_Отметка

    Parameters
    ----------
    BaseEstimator
        Базовый класс для Estimators
    TransformerMixin
        Базовый класс для Transformers
    """
    def __init__(self):
        self.n_features_in_ = None  # Добавляем обязательный атрибут
    def fit(self,X,y=None):
        # Сохраняем количество фичей
        self.n_features_in_ = X.shape[1]
        return self
    def transform(self,X):
        df = X.copy()

        df['Этаж_Отметка'] = df['Этаж'].apply(check_floor_elev)

        return df
    

class AddServiceColumns(BaseEstimator, TransformerMixin):
    """Класс-трансформер для добавления колонок Число СК, Вид, Тип, Размер, Толщина стенки

    Parameters
    ----------
    BaseEstimator
        Базовый класс для Estimators
    TransformerMixin
        Базовый класс для Transformers
    """
    def __init__(self):
        self.n_features_in_ = None  # Добавляем обязательный атрибут
    def fit(self,X,y=None):
        # Сохраняем количество фичей
        self.n_features_in_ = X.shape[1]
        return self
    def transform(self,X):
        df = X.copy()

        df['Число СК'] = df['СК'].str.split(', ').apply(lambda x:len(x))
        df['Вид'] = default_string_value
        df['Тип'] = default_string_value
        df['Размер'] = default_numeric_value
        df['Толщина стенки'] = default_numeric_value

        return df
    
class PreprocessMetalPipes(BaseEstimator, TransformerMixin):
    """Класс-трансформер для добавления колонок Вид, Размер, толщина для металлических труб и СДТ

    Parameters
    ----------
    BaseEstimator
        Базовый класс для Estimators
    TransformerMixin
        Базовый класс для Transformers
    """
    def __init__(self):
        self.n_features_in_ = None  # Добавляем обязательный атрибут
    def fit(self,X,y=None):
        # Сохраняем количество фичей
        self.n_features_in_ = X.shape[1]
        return self
    def transform(self,X):
        df = X.copy()

        #Труба металлическая
        df['Вид'] = np.where(df['Тип СК'].isin(metal_pipe_names)
                    ,df['СК'].str.split(', ').str[1]
                    ,df['Вид'])
        df['Размер'] = np.where(df['Тип СК'].isin(metal_pipe_names)
                    ,df['СК'].str.split(', ').str[-2]
                    ,df['Размер'])
        df['Толщина стенки'] = np.where(df['Тип СК'].isin(metal_pipe_names)
                    ,df['СК'].str.split(', ').str[-1].apply(try_to_float_parse)
                    ,df['Толщина стенки'])
        # df[df['Тип СК'] == sk_name]

        #Металлическая соединительная деталь трубы
        df['Вид'] = np.where(df['Тип СК'].isin(metal_sdt_names)
                    ,df['СК'].str.split(', ').str[2]
                    ,df['Вид'])
        df['Тип'] = np.where(df['Тип СК'].isin(metal_sdt_names)
                    ,df['СК'].str.split(', ').str[1]
                    ,df['Тип'])
        df['Размер'] = np.where(df['Тип СК'].isin(metal_sdt_names)
                    ,df['СК'].str.split(', ').str[-2]
                    ,df['Размер'])
        df['Толщина стенки'] = np.where(df['Тип СК'].isin(metal_sdt_names)
                    ,df['СК'].str.split(', ').str[-1].apply(try_to_float_parse)
                    ,df['Толщина стенки'])
        # df[df['Тип СК'] == sk_name]

        return df
    

class PreprocessPlasticPipes(BaseEstimator, TransformerMixin):
    """Класс-трансформер для добавления колонок Вид,Тип, Размер, толщина для пластиковых труб и СДТ

    Parameters
    ----------
    BaseEstimator
        Базовый класс для Estimators
    TransformerMixin
        Базовый класс для Transformers
    """
    def __init__(self):
        self.n_features_in_ = None  # Добавляем обязательный атрибут
    def fit(self,X,y=None):
        # Сохраняем количество фичей
        self.n_features_in_ = X.shape[1]
        return self
    def transform(self,X):
        df = X.copy()

        df['Вид'] = np.where(df['Тип СК'].isin(pp_pipe_names)
                    ,df['СК'].str.split(', ').str[1]
                    ,df['Вид'])
        df['Размер'] = np.where(df['Тип СК'].isin(pp_pipe_names)
                    ,df['СК'].str.split(', ').str[-1]
                    ,df['Размер'])
        # df[df['Тип СК'] == sk_name]

        df['Вид'] = np.where(df['Тип СК'].isin(pp_sdt_names)
                    ,df['СК'].str.split(', ').str[2]
                    ,df['Вид'])
        df['Тип'] = np.where(df['Тип СК'].isin(pp_sdt_names)
                    ,df['СК'].str.split(', ').str[1]
                    ,df['Тип'])
        df['Размер'] = np.where(df['Тип СК'].isin(pp_sdt_names)
                    ,df['СК'].str.split(', ').str[-1]
                    ,df['Размер'])


        return df


class PreprocessPrefab(BaseEstimator, TransformerMixin):
    """Класс-трансформер для добавления колонок Вид для префаба ВИС

    Parameters
    ----------
    BaseEstimator
        Базовый класс для Estimators
    TransformerMixin
        Базовый класс для Transformers
    """
    def __init__(self):
        self.n_features_in_ = None  # Добавляем обязательный атрибут
    def fit(self,X,y=None):
        # Сохраняем количество фичей
        self.n_features_in_ = X.shape[1]
        return self
    def transform(self,X):
        df = X.copy()

        df['Вид'] = np.where(df['Тип СК'].isin(prefab_names)
                    ,default_string_value
                    ,df['Вид'])


        return df 
    

class PreprocessAccessories(BaseEstimator, TransformerMixin):
    """Класс-трансформер для добавления колонок Тип, Вид, Размер для арматуры

    Parameters
    ----------
    BaseEstimator
        Базовый класс для Estimators
    TransformerMixin
        Базовый класс для Transformers
    """
    def __init__(self):
        self.n_features_in_ = None  # Добавляем обязательный атрибут
    def fit(self,X,y=None):
        # Сохраняем количество фичей
        self.n_features_in_ = X.shape[1]
        return self
    def transform(self,X):
        df = X.copy()

        df['Тип'] = np.where(df['Тип СК'].isin(pipe_accessories_names)
                    ,df['СК'].str.split(', ').str[1]
                    ,df['Тип'])
        df['Вид'] = np.where(df['Тип СК'].isin(pipe_accessories_names)
                    ,df['СК'].str.split(', ').str[2]
                    ,df['Вид'])
        df['Размер'] = np.where(df['Тип СК'].isin(pipe_accessories_names)
                    ,df['СК'].apply(extract_pipe_size)
                    ,df['Размер'])


        return df
    
#Преобразование оборудования
class PreprocessEquipment(BaseEstimator, TransformerMixin):
    """Класс-трансформер для добавления колонок Тип, Вид для оборудования

    Parameters
    ----------
    BaseEstimator
        Базовый класс для Estimators
    TransformerMixin
        Базовый класс для Transformers
    """
    def __init__(self):
        self.n_features_in_ = None  # Добавляем обязательный атрибут
    def fit(self,X,y=None):
        # Сохраняем количество фичей
        self.n_features_in_ = X.shape[1]
        return self
    def transform(self,X):
        df = X.copy()

        df['Тип'] = np.where(df['Тип СК'].isin(equipment_names)
                    ,df['СК'].str.split(', ').str[1]
                    ,df['Тип'])
        df['Вид'] = np.where(df['Тип СК'].isin(equipment_names)
                    ,df['СК'].str.split(', ').str[2]
                    ,df['Вид'])


        return df
    
#Преобразование изоляции
class PreprocessInsulation(BaseEstimator, TransformerMixin):
    """Класс-трансформер для добавления колонок Вид, Размер, толщина стенки для изоляции

    Parameters
    ----------
    BaseEstimator
        Базовый класс для Estimators
    TransformerMixin
        Базовый класс для Transformers
    """
    def __init__(self):
        self.n_features_in_ = None  # Добавляем обязательный атрибут
    def fit(self,X,y=None):
        # Сохраняем количество фичей
        self.n_features_in_ = X.shape[1]
        return self
    def transform(self,X):
        df = X.copy()

        df['Вид'] = np.where(df['Тип СК'].isin(insulation_names)
                    ,df['СК'].str.split(', ').str[1]
                    ,df['Вид'])
        df['Размер'] = np.where(df['Тип СК'].isin(insulation_names)
                    ,df['СК'].str.split(', ').str[-2]
                    ,df['Размер'])
        df['Толщина стенки'] = np.where(df['Тип СК'].isin(insulation_names)
                    ,df['СК'].str.split(', ').str[-1].apply(try_to_float_parse)
                    ,df['Толщина стенки'])
        return df
    

class CheckTotal(BaseEstimator, TransformerMixin):
    """Класс-трансформер для добавления Итого_ОК

    Parameters
    ----------
    BaseEstimator
        Базовый класс для Estimators
    TransformerMixin
        Базовый класс для Transformers
    """
    def __init__(self):
        self.n_features_in_ = None  # Добавляем обязательный атрибут
    def fit(self,X,y=None):
        # Сохраняем количество фичей
        self.n_features_in_ = X.shape[1]
        return self
    def transform(self,X):
        df = X.copy()

        df['Итого_ОК'] = np.where(df['Итого'] != 0, True, False)
        return df
    

class CheckSKName(BaseEstimator, TransformerMixin):
    """Класс-трансформер для добавления Тип_СК_Регл

    Parameters
    ----------
    BaseEstimator
        Базовый класс для Estimators
    TransformerMixin
        Базовый класс для Transformers
    """
    def __init__(self):
        self.n_features_in_ = None  # Добавляем обязательный атрибут
    def fit(self,X,y=None):
        # Сохраняем количество фичей
        self.n_features_in_ = X.shape[1]
        return self
    def transform(self,X):
        df = X.copy()

        df['Тип_СК_Регл'] = np.where(df['Тип СК'].isin(sk_names_map_dict.keys())
                                     , df['Тип СК'].map(sk_names_map_dict)
                                     , invalid_sys_name)


        return df


class CheckType(BaseEstimator, TransformerMixin):
    """Класс-трансформер для добавления Тип_регл

    Parameters
    ----------
    BaseEstimator
        Базовый класс для Estimators
    TransformerMixin
        Базовый класс для Transformers
    """
    def __init__(self):
        self.n_features_in_ = None  # Добавляем обязательный атрибут
    def fit(self,X,y=None):
        # Сохраняем количество фичей
        self.n_features_in_ = X.shape[1]
        return self
    def transform(self,X):
        df = X.copy()

        df['Тип_Регл'] = np.where((df['Тип'].isin(valid_types)) | (df['Тип'] == default_string_value)
                                     , df['Тип']
                                     , invalid_sys_name)


        return df
    
#Парсим размер
class SplitPipeSize(BaseEstimator, TransformerMixin):
    """Класс-трансформер для добавления Размер_Первый,второй, третий, Размер_Кол-во

    Parameters
    ----------
    BaseEstimator
        Базовый класс для Estimators
    TransformerMixin
        Базовый класс для Transformers
    """
    def __init__(self):
        self.n_features_in_ = None  # Добавляем обязательный атрибут
    def fit(self,X,y=None):
        # Сохраняем количество фичей
        self.n_features_in_ = X.shape[1]
        return self
    def transform(self,X):
        df = X.copy()

        df['Размер_Первый'] = default_numeric_value
        df['Размер_Второй'] = default_numeric_value
        df['Размер_Третий'] = default_numeric_value
        df['Размер_Кол-во'] = df['Размер'].astype(str).str.split('-').apply(lambda x:len(x))

        df['Размер_Первый'] = np.where(df['Размер_Кол-во'] < 2
                                       ,df['Размер'].apply(try_to_float_parse)
                                       ,default_numeric_value)

        df['Размер_Первый'] = np.where(df['Размер_Кол-во'] >= 2
                                       ,df['Размер'].astype(str).str.split('-').str[0].apply(try_to_float_parse)
                                       ,df['Размер_Первый'])

        df['Размер_Второй'] = np.where(df['Размер_Кол-во'] >= 2
                                       ,df['Размер'].astype(str).str.split('-').str[1].apply(try_to_float_parse)
                                       ,df['Размер_Второй'])
        
        df['Размер_Третий'] = np.where(df['Размер_Кол-во'] >= 3
                                       ,df['Размер'].astype(str).str.split('-').str[2].apply(try_to_float_parse)
                                       ,df['Размер_Третий'])


        return df

#Добавляем колонку Сортамент
class ExtractSortament(BaseEstimator, TransformerMixin):
    """Класс-трансформер для добавления Вид_Сортамент

    Parameters
    ----------
    BaseEstimator
        Базовый класс для Estimators
    TransformerMixin
        Базовый класс для Transformers
    """
    def __init__(self):
        self.n_features_in_ = None  # Добавляем обязательный атрибут
    def fit(self,X,y=None):
        # Сохраняем количество фичей
        self.n_features_in_ = X.shape[1]
        return self
    def transform(self,X):
        df = X.copy()

        df['Вид_Сортамент'] = np.where((df['Тип СК'].isin(metal_pipe_names)) | (df['Тип СК'].isin(metal_sdt_names))
                                       ,df['Вид'].apply(extract_gost)
                                       ,default_string_value)

        return df
    
#Добавляем колонку Вид_Угол
class ExtractDegree(BaseEstimator, TransformerMixin):
    """Класс-трансформер для добавления Вид_Угол и Вид_Угол_Кратность

    Parameters
    ----------
    BaseEstimator
        Базовый класс для Estimators
    TransformerMixin
        Базовый класс для Transformers
    """
    def __init__(self):
        self.n_features_in_ = None  # Добавляем обязательный атрибут
    def fit(self,X,y=None):
        # Сохраняем количество фичей
        self.n_features_in_ = X.shape[1]
        return self
    def transform(self,X):
        df = X.copy()

        df['Вид_Угол'] = np.where(df['Тип'].isin(['Отвод','Тройник'])
                                       ,df['Вид'].apply(extract_degrees)
                                       ,default_numeric_value)
        df['Вид_Угол_Кратность'] = np.where(df['Тип'].isin(['Отвод','Тройник'])
                                       ,df['Вид_Угол'].apply(сheck_degree)
                                       ,default_string_value)

        return df
    

class WithoutBadChars(BaseEstimator, TransformerMixin):
    """Класс-трансформер для добавления СК_Симв_ОК

    Parameters
    ----------
    BaseEstimator
        Базовый класс для Estimators
    TransformerMixin
        Базовый класс для Transformers
    """
    def __init__(self):
        self.n_features_in_ = None  # Добавляем обязательный атрибут
    def fit(self,X,y=None):
        # Сохраняем количество фичей
        self.n_features_in_ = X.shape[1]
        return self
    def transform(self,X):
        df = X.copy()

        df['СК_Симв_ОК'] = np.where(df['СК'].apply(check_bad_chars)
                                       ,True
                                       ,False)
        return df
    
#Конвертация
class ConvertToFloat(BaseEstimator, TransformerMixin):
    """Класс-трансформер для конвертации колонок во float (тех, которые можно перевести). Остальные останутся прежними

    Parameters
    ----------
    BaseEstimator
        Базовый класс для Estimators
    TransformerMixin
        Базовый класс для Transformers
    """
    def __init__(self):
        self.n_features_in_ = None  # Добавляем обязательный атрибут
    def fit(self,X,y=None):
        # Сохраняем количество фичей
        self.n_features_in_ = X.shape[1]
        return self
    def transform(self,X):
        df = X.copy()

        df = df.apply(convert_to_double)


        return df


class DropCols(BaseEstimator, TransformerMixin):
    """Класс-трансформер для удаления лишних и сервисных колонок

    Parameters
    ----------
    BaseEstimator
        Базовый класс для Estimators
    TransformerMixin
        Базовый класс для Transformers
    """
    def __init__(self):
        self.n_features_in_ = None  # Добавляем обязательный атрибут
    def fit(self,X,y=None):
        # Сохраняем количество фичей
        self.n_features_in_ = X.shape[1]
        return self
    def transform(self,X):
        df = X.copy()
        df = df[prop_col_names]
        return df
    
class FillErrLog(BaseEstimator, TransformerMixin):
    """Класс-трансформер для заполнения колонки Список ошибок

    Parameters
    ----------
    BaseEstimator
        Базовый класс для Estimators
    TransformerMixin
        Базовый класс для Transformers
    """
    def __init__(self):
        self.n_features_in_ = None  # Добавляем обязательный атрибут
    def fit(self,X,y=None):
        # Сохраняем количество фичей
        self.n_features_in_ = X.shape[1]
        return self
    def transform(self,X):
        df = X.copy()
        df['Список ошибок'] = ''


        df['Список ошибок'] = np.where(df['Секция_ОК']
                                ,df['Список ошибок']
                                ,df['Список ошибок'].apply(lambda x: x + '\nНекорректное значение секции'))
        
        df['Список ошибок'] = np.where(df['ЧастьСистемы_ОК']
                                ,df['Список ошибок']
                                ,df['Список ошибок'].apply(lambda x: x + '\nНекорректное значение части системы'))
        
        df['Список ошибок'] = np.where(df['Этаж_ОК']
                        ,df['Список ошибок']
                        ,df['Список ошибок'].apply(lambda x: x + '\nНекорректное значение имени этажа'))
        
        df['Список ошибок'] = np.where(df['Этаж_Отметка']
                ,df['Список ошибок']
                ,df['Список ошибок'].apply(lambda x: x + '\nНекорректное значение отметки'))
        
        df['Список ошибок'] = np.where(df['Итого_ОК']
                                ,df['Список ошибок']
                                ,df['Список ошибок'].apply(lambda x: x + '\nИтого 0'))
        
        df['Список ошибок'] = np.where(df['Тип_СК_Регл'] != invalid_sys_name
                                ,df['Список ошибок']
                                ,df['Список ошибок'].apply(lambda x: x + '\nНеверный Тип СК'))
        
        df['Список ошибок'] = np.where(df['Тип_Регл'] != invalid_sys_name
                                ,df['Список ошибок']
                                ,df['Список ошибок'].apply(lambda x: x + '\nНеверный параметр тип'))
        
        df['Список ошибок'] = np.where(df['Вид_Сортамент'] != invalid_sys_name
                        ,df['Список ошибок']
                        ,df['Список ошибок'].apply(lambda x: x + '\nНеизвестный сортамент'))
        
        df['Список ошибок'] = np.where(df['Вид_Угол_Кратность'] != "Некратно"
                ,df['Список ошибок']
                ,df['Список ошибок'].apply(lambda x: x + '\nУгол некратен 5'))
        
        df['Список ошибок'] = np.where(df['СК_Симв_ОК'] == 1
                                        ,df['Список ошибок']
                                        ,df['Список ошибок'].apply(lambda x: x + '\nОбнаружены лишние символы'))


        return df
    



    
