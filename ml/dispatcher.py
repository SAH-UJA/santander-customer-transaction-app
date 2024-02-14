import lightgbm as lgb
from sklearn import ensemble
import mlflow

# Dictionary containing predefined models for different algorithms
MODELS = {
    "lightgbm": lgb.LGBMClassifier(
        colsample_bytree=0.4,
        n_estimators=100,
        learning_rate=0.005,
        max_bin=1023,
        min_child_samples=800,
        n_jobs=-1,
        num_leaves=20,
        objective="binary",
        reg_alpha=0.1,
        reg_lambda=0.2,
        metric="auc",
    ),
    "randomforest": ensemble.RandomForestClassifier(
        n_estimators=20, n_jobs=-1, verbose=2
    ),
}

# Dictionary mapping model names to their corresponding MLflow tracking functions
MLFLOW_MODULE = {"lightgbm": mlflow.lightgbm, "randomforest": mlflow.sklearn}
