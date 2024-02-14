import os
import pandas as pd
import joblib
import numpy as np

TEST_DATA = os.environ.get("TEST_DATA")
MODEL = os.environ.get("MODEL")


def predict(test_data_path, model_type, model_path):
    """
    Make predictions using the trained model and standard scalers for each fold.

    Parameters:
    - test_data_path (str): The path to the CSV file containing the test data.
    - model_type (str): The type of the trained model (e.g., 'lightgbm', 'randomforest').
    - model_path (str): The directory containing the saved models and scalers.

    Returns:
    - sub (pd.DataFrame): DataFrame containing the predicted probabilities for each test sample.
    """
    # Read the test data into a DataFrame
    df = pd.read_csv(test_data_path)
    test_idx = df["ID_code"].values
    predictions = None

    # Iterate over folds for cross-validation
    for FOLD in range(5):
        df = pd.read_csv(test_data_path)

        # Load standard scalers and columns used during training
        std_scalers = joblib.load(
            os.path.join(model_path, f"{model_type}_{FOLD}_std_scaler.pkl")
        )
        cols = joblib.load(os.path.join(model_path, f"{model_type}_{FOLD}_columns.pkl"))

        # Apply standard scaling to relevant columns
        for c in std_scalers:
            std_scaler = std_scalers[c]
            df.loc[:, c] = std_scaler.transform(df[c].to_frame())

        # Load the trained classifier for the fold
        clf = joblib.load(os.path.join(model_path, f"{model_type}_{FOLD}.pkl"))

        # Select relevant columns and make predictions
        df = df[cols]
        preds = clf.predict_proba(df)[:, 1]

        # Aggregate predictions across folds
        if FOLD == 0:
            predictions = preds
        else:
            predictions += preds

    # Average predictions across folds
    predictions /= 5

    # Create a DataFrame with test IDs and predicted probabilities
    sub = pd.DataFrame(
        np.column_stack((test_idx, predictions)), columns=["ID_code", "target"]
    )
    return sub


if __name__ == "__main__":
    # Example usage of the predict function
    # Replace TEST_DATA and MODEL with your actual test data and model type
    submission = predict(
        test_data_path=TEST_DATA,
        model_type=MODEL,
        model_path="models/",
    )

    # Save the submission file
    submission.to_csv(f"models/cv_{MODEL}_submission.csv", index=False)
