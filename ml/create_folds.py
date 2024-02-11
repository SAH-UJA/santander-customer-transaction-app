import pandas as pd
from sklearn.model_selection import StratifiedKFold
import os


def create_folds(data_path, output_path):
    """
    Create folds for cross-validation and save the resulting DataFrame to a CSV file.

    Parameters:
    - data_path (str): The path to the input CSV file containing the data.
    - output_path (str): The path where the folds CSV file will be saved.
    """
    # Read the input CSV file into a pandas DataFrame
    df = pd.read_csv(data_path)

    # Add a new column 'kfold' and initialize with -1
    df["kfold"] = -1

    # Shuffle the DataFrame to randomize the data
    df = df.sample(frac=1).reset_index(drop=True)

    # Initialize StratifiedKFold for cross-validation with 5 folds
    kf = StratifiedKFold(n_splits=5, shuffle=False)

    # Enumerate through folds and assign fold numbers to corresponding rows
    for fold, (train_idx, val_idx) in enumerate(kf.split(X=df, y=df.target.values)):
        print(
            f"Fold {fold + 1}: Train Size - {len(train_idx)}, Validation Size - {len(val_idx)}"
        )
        df.loc[val_idx, "kfold"] = fold

    # Save the DataFrame with fold information to a new CSV file
    df.to_csv(output_path, index=False)


if __name__ == "__main__":
    # Set the path for the input data and output folds CSV file
    input_data_path = f"{os.getcwd()}/data/raw/train.csv"
    output_folds_path = f"{os.getcwd()}/data/raw/train_folds.csv"

    # Call the function to create folds and save the results
    create_folds(data_path=input_data_path, output_path=output_folds_path)
