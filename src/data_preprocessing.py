import os
import pandas as pd
import numpy as np
from src.logger import get_logger
from src.exceptions import CustomException
from config.paths_config import (
    TRAIN_FILE_PATH,
    TEST_FILE_PATH,
    PROCESSED_TRAIN_DATA_PATH,
    PROCESSED_TEST_DATA_PATH,
    CONFIG_PATH,
    PROCESSED_DIR
)
from utils.common_functions import read_yaml, load_data
from sklearn.preprocessing import LabelEncoder
from imblearn.over_sampling import SMOTE
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier

logger = get_logger(__name__)

class DataProcessor:
    def __init__(self, train_path, test_path, processed_dir, config_path):
        self.train_path = train_path
        self.test_path = test_path
        self.processed_dir = processed_dir
        self.config = read_yaml(config_path)
        os.makedirs(self.processed_dir, exist_ok=True)

    def preporocess_data(self, df):
        try:
            logger.info("Starting data processing step")

            if "Booking_ID" in df.columns:
                df.drop(columns=["Booking_ID"], inplace=True)

            df.drop_duplicates(inplace=True)

            cat_cols = self.config["data_preprocessing"]["categorical_columns"]
            num_cols = self.config["data_preprocessing"]["numerical_columns"]

            le = LabelEncoder()

            for col in cat_cols:
                df[col] = le.fit_transform(df[col])

            skew_threshold = self.config["data_preprocessing"]["skewness_threshold"]

            skewed_cols = df[num_cols].skew().abs()
            skewed_cols = skewed_cols[skewed_cols > skew_threshold].index.tolist()

            for col in skewed_cols:
                df[col] = np.log1p(df[col])

            return df

        except Exception as e:
            logger.error(f"Error during preprocessing: {e}")
            raise CustomException("Data preprocessing failed")

    def balance_data(self, df):
        try:
            X = df.drop(columns="booking_status")
            y = df["booking_status"]

            X_resampled, y_resampled = SMOTE(random_state=42).fit_resample(X, y)

            balanced_df = pd.DataFrame(X_resampled, columns=X.columns)
            balanced_df["booking_status"] = y_resampled

            return balanced_df

        except Exception as e:
            logger.error(f"Error during balancing data: {e}")
            raise CustomException("Data balancing failed")

    def select_features(self, balanced_df):
        try:
            X = balanced_df.drop(columns="booking_status")
            y = balanced_df["booking_status"]

            X_train, _, y_train, _ = train_test_split(
                X,
                y,
                test_size=0.2,
                stratify=y,
                random_state=42
            )

            model = RandomForestClassifier(
                n_estimators=300,
                max_depth=None,
                random_state=42,
                class_weight="balanced",
                n_jobs=-1
            )

            model.fit(X_train, y_train)

            feature_importance_df = pd.DataFrame({
                "Feature": X.columns,
                "Importance": model.feature_importances_
            }).sort_values(by="Importance", ascending=False)

            num_features = self.config["data_preprocessing"]["no_of_features"]
            selected_features = feature_importance_df.head(num_features)["Feature"].tolist()

            return balanced_df[selected_features + ["booking_status"]]

        except Exception as e:
            logger.error(f"Error during feature selection: {e}")
            raise CustomException("Feature selection failed")

    def process_and_save(self, df, file_path):
        try:
            df.to_csv(file_path, index=False)

        except Exception as e:
            logger.error(f"Error saving processed data: {e}")
            raise CustomException("Saving processed data failed")

    def run(self):
        try:
            train_df = load_data(self.train_path)
            test_df = load_data(self.test_path)

            train_df = self.preporocess_data(train_df)
            test_df = self.preporocess_data(test_df)

            train_df = self.balance_data(train_df)

            train_df = self.select_features(train_df)

            test_df = test_df[train_df.columns]

            self.process_and_save(train_df, PROCESSED_TRAIN_DATA_PATH)
            self.process_and_save(test_df, PROCESSED_TEST_DATA_PATH)

            logger.info("Data processing pipeline completed successfully")

        except Exception as e:
            logger.error(f"Error in data processing pipeline: {e}")
            raise CustomException("Data processing pipeline failed")

        

if __name__ == "__main__":
    processor = DataProcessor(TRAIN_FILE_PATH, TEST_FILE_PATH,PROCESSED_DIR,CONFIG_PATH)
    processor.run()