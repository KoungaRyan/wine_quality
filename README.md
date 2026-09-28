# 🍷 Wine Quality — Prédiction de la qualité du vin

Application web **Django** qui prédit la qualité d'un vin (note de 3 à 9) à partir de ses propriétés physico-chimiques, grâce à deux modèles de **Random Forest** entraînés séparément pour le **vin rouge** et le **vin blanc**.

L'utilisateur saisit cinq mesures dans un formulaire et obtient la note de qualité estimée.

---

## Données

Jeu de données public **Wine Quality** (UCI Machine Learning Repository) — vins portugais *Vinho Verde*.

| Fichier | Échantillons | Notes observées |
|---|---|---|
| `winequality-red.csv` | 1 599 | 3 à 8 |
| `winequality-white.csv` | 4 898 | 3 à 9 |

Chaque vin est décrit par 11 variables physico-chimiques (acidité fixe, acidité volatile, acide citrique, sucre résiduel, chlorures, dioxyde de soufre libre et total, densité, pH, sulfates, alcool). La cible `quality` est la médiane d'au moins trois évaluations d'experts sur une échelle de 0 à 10.

> P. Cortez, A. Cerdeira, F. Almeida, T. Matos et J. Reis. *Modeling wine preferences by data mining from physicochemical properties.* Decision Support Systems, Elsevier, 47(4):547-553, 2009. [doi:10.1016/j.dss.2009.05.016](http://dx.doi.org/10.1016/j.dss.2009.05.016)

---

## Modélisation

Le script `wine_quality_app/ml_model.py` applique le même pipeline aux deux types de vin :

1. **Chargement** du CSV (séparateur `;`)
2. **Sélection de variables** avec `SelectKBest(f_classif, k=5)` : on conserve les 5 variables les plus discriminantes selon un test ANOVA
3. **Découpage** entraînement / test : 90 % / 10 % (`random_state=42`)
4. **Entraînement** d'un `RandomForestClassifier` (hyperparamètres par défaut)
5. **Sauvegarde** du modèle avec `joblib`

### Variables retenues

| Vin rouge | Vin blanc |
|---|---|
| Acidité volatile | Acidité volatile |
| Acide citrique | Chlorures |
| Dioxyde de soufre total | Dioxyde de soufre total |
| Sulfates | Densité |
| Alcool | Alcool |

Ces variables correspondent exactement aux champs des formulaires `red_wine_qualityForm` et `white_wine_qualityForm` (`forms.py`).

---

## Structure du projet

```
wine_quality-main/
└── wine_quality/
    ├── manage.py
    ├── db.sqlite3
    ├── wine_quality/               # Configuration Django
    │   ├── settings.py
    │   ├── urls.py                 # Route "" → wine_quality_app.urls
    │   ├── asgi.py
    │   └── wsgi.py
    └── wine_quality_app/           # Application principale
        ├── ml_model.py             # Entraînement des modèles rouge et blanc
        ├── forms.py                # Formulaires de saisie (5 variables par type de vin)
        ├── modelred.joblib         # Modèle vin rouge entraîné
        ├── apps.py
        ├── admin.py
        ├── migrations/
        └── data/
            ├── winequality-red.csv
            ├── winequality-white.csv
            └── winequality.names   # Description du jeu de données
```

---

## Installation

### Prérequis

- Python ≥ 3.10 (requis par Django 5)

### Mise en place

```bash
git clone https://github.com/KoungaRyan/wine_quality.git
cd wine_quality/wine_quality

python -m venv .venv
source .venv/bin/activate        # Windows : .venv\Scripts\activate

pip install "django>=5.0,<5.1" scikit-learn pandas joblib
```

---

## Utilisation

### 1. Entraîner les modèles

Depuis le dossier `wine_quality/` (celui qui contient `manage.py`) :

```bash
python wine_quality_app/ml_model.py
```

Le script génère `modelred.joblib` et `modelwhite.joblib` dans le dossier courant.

> 💡 Il est recommandé de ré-entraîner les modèles plutôt que d'utiliser le `modelred.joblib` versionné : un modèle scikit-learn sérialisé n'est chargeable qu'avec une version de scikit-learn compatible avec celle qui l'a produit.

### 2. Lancer le serveur

```bash
python manage.py migrate
python manage.py runserver
```

L'application est alors accessible sur <http://127.0.0.1:8000/>.

### 3. Prédire en Python (sans l'interface)

```python
import joblib
import pandas as pd

model = joblib.load("modelred.joblib")
vin = pd.DataFrame([{
    "volatile acidity": 0.70,
    "citric acid": 0.00,
    "total sulfur dioxide": 34,
    "sulphates": 0.56,
    "alcohol": 9.4,
}])
print(model.predict(vin))   # ex. [5]
```

---

## État du projet et pistes d'amélioration

La configuration Django, les formulaires et l'entraînement sont en place. Pour que l'interface web soit complète, le dépôt doit encore contenir :

- [ ] `wine_quality_app/urls.py` — référencé par `wine_quality/urls.py` mais absent
- [ ] `wine_quality_app/views.py` — vue qui charge le modèle, valide le formulaire et renvoie la prédiction
- [ ] `wine_quality_app/templates/` — pages HTML (choix du type de vin, formulaire, résultat)
- [ ] `modelwhite.joblib` — non versionné (à régénérer via `ml_model.py`)

Autres améliorations possibles :

- Ajouter un `requirements.txt` et un `.gitignore` (exclure `__pycache__/`, `db.sqlite3`, `*.joblib`)
- Évaluer les modèles sur le jeu de test (accuracy, matrice de confusion) et documenter les scores
- Utiliser le paramètre `k` de `FeaturesSelection` (actuellement fixé à 5 dans la fonction)
- Fixer `random_state` du Random Forest pour des résultats reproductibles
- Pour un déploiement : sortir `SECRET_KEY` dans une variable d'environnement, passer `DEBUG = False` et renseigner `ALLOWED_HOSTS`

---

## Technologies

Python · Django 5 · scikit-learn · pandas · joblib · SQLite

## Auteur

**Ryan Kounga** — [@KoungaRyan](https://github.com/KoungaRyan)
