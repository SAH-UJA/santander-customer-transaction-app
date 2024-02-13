"""
prediction_module.py

This module provides a Singleton class for loading a prediction model
and performing inferences on Pandas DataFrames.
"""

import pandas as pd
import numpy as np
import logging
import joblib
import lightgbm


class SingletonMeta(type):
    """
    SingletonMeta is a metaclass for creating singleton instances of a class.
    It ensures that only one instance of the class is created.
    """

    _instances = {}

    def __call__(cls, *args, **kwargs):
        model_path = kwargs.get("model_path", "default")
        if (
            cls not in cls._instances
            or cls._instances[cls].get("model_path") != model_path
        ):
            instance = super().__call__(*args, **kwargs)
            cls._instances[cls] = {"instance": instance, "model_path": model_path}
        return cls._instances[cls]["instance"]


class PredictionModel(metaclass=SingletonMeta):
    """
    PredictionModel is a Singleton class for loading a prediction model and
    performing inferences on Pandas DataFrames.
    """

    def __init__(self, model_path=None):
        """
        Initializes the PredictionModel instance.

        Parameters:
        - model_path (str): Path to the saved model file.
        """
        try:
            with open(model_path, "rb") as file:
                self._model = joblib.load(file)
        except Exception as e:
            logging.error(f"Failed to load model: {e}")
            raise e

    def perform_inference(self, df: pd.DataFrame):
        """
        Performs inference on the given DataFrame using the loaded model.

        Parameters:
        - df (pd.DataFrame): DataFrame with input features for inference.

        Returns:
        - pd.DataFrame: DataFrame with 'ID_code' and 'target_pred' columns.
        """
        # Assuming there are 200 features labeled as 'var_0', 'var_1', ..., 'var_199'
        feature_columns = [f"var_{_}" for _ in range(200)]

        pred = self._model.predict(df[feature_columns])
        target_pred = pd.Series(np.where(pred >= 0.5, 1, 0), name="target_pred")

        result_df = pd.concat([df["ID_code"], target_pred], axis=1)
        return result_df
