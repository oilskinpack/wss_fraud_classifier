from sklearn.metrics import ConfusionMatrixDisplay, classification_report, accuracy_score,confusion_matrix
from datetime import datetime
from datetime import UTC
import os
import matplotlib.pyplot as plt
from Utils.save_load_utils import save_model


def save_model_logs(grid,estimator,param_grid,y_test,preds):
    #Исходные данные для имени файла
    est_name = (type(estimator)).__name__
    today = datetime.now().strftime('%H-%M')
    log_name = f'LOG_{est_name}_{today}.txt'

    #Путь
    base_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(base_dir, '..', '..', '06.Outputs', '03.Logs',log_name)

    #Сохранение лога
    save_log_txt(grid,estimator,param_grid,y_test,preds,file_path)
    #Сохранение матрицы ошибок
    save_confmatrix_plot(file_path,preds,y_test)
    #Сохранение модели
    save_model(grid.best_estimator_,log_name)

def save_confmatrix_plot(file_path,preds,y_test):
    """Сохранение матрицы ошибок

    Parameters
    ----------
    file_path
        Путь для сохранения
    preds
        Предсказания
    y_test
        Hold-out
    """
    cons_matr_plot_name = file_path.replace('03.Logs','02.Plots').replace('LOG','ConfMatrix').replace('txt','png')
    ConfusionMatrixDisplay(confusion_matrix(preds, y_test)).plot()
    plt.savefig(cons_matr_plot_name)
    plt.close()
    
    print(f'ConfMatrix.png сохранен')

def save_log_txt(grid,estimator,param_grid,y_test,preds,file_path):
    """Сохранение файла лога с данными об алгоритме, тестируемых параметрах и значениях, а также лучших параметрах и матрице ошибок

    Parameters
    ----------
    grid
        Обученный GridSearchCV
    estimator
        Алгоритм
    param_grid
        Параметры для Grid
    y_test
        Hold-out
    preds
        Предсказания
    file_path
        Путь для сохранения
    """
    log_info = []

    #Добавление инфо о алгоритме и тестируемом диапазоне
    log_info.append(f"Алгоритм: \n{type(estimator)}")
    log_info.append(f'Тестируемый диапазон: \n{param_grid}')

    #Получение словаря лучших значений параметров
    all_grid_params = grid.best_estimator_.get_params()
    all_best_est_params = all_grid_params['estimator'].get_params()
    my_params = [param.split('__')[1] for param in param_grid]
    best_est_params = dict(filter(lambda item: item[0] in my_params,all_best_est_params.items()))
    log_info.append(f'Лучшие параметры: \n{best_est_params}')

    #Репорт
    class_report = classification_report(y_test,preds)
    log_info.append(f'Репорт: \n{class_report}')

    #Сохранение файла
    with open(file_path, 'w',encoding='utf-8') as f:
        log = "\n\n".join(log_info)
        f.write(log)
    print(f'LOG.txt сохранен')




