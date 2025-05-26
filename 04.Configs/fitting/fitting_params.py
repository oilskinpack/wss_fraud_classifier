from sklearn.ensemble import GradientBoostingClassifier

#Алгоритм
estimator = GradientBoostingClassifier()


best_params = {'estimator__max_depth': [8]
               , 'estimator__max_features': [None]
               , 'estimator__min_samples_leaf': [1]
               , 'estimator__min_samples_split': [8]
               , 'estimator__n_estimators': [80]}

#Параметры
n_estimators = [20,30,40,50,60,70,80,90,100]
max_depth = [2,3,4,5,6,7,8]
min_samples_leaf = [1,4,8]
min_samples_split = [1,4,8]
max_features = [None]

# param_grid = {'estimator__n_estimators':n_estimators
#               ,'estimator__max_depth':max_depth
#               ,'estimator__max_features':max_features
#               ,'estimator__min_samples_split':min_samples_split
#               ,'estimator__min_samples_leaf': min_samples_leaf
#               }
param_grid = best_params

score_param = 'f1'




