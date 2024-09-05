#wine_qualiy_app/model.py
import joblib
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
import pandas as pd

donnees = pd.read_csv("wine_quality_app/data/winequality-red.csv", sep= ";")
X_red = donnees.drop('quality', axis=1)  # Caractéristiques
y_red = donnees['quality']  # Variable cible

#selection des variables explicative
def FeaturesSelection(data,y,k:int):
    from sklearn.feature_selection import SelectKBest, f_classif


    # Sélection des K meilleures caractéristiques
    selector = SelectKBest(score_func=f_classif, k=5)
    data_new = selector.fit_transform(data, y)

    # Variables sélectionnées
    selected_features = selector.get_support(indices=True)
  
    return data.columns[selected_features]

data_red_X=X_red[FeaturesSelection(X_red,y_red,5)]
X_train, X_test, y_train, y_test = train_test_split(data_red_X, y_red, test_size=0.1, random_state=42)

modelred = RandomForestClassifier()
modelred.fit(X_train, y_train)

joblib.dump(modelred, 'modelred.joblib')


# modele pour le vin blanc

donnees = pd.read_csv("wine_quality_app/data/winequality-white.csv", sep= ";")
X_white = donnees.drop('quality', axis=1)  # Caractéristiques
y_white = donnees['quality']  # Variable cible
data_white_X=X_white[FeaturesSelection(X_white,y_white,5)]
X_train, X_test, y_train, y_test = train_test_split(data_white_X, y_white, test_size=0.1, random_state=42)

modelwhite = RandomForestClassifier()
modelwhite.fit(X_train, y_train)

joblib.dump(modelwhite, 'modelwhite.joblib')



