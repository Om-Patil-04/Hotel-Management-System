from scipy.stats import randint, uniform

from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier, AdaBoostClassifier

from lightgbm import LGBMClassifier
from xgboost import XGBClassifier
from catboost import CatBoostClassifier


LIGHTGBM_PARAMS = {
    'n_estimators': randint(200, 1200),
    'max_depth': randint(3, 12),
    'learning_rate': uniform(0.01, 0.3),
    'num_leaves': randint(16, 128),
    'boosting_type': ['gbdt', 'dart'],
    'objective': ['binary'],
    'subsample': uniform(0.6, 1.0),
    'min_child_samples': randint(10, 100),
    'reg_alpha': uniform(0.0, 1.0),
    'reg_lambda': uniform(0.0, 1.0),
    'colsample_bytree': uniform(0.6, 1.0),
}

XGBOOST_PARAMS = {
    'n_estimators': randint(200, 1200),
    'max_depth': randint(3, 12),
    'learning_rate': uniform(0.01, 0.3),
    'subsample': uniform(0.6, 1.0),
    'colsample_bytree': uniform(0.6, 1.0),
    'gamma': uniform(0.0, 5.0),
    'min_child_weight': randint(1, 20),
    'reg_alpha': uniform(0.0, 1.0),
    'reg_lambda': uniform(0.0, 5.0),
    'booster': ['gbtree'],
    'objective': ['binary:logistic'],
}


RANDOM_FOREST_PARAMS = {
    'n_estimators': randint(100, 1000),
    'max_depth': randint(5, 30),
    'min_samples_split': randint(2, 20),
    'min_samples_leaf': randint(1, 10),
    'max_features': ['sqrt', 'log2'],
}

ADABOOST_PARAMS = {
    'n_estimators': randint(50, 500),
    'learning_rate': uniform(0.01, 1.0),
}

MODEL_REGISTRY = {
    'LightGBM': LGBMClassifier(random_state=42, class_weight='balanced', verbosity = 1, force_row_wise=True),

    'XGBoost': XGBClassifier(eval_metric='logloss',random_state=42),

    'RandomForest': RandomForestClassifier(random_state=42),

    'AdaBoost': AdaBoostClassifier(estimator=DecisionTreeClassifier(max_depth=1),random_state=42)
}

RANDOM_SEARCH_PARAMS = {
    'LightGBM': LIGHTGBM_PARAMS,
    'RandomForest': RANDOM_FOREST_PARAMS,
    'XGBoost': XGBOOST_PARAMS,
    'AdaBoost': ADABOOST_PARAMS,
}
