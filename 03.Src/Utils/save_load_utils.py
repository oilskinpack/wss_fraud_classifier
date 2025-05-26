import os
import pandas as pd
from joblib import dump,load


def get_union_raw_data():
    """Собирает все сырые датасеты, объединяя их в один датафрейм

    Returns : pd.Dataframe
    -------
        Объединенный датафрейм с сырыми данными
    """

    # Путь к текущему .py-файлу (где находится эта функция)
    base_dir = os.path.dirname(os.path.abspath(__file__))

    # Путь к папке с данными (относительно этого файла)
    dir_path = os.path.join(base_dir, '..', '..', '01.Data', '01.Raw')
    # dir_path = os.path.join('..','..','01.Data','01.Raw')
    file_names = os.listdir(dir_path)

    full_df = None
    for file_name in file_names:
        data_path = os.path.join(dir_path,file_name)
        df = pd.read_excel(data_path,sheet_name='Отчет')
        df['Наименование файла'] = file_name
        if(full_df is None):
            full_df = df
        else:
            full_df = pd.concat([full_df,df],axis=0)
    full_df = full_df.reset_index(drop=True)
    return full_df

def save_model(final_model,log_name):
    name = log_name.replace('LOG','dev_model_').replace('txt','joblib')
    base_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(base_dir, '..', '..', '06.Outputs', '01.Models',name)
    dump(final_model,file_path)
    print(f'{name} сохранена')

def load_model(model_name):
    base_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(base_dir, '..', '..', '06.Outputs', '01.Models',model_name)
    model = load(file_path)
    return model


