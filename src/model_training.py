import os
import joblib
import numpy as np
import time
import warnings
from datetime import datetime

from tqdm import tqdm

from sklearn.model_selection import RandomizedSearchCV, train_test_split
from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    roc_auc_score,
    roc_curve
)

from src.logger import get_logger
from src.exceptions import CustomException
from utils.common_functions import load_data

from config.model_params import MODEL_REGISTRY, RANDOM_SEARCH_PARAMS
from config.paths_config import (
    PROCESSED_TRAIN_DATA_PATH,
    PROCESSED_TEST_DATA_PATH,
    MODEL_OUTPUT_PATH
)

import mlflow
import mlflow.sklearn

warnings.filterwarnings("ignore")

logger = get_logger(__name__)

class ModelTrainer:

    def __init__(self, train_path, test_path, model_output_path):
        self.train_path = train_path
        self.test_path = test_path
        self.model_output_path = model_output_path
        self.models = MODEL_REGISTRY
        self.param_distributions = RANDOM_SEARCH_PARAMS

    def load_and_split_data(self):
        try:
            train_df = load_data(self.train_path)
            test_df = load_data(self.test_path)

            label_map = {"Canceled": 0, "Not_Canceled": 1}

            train_df["booking_status"] = train_df["booking_status"].map(label_map)
            test_df["booking_status"] = test_df["booking_status"].map(label_map)

            X_train = train_df.drop(columns=["booking_status"])
            y_train = train_df["booking_status"].astype(int)

            X_test = test_df.drop(columns=["booking_status"])
            y_test = test_df["booking_status"].astype(int)

            return X_train, X_test, y_train, y_test

        except Exception as e:
            logger.error(f"Error loading data: {e}")
            raise CustomException("Failed to load data")

    def _optimal_threshold(self, y_true, y_proba):
        try:
            if len(np.unique(y_true)) < 2:
                return 0.5
            fpr, tpr, thresholds = roc_curve(y_true, y_proba)
            return thresholds[np.argmax(tpr - fpr)]
        except Exception:
            return 0.5

    def train_and_evaluate(self):
        try:
            X_train, X_test, y_train, y_test = self.load_and_split_data()

            X_tr, X_val, y_tr, y_val = train_test_split(
                X_train,
                y_train,
                test_size=0.2,
                stratify=y_train,
                random_state=42
            )

            best_model = None
            best_score = -1.0
            best_model_name = None
            best_threshold = 0.5

            metrics_summary = {}

            for model_name, model in tqdm(self.models.items(), desc="Training models"):
                start_time = time.perf_counter()

                param_dist = dict(self.param_distributions[model_name])
                n_iter = param_dist.pop("n_iter", 25)

                search = RandomizedSearchCV(
                    estimator=model,
                    param_distributions=param_dist,
                    n_iter=n_iter,
                    scoring="roc_auc",
                    cv=5,
                    n_jobs=-1,
                    random_state=42,
                    verbose=0
                )

                fit_params = {}

                if model_name == "XGBoost":
                    fit_params = {}
                elif model_name == "LightGBM":
                    fit_params = {
                        "eval_set": [(X_val, y_val)],
                        "eval_metric": "auc"
                    }
                

                search.fit(X_tr, y_tr, **fit_params)

                best_estimator = search.best_estimator_
                cv_score = search.best_score_

                if hasattr(best_estimator, "predict_proba"):
                    y_proba = best_estimator.predict_proba(X_test)[:, 1]
                elif hasattr(best_estimator, "decision_function"):
                    scores = best_estimator.decision_function(X_test)
                    y_proba = (scores - scores.min()) / (scores.max() - scores.min() + 1e-8)
                else:
                    logger.warning(f"{model_name} skipped: no probability output")
                    continue

                threshold = self._optimal_threshold(y_test, y_proba)
                y_pred = (y_proba >= threshold).astype(int)

                roc_auc = roc_auc_score(y_test, y_proba)

                elapsed = time.perf_counter() - start_time

                metrics_summary[model_name] = {
                    "cv_roc_auc": cv_score,
                    "test_roc_auc": roc_auc,
                    "accuracy": accuracy_score(y_test, y_pred),
                    "precision": precision_score(y_test, y_pred),
                    "recall": recall_score(y_test, y_pred),
                    "f1_score": f1_score(y_test, y_pred),
                    "threshold": threshold,
                    "training_time_sec": round(elapsed, 2),
                    "best_params": search.best_params_
                }

                logger.info(
                    f"{model_name} | "
                    f"CV ROC-AUC={cv_score:.4f} | "
                    f"Test ROC-AUC={roc_auc:.4f} | "
                    f"Time={elapsed:.2f}s"
                )

                if roc_auc > best_score:
                    best_score = roc_auc
                    best_model = best_estimator
                    best_model_name = model_name
                    best_threshold = threshold

            artifact = {
                "model": best_model,
                "model_name": best_model_name,
                "best_score": best_score,
                "threshold": best_threshold,
                "metrics": metrics_summary,
                "features": X_train.columns.tolist(),
                "trained_at": datetime.utcnow().isoformat()
            }

            os.makedirs(os.path.dirname(self.model_output_path), exist_ok=True)
            joblib.dump(artifact, self.model_output_path)

            logger.info(f"Best model selected: {best_model_name} | ROC-AUC={best_score:.4f}")

            return artifact

        except Exception as e:
            logger.error(f"Error during model training: {e}")
            raise CustomException("Training failed")

    def run(self):
        try:
            mlflow.set_experiment("hotel_booking_cancellation_ml_pipeline")

            with mlflow.start_run(run_name="model_training_pipeline"):
                logger.info("Model training pipeline started")
                logger.info("MLflow experiment started")

                mlflow.set_tag("pipeline", "model_training")
                mlflow.set_tag("problem_type", "binary_classification")
                mlflow.set_tag("target", "booking_status")

                logger.info("Logging training and testing datasets to MLflow")
                mlflow.log_artifact(self.train_path, artifact_path="datasets")
                mlflow.log_artifact(self.test_path, artifact_path="datasets")

                artifact = self.train_and_evaluate()

                metrics = artifact["metrics"]
                best_model_name = artifact["model_name"]
                best_metrics = metrics[best_model_name]

                logger.info("--------------------------------------------------")
                logger.info("MODEL SELECTION SUMMARY")
                logger.info(f"Best Algorithm        : {best_model_name}")
                logger.info("Selection Criterion   : Highest Test ROC-AUC")
                logger.info(f"CV ROC-AUC            : {best_metrics['cv_roc_auc']:.4f}")
                logger.info(f"Test ROC-AUC          : {best_metrics['test_roc_auc']:.4f}")
                logger.info(f"Accuracy              : {best_metrics['accuracy']:.4f}")
                logger.info(f"Precision             : {best_metrics['precision']:.4f}")
                logger.info(f"Recall                : {best_metrics['recall']:.4f}")
                logger.info(f"F1-score              : {best_metrics['f1_score']:.4f}")
                logger.info(f"Optimal Threshold     : {best_metrics['threshold']:.4f}")
                logger.info("--------------------------------------------------")

                logger.info("Best model hyperparameters")
                for param_name, param_value in best_metrics["best_params"].items():
                    logger.info(f"{best_model_name} | {param_name} = {param_value}")

                logger.info("Logging per-model metrics and parameters to MLflow")

                for model_name, model_metrics in metrics.items():
                    prefix = model_name.lower()

                    mlflow.log_metric(f"{prefix}_cv_roc_auc", model_metrics["cv_roc_auc"])
                    mlflow.log_metric(f"{prefix}_test_roc_auc", model_metrics["test_roc_auc"])
                    mlflow.log_metric(f"{prefix}_accuracy", model_metrics["accuracy"])
                    mlflow.log_metric(f"{prefix}_precision", model_metrics["precision"])
                    mlflow.log_metric(f"{prefix}_recall", model_metrics["recall"])
                    mlflow.log_metric(f"{prefix}_f1_score", model_metrics["f1_score"])
                    mlflow.log_metric(f"{prefix}_threshold", model_metrics["threshold"])
                    mlflow.log_metric(
                        f"{prefix}_training_time_sec",
                        model_metrics["training_time_sec"]
                    )

                    for param_name, param_value in model_metrics["best_params"].items():
                        mlflow.log_param(f"{prefix}_{param_name}", param_value)

                mlflow.set_tag("best_model", best_model_name)
                mlflow.set_tag(
                    "model_selection_reason",
                    f"{best_model_name} achieved highest test ROC-AUC ({best_metrics['test_roc_auc']:.4f})"
                )

                logger.info("Logging best model metrics explicitly to MLflow")
                mlflow.log_metric("best_cv_roc_auc", best_metrics["cv_roc_auc"])
                mlflow.log_metric("best_test_roc_auc", best_metrics["test_roc_auc"])
                mlflow.log_metric("best_accuracy", best_metrics["accuracy"])
                mlflow.log_metric("best_precision", best_metrics["precision"])
                mlflow.log_metric("best_recall", best_metrics["recall"])
                mlflow.log_metric("best_f1_score", best_metrics["f1_score"])
                mlflow.log_metric("best_threshold", best_metrics["threshold"])

                logger.info("Logging feature list used for training")
                feature_file = "features.txt"
                with open(feature_file, "w") as f:
                    for col in artifact["features"]:
                        f.write(f"{col}\n")

                mlflow.log_artifact(feature_file, artifact_path="metadata")
                os.remove(feature_file)

                logger.info(
                    f"Persisting trained model | "
                    f"Algorithm={best_model_name} | "
                    f"Test ROC-AUC={best_metrics['test_roc_auc']:.4f}"
                )

                mlflow.sklearn.log_model(
                    sk_model=artifact["model"],
                    artifact_path="model",
                    registered_model_name="hotel_booking_cancellation_model"
                )

                logger.info(
                    "Model successfully stored and registered in MLflow | "
                    f"Registered Name=hotel_booking_cancellation_model | "
                    f"Algorithm={best_model_name}"
                )

                logger.info("Model training pipeline finished successfully")
                return artifact

        except Exception as e:
            logger.error(f"Pipeline execution failed: {e}")
            raise CustomException("Pipeline failed")

if __name__ == "__main__":
    trainer = ModelTrainer(
        PROCESSED_TRAIN_DATA_PATH,
        PROCESSED_TEST_DATA_PATH,
        MODEL_OUTPUT_PATH
    )
    trainer.run()
