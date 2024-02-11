import lightgbm as lgb
from sklearn import ensemble
import mlflow


MODELS = {
    "lightgbm": lgb.LGBMClassifier(
        objective="binary", boosting="gbdt", learning_rate=0.01
    ),
    "randomforest": ensemble.RandomForestClassifier(
        n_estimators=200, n_jobs=-1, verbose=2
    ),
}

MLFLOW = {"lightgbm": mlflow.lightgbm, "randomforest": mlflow.sklearn}
