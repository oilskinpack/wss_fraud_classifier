from sklearn.pipeline import Pipeline
from sklearn.model_selection import train_test_split
from sklearn.model_selection import GridSearchCV
from sklearn.base import clone
from Utils.save_load_utils import get_union_raw_data
from Data_prep.prep_pipelines import (get_feature_names_dict
            ,                           build_num_prep_pipeline
                                        ,build_cat_prep_pipeline
                                        ,build_full_prep_pipeline)
from prep.preprocessing_config import get_known_categ_map
from Data_prep.data_preparer import build_preparer
from fitting.fitting_params import param_grid,estimator,score_param
from Utils.logs_utils import save_model_logs


def build_full_pipeline(feature_creator,preprocessor,estimator):
    """Создание полного пайплайн

    Parameters
    ----------
    feature_creator
        Пайплайн создания признаков
    preprocessor
        Пайплайн препроцессинга
    estimator
        Алгоритм ML sklearn

    Returns
    -------
        Полный готовый к обучению пайплайн
    """
    full_pipeline = Pipeline([
    ('feature_creator', feature_creator),
    ('preprocessor', preprocessor),
    ('estimator', estimator)
    ])
    return full_pipeline

def fit_model(orig_data,full_pipeline,param_grid,score_param):
    #Получаем признаки и целевую переменную
    X = orig_data.drop('Ошибка',axis=1)
    y = orig_data['Ошибка']

    #Разбивка данных
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.15, random_state=42,stratify=y)
    grid = GridSearchCV(full_pipeline
                    ,param_grid=param_grid
                    ,verbose=3
                    ,cv=5
                    ,scoring=score_param)
    grid.fit(X_train,y_train)

    preds = grid.predict(X_test)

    return (grid,y_test,preds)


def run_ml_pipeline():
    """Метод, выполняющий полный цикл, а именно:
     объединяет сырые данные
    - создает пайплайны feature,preprocessor и estimator
    - создает финальный пайплайн
    - делит данные и обучает на них grid search cv
    - сохраняет лог с результатами теста и возвращает обученный DataGrid

    Returns
    -------
        Обученный DataGrid
    """
    orig_data = get_union_raw_data()
    feature_pipeline_for_model = build_preparer()  # Для основной модели
    feature_pipeline_for_names = build_preparer()  # Только для получения имен признаков

    # Получаем имена признаков (не влияет на основной пайплайн)
    feature_names_dict = get_feature_names_dict(feature_pipeline_for_names, orig_data)
    known_categories = get_known_categ_map(feature_names_dict['cat'])

    num_prep_pipeline = build_num_prep_pipeline() #Получение препроцессора для числовых колонок
    cat_prep_pipeline = build_cat_prep_pipeline(known_categories) #Получение категориальных колонок

    preprocessor_pipeline = build_full_prep_pipeline(num_preprocessing_pipeline=num_prep_pipeline
                            ,num_features=feature_names_dict['num']
                            ,cat_preprocessing_pipeline=cat_prep_pipeline
                            ,cat_features=feature_names_dict['cat'])       #Препроцессор


    # Строим основной пайплайн с НЕобученным feature_pipeline_for_model
    full_pipeline = build_full_pipeline(
        feature_creator=feature_pipeline_for_model,  # Чистый, необученный пайплайн
        preprocessor=preprocessor_pipeline,
        estimator=estimator
    )

    #Обучение
    grid,y_test,preds = fit_model(orig_data=orig_data
            ,full_pipeline=full_pipeline
            ,param_grid=param_grid
            ,score_param=score_param)

    save_model_logs(grid,estimator,param_grid,y_test,preds)

    return grid.best_estimator_



