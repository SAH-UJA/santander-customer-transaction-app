import os
import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn import metrics
import joblib
import mlflow
from . import dispatcher

mlflow.set_tracking_uri("http://127.0.0.1:5000")

TRAINING_DATA = os.environ.get("TRAINING_DATA")
TEST_DATA = os.environ.get("TEST_DATA")
FOLD = int(os.environ.get("FOLD"))
MODEL = os.environ.get("MODEL")

FOLD_MAPPPING = {
    0: [1, 2, 3, 4],
    1: [0, 2, 3, 4],
    2: [0, 1, 3, 4],
    3: [0, 1, 2, 4],
    4: [0, 1, 2, 3],
}


def train_and_evaluate():
    """
    Train a model, evaluate its performance, and log the results using MLflow.
    """
    df = pd.read_csv(TRAINING_DATA)
    df_test = pd.read_csv(TEST_DATA)
    train_df = df[df.kfold.isin(FOLD_MAPPPING.get(FOLD))].reset_index(drop=True)
    valid_df = df[df.kfold == FOLD].reset_index(drop=True)

    ytrain = train_df.target.values
    yvalid = valid_df.target.values

    train_df = train_df.drop(["ID_code", "target", "kfold"], axis=1)
    valid_df = valid_df.drop(["ID_code", "target", "kfold"], axis=1)

    valid_df = valid_df[train_df.columns]

    std_scalers = {}
    for c in train_df.columns:
        std_scaler = StandardScaler()
        data = pd.concat(
            [train_df[c], valid_df[c], df_test[c]], ignore_index=True
        ).to_frame()
        std_scaler.fit(data)
        train_df.loc[:, c] = std_scaler.transform(train_df[c].to_frame())
        valid_df.loc[:, c] = std_scaler.transform(valid_df[c].to_frame())
        std_scalers[c] = std_scaler

    # Data is ready to train
    clf = dispatcher.MODELS[MODEL]
    clf.fit(train_df, ytrain)
    preds = clf.predict_proba(valid_df)[:, 1]
    roc_auc = metrics.roc_auc_score(yvalid, preds)
    print(roc_auc)

    # Save standard scalers, model, and columns for later use
    joblib.dump(std_scalers, f"models/{MODEL}_{FOLD}_std_scaler.pkl")
    joblib.dump(clf, f"models/{MODEL}_{FOLD}.pkl")
    joblib.dump(train_df.columns, f"models/{MODEL}_{FOLD}_columns.pkl")

    # Log results using MLflow
    with mlflow.start_run():
        # Log model parameters
        mlflow.log_params(clf.get_params())

        # Log evaluation metrics
        mlflow.log_metric("roc_auc", roc_auc)

        # Log model
        dispatcher.MLFLOW.get(MODEL).log_model(clf, MODEL)


if __name__ == "__main__":
    train_and_evaluate()
