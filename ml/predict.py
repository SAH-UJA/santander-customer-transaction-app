import os
import pandas as pd
import joblib
import numpy as np

TEST_DATA = os.environ.get("TEST_DATA")
MODEL = os.environ.get("MODEL")


def predict(test_data_path, model_type, model_path):
    df = pd.read_csv(test_data_path)
    test_idx = df["ID_code"].values
    predictions = None

    for FOLD in range(5):
        df = pd.read_csv(test_data_path)
        std_scalers = joblib.load(
            os.path.join(model_path, f"{model_type}_{FOLD}_std_scaler.pkl")
        )
        cols = joblib.load(os.path.join(model_path, f"{model_type}_{FOLD}_columns.pkl"))
        for c in std_scalers:
            std_scaler = std_scalers[c]
            df.loc[:, c] = std_scaler.transform(df[c].to_frame())

        clf = joblib.load(os.path.join(model_path, f"{model_type}_{FOLD}.pkl"))

        df = df[cols]
        preds = clf.predict_proba(df)[:, 1]

        if FOLD == 0:
            predictions = preds
        else:
            predictions += preds

    predictions /= 5

    sub = pd.DataFrame(
        np.column_stack((test_idx, predictions)), columns=["ID_code", "target"]
    )
    return sub


if __name__ == "__main__":
    submission = predict(
        test_data_path=TEST_DATA,
        model_type=MODEL,
        model_path="models/",
    )
    submission.loc[:, "ID_code"] = submission.loc[:, "ID_code"]
    submission.to_csv(f"models/lgb_submission.csv", index=False)
