import os
import sys
import pandas as pd
from google.cloud import storage
from sklearn.model_selection import train_test_split

from src.logger import get_logger
from src.exceptions import CustomException
from utils.common_functions import read_yaml
from config.paths_config import RAW_DIR, RAW_FILE_PATH, TRAIN_FILE_PATH, TEST_FILE_PATH, CONFIG_PATH

logger = get_logger(__name__)


class DataIngestion:
    def __init__(self, config):
        self.config = config["data_ingestion"]
        self.bucket_name = self.config["bucket_name"]
        self.file_name = self.config["bucket_file_name"]
        self.train_test_ratio = self.config["train_ratio"]

        os.makedirs(RAW_DIR, exist_ok=True)
        os.makedirs(os.path.dirname(TRAIN_FILE_PATH), exist_ok=True)
        os.makedirs(os.path.dirname(TEST_FILE_PATH), exist_ok=True)

        logger.info(
            f"Data Ingestion initialized with bucket={self.bucket_name}, file={self.file_name}"
        )

    def download_csv_from_gcp(self):
        try:
            client = storage.Client()
            bucket = client.bucket(self.bucket_name)
            blob = bucket.blob(self.file_name)
            blob.download_to_filename(RAW_FILE_PATH)

            logger.info(
                f"File {self.file_name} downloaded from GCP bucket "
                f"{self.bucket_name} to {RAW_FILE_PATH}"
            )

        except Exception as e:
            logger.error("Error in downloading file from GCP")
            raise CustomException("Failed to download file from GCP", sys) from e

    def split_data(self):
        try:
            logger.info("Starting the data splitting process")

            df = pd.read_csv(RAW_FILE_PATH)
            train_data, test_data = train_test_split(
                df,
                train_size=1 - self.train_test_ratio,
                random_state=42,
            )

            train_data.to_csv(TRAIN_FILE_PATH, index=False)
            test_data.to_csv(TEST_FILE_PATH, index=False)

            logger.info(
                f"Data split completed. Train: {TRAIN_FILE_PATH}, Test: {TEST_FILE_PATH}"
            )

        except Exception as e:
            logger.error("Error in splitting data")
            raise CustomException("Failed to split data", sys) from e
        
    def run(self):
        try:
            logger.info("Data Ingestion process started")
            self.download_csv_from_gcp()
            self.split_data()

            logger.info("Data Ingestion process completed successfully")


        except Exception as e:
            logger.error("Error in Data Ingestion process")
            raise CustomException("Data Ingestion process failed", sys) from e

        finally:
            logger.info("Data Ingestion process finished")


if __name__ == "__main__":
    data_ingestion = DataIngestion(read_yaml(CONFIG_PATH))
    data_ingestion.run()