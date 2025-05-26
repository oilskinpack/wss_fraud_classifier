import matplotlib.pyplot as plt
import seaborn as sns

#Функция для вывода корреляций между признаком и остальными признаками
def show_corr_features_with(p_name,df,pos=True):
    """Функция для вывода барплота корреляций между признаком и остальными признаками

    Parameters
    ----------
    p_name
        Имя параметра
    df
        Датафрейм
    pos, optional
        Показывать признаки с положительной или отрицательной корреляцией, по умолчанию Положительная
    """
    my_corr = df.corr(numeric_only=True)[p_name].sort_values(ascending=False).dropna(axis=0).reset_index().drop(index=0)
    if(pos):
        corr = my_corr [my_corr [p_name] > 0]
    else:
        corr = my_corr[my_corr[p_name] < 0].sort_values(ascending=True,by=p_name)
    plt.xticks(rotation=90)
    sns.barplot(x='index', y=p_name, hue='index', data=corr, palette='Set2', legend=False)