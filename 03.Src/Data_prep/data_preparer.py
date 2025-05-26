from sklearn.pipeline import Pipeline
from Data_prep.prep_transformers import (SectionCheck
                                         ,SplitEPSection
                                         ,CheckPartSysName
                                         ,CheckPartSysType
                                         ,CheckFloorName
                                         ,CheckFloorElev
                                         ,AddServiceColumns
                                         ,PreprocessMetalPipes
                                         ,PreprocessPlasticPipes
                                         ,PreprocessPrefab
                                         ,PreprocessAccessories
                                         ,PreprocessEquipment
                                         ,PreprocessInsulation
                                         ,CheckTotal
                                         ,CheckSKName
                                         ,CheckType
                                         ,SplitPipeSize
                                         ,ExtractSortament
                                         ,ExtractDegree
                                         ,WithoutBadChars
                                         ,FillErrLog
                                         ,DropCols
                                         ,ConvertToFloat)

def build_preparer():
    """Создает и возвращает pipeline для преобразования сырых данных в колонки-фичи для дальнейшего препроцессинга

    Returns
    -------
        Пайплайн для конвертации сырых данных в данные с фичами
    """
    preparing_transformer = [
                    ('SectionCheck',SectionCheck())                     #Добавляются колонки Секция_ОК, Секция_Паркинг, Секция_Стилобат
                    ,('SplitEPSection',SplitEPSection())                #Колонка ЕП секция делится на 2 колонки (Часть системы и Этаж)
                    ,('CheckPartSysName',CheckPartSysName())            #Добавляются Часть системы_ОК и Часть системы_Регл
                    ,('CheckPartSysType',CheckPartSysType())            #Вытаскиваю первую часть параметра Часть системы
                    ,('CheckFloorName', CheckFloorName())               #Добавляется колонка Этаж_ОК       
                    ,('CheckFloorElev',CheckFloorElev())                #Добавляется колонка Этаж_Отметка (выше ниже диапазон)
                    ,('AddServiceColumns',AddServiceColumns())          #Число СК, Вид, Тип, Размер, Толщина стенки
                    ,('PreprocessMetalPipes',PreprocessMetalPipes())    #Парсинг параметров мет труб и СДТ
                    ,('PreprocessPlasticPipes',PreprocessPlasticPipes()) #Парсинг параметров пп труб и СДТ
                    ,('PreprocessPrefab',PreprocessPrefab())             #Парсинг параметров префаба
                    ,('PreprocessAccessories',PreprocessAccessories())   #Парсинг параметров арматуры
                    ,('PreprocessEquipment',PreprocessEquipment())       #Парсинг параметров оборудования
                    ,('PreprocessInsulation',PreprocessInsulation())     #Парсинг параметров изоляции
                    ,('CheckTotal',CheckTotal())                         #Проверка что Итого != 0
                    ,('CheckSKName',CheckSKName())                       #Добавляем колонку Тип СК_Регл
                    ,('CheckType',CheckType())                           #Добавляем колонку Тип_Регл
                    ,('SplitPipeSize',SplitPipeSize())                   #Разбивка размера
                    ,('ExtractSortament',ExtractSortament())             #Сортамент
                    ,('ExtractDegree',ExtractDegree())                   #Добавляем колонку по углу (кратно, некратно)
                    ,('WithoutBadChars',WithoutBadChars())               #Ищем недопустимые символы в колонке СК
                    ,('DropCols',DropCols())                             #Структурируем колонки
                    ,('ConvertToFloat',ConvertToFloat())                 #Конвертация во float (кроме строковых колонок)
                    ]
    
    preparing_pipeline = Pipeline(preparing_transformer)
    return preparing_pipeline
    
def build_err_preparer():
    preparing_transformer = [
                    ('SectionCheck',SectionCheck())                     #Добавляются колонки Секция_ОК, Секция_Паркинг, Секция_Стилобат
                    ,('SplitEPSection',SplitEPSection())                #Колонка ЕП секция делится на 2 колонки (Часть системы и Этаж)
                    ,('CheckPartSysName',CheckPartSysName())            #Добавляются Часть системы_ОК и Часть системы_Регл
                    ,('CheckPartSysType',CheckPartSysType())            #Вытаскиваю первую часть параметра Часть системы
                    ,('CheckFloorName', CheckFloorName())               #Добавляется колонка Этаж_ОК       
                    ,('CheckFloorElev',CheckFloorElev())                #Добавляется колонка Этаж_Отметка (выше ниже диапазон)
                    ,('AddServiceColumns',AddServiceColumns())          #Число СК, Вид, Тип, Размер, Толщина стенки
                    ,('PreprocessMetalPipes',PreprocessMetalPipes())    #Парсинг параметров мет труб и СДТ
                    ,('PreprocessPlasticPipes',PreprocessPlasticPipes()) #Парсинг параметров пп труб и СДТ
                    ,('PreprocessPrefab',PreprocessPrefab())             #Парсинг параметров префаба
                    ,('PreprocessAccessories',PreprocessAccessories())   #Парсинг параметров арматуры
                    ,('PreprocessEquipment',PreprocessEquipment())       #Парсинг параметров оборудования
                    ,('PreprocessInsulation',PreprocessInsulation())     #Парсинг параметров изоляции
                    ,('CheckTotal',CheckTotal())                         #Проверка что Итого != 0
                    ,('CheckSKName',CheckSKName())                       #Добавляем колонку Тип СК_Регл
                    ,('CheckType',CheckType())                           #Добавляем колонку Тип_Регл
                    ,('SplitPipeSize',SplitPipeSize())                   #Разбивка размера
                    ,('ExtractSortament',ExtractSortament())             #Сортамент
                    ,('ExtractDegree',ExtractDegree())                   #Добавляем колонку по углу (кратно, некратно)
                    ,('WithoutBadChars',WithoutBadChars())               #Ищем недопустимые символы в колонке СК
                    ,('FillErrLog',FillErrLog())
                    # ,('DropCols',DropCols())                             #Структурируем колонки
                    # ,('ConvertToFloat',ConvertToFloat())                 #Конвертация во float (кроме строковых колонок)
                    ]

    preparing_pipeline = Pipeline(preparing_transformer)
    return preparing_pipeline