from sklearn import metrics as skmetrics


class ClassificationMetrics:
    """
    A utility class for computing various classification metrics.

    Usage:
    metrics_calculator = ClassificationMetrics()
    accuracy = metrics_calculator("accuracy", y_true, y_pred)
    f1 = metrics_calculator("f1", y_true, y_pred)
    precision = metrics_calculator("precision", y_true, y_pred)
    recall = metrics_calculator("recall", y_true, y_pred)
    auc = metrics_calculator("auc", y_true, y_proba)
    logloss = metrics_calculator("logloss", y_true, y_proba)
    """

    def __init__(self):
        """
        Initialize the ClassificationMetrics object with available metrics functions.
        """
        self.metrics = {
            "accuracy": self._accuracy,
            "f1": self._f1,
            "precision": self._precision,
            "recall": self._recall,
            "auc": self._auc,
            "logloss": self._logloss,
        }

    def __call__(self, metric, y_true, y_pred, y_proba=None):
        """
        Compute the specified classification metric.

        Parameters:
        - metric (str): The name of the metric to compute.
        - y_true (array-like): True labels.
        - y_pred (array-like): Predicted labels.
        - y_proba (array-like, optional): Predicted probabilities (required for auc and logloss).

        Returns:
        - float: The computed metric value.
        """
        if metric not in self.metrics:
            raise ValueError("Metric not implemented")

        if metric == "auc":
            if y_proba is not None:
                return self._auc(y_true=y_true, y_pred=y_proba)
            else:
                raise ValueError("y_proba cannot be None for AUC")
        elif metric == "logloss":
            if y_proba is not None:
                return self._logloss(y_true=y_true, y_pred=y_proba)
            else:
                raise ValueError("y_proba cannot be None for logloss")
        else:
            return self.metrics[metric](y_true=y_true, y_pred=y_pred)

    @staticmethod
    def _auc(y_true, y_pred):
        """
        Compute the Area Under the ROC Curve (AUC).

        Parameters:
        - y_true (array-like): True labels.
        - y_pred (array-like): Predicted probabilities.

        Returns:
        - float: AUC value.
        """
        return skmetrics.roc_auc_score(y_true=y_true, y_score=y_pred)

    @staticmethod
    def _accuracy(y_true, y_pred):
        """
        Compute accuracy.

        Parameters:
        - y_true (array-like): True labels.
        - y_pred (array-like): Predicted labels.

        Returns:
        - float: Accuracy value.
        """
        return skmetrics.accuracy_score(y_true=y_true, y_pred=y_pred)

    @staticmethod
    def _f1(y_true, y_pred):
        """
        Compute F1 score.

        Parameters:
        - y_true (array-like): True labels.
        - y_pred (array-like): Predicted labels.

        Returns:
        - float: F1 score value.
        """
        return skmetrics.f1_score(y_true=y_true, y_pred=y_pred)

    @staticmethod
    def _recall(y_true, y_pred):
        """
        Compute recall.

        Parameters:
        - y_true (array-like): True labels.
        - y_pred (array-like): Predicted labels.

        Returns:
        - float: Recall value.
        """
        return skmetrics.recall_score(y_true=y_true, y_pred=y_pred)

    @staticmethod
    def _precision(y_true, y_pred):
        """
        Compute precision.

        Parameters:
        - y_true (array-like): True labels.
        - y_pred (array-like): Predicted labels.

        Returns:
        - float: Precision value.
        """
        return skmetrics.precision_score(y_true=y_true, y_pred=y_pred)

    @staticmethod
    def _logloss(y_true, y_pred):
        """
        Compute log loss.

        Parameters:
        - y_true (array-like): True labels.
        - y_pred (array-like): Predicted probabilities.

        Returns:
        - float: Log loss value.
        """
        return skmetrics.log_loss(y_true=y_true, y_pred=y_pred)
