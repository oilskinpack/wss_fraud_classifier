from collections import defaultdict
import pandas as pd
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.base import clone
import copy

def get_feature_names_dict(preparing_pipeline,orig_data):
    """Получение словаря названий колонок после создания признаков, ключ - тип, значение - список имен признаков

    Parameters
    ----------
    preparing_pipeline
        Пайплайн создающий датафрейм с готовыми признаками
    orig_data
        Сырые данные

    Returns
    -------
        Словарь где ключ - тип, значение - список имен признаков
    """
    # feature_types_dict = defaultdict(list)
    # feature_pipeline = clone(preparing_pipeline)

    # feature_pipeline.fit(orig_data)
    # feature_df = feature_pipeline.transform(orig_data)

    # cat_features = feature_df.select_dtypes(include='object').columns.to_list()
    # num_features = feature_df.select_dtypes(include='float').columns.to_list()

    # feature_types_dict['cat'] = cat_features
    # feature_types_dict['num'] = num_features
    # feature_types_dict
    # return feature_types_dict
    feature_types_dict = defaultdict(list)
    
    # Создаем полную независимую копию пайплайна
    feature_pipeline = copy.deepcopy(preparing_pipeline)

    
    # Разделяем fit и transform
    feature_pipeline.fit(orig_data)
    feature_df = feature_pipeline.transform(orig_data)
    
    # Получаем типы признаков
    cat_features = feature_df.select_dtypes(include='object').columns.tolist()
    num_features = feature_df.select_dtypes(include='float').columns.tolist()
    
    feature_types_dict['cat'] = cat_features
    feature_types_dict['num'] = num_features
    
    return feature_types_dict


def build_num_prep_pipeline():
    """Создание пайплайна препроцессинга для числовых колонок

    Returns
    -------
        Пайплайн
    """
    return Pipeline([('scaler',StandardScaler())])

def build_cat_prep_pipeline(known_categories):
    """Создание пайплайна препроцессинга для категориальных колонок

    Parameters
    ----------
    known_categories
        Словарь, где ключ - название колонки, значение - перечень всех возможных значений
    """
    cat_preprocessing_pipeline = Pipeline([('encoder',OneHotEncoder(drop='first'
                                                                ,sparse_output=False
                                                                ,handle_unknown='ignore'
                                                                ,categories=known_categories))])
    return cat_preprocessing_pipeline

def build_full_prep_pipeline(num_preprocessing_pipeline,num_features,cat_preprocessing_pipeline,cat_features):
    """Создание полного пайплайн препроцессора

    Parameters
    ----------
    num_preprocessing_pipeline
        Пайплайн числовых признаков
    num_features
        Список числовых признаков
    cat_preprocessing_pipeline
        Пайплайн категориальных признаков
    cat_features
        Список категориальных признаков
    """
    transformer = [('num',num_preprocessing_pipeline,num_features)
                ,('cat',cat_preprocessing_pipeline,cat_features)]
    preprocessor = ColumnTransformer(transformers=transformer,verbose_feature_names_out=False)
    return preprocessor

