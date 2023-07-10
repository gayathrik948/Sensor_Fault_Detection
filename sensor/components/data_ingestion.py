
from typing import Tuple
from sensor.configuration.mongo_operations import MongoDBOperation
from sensor.entity.config_entity import DataIngestionConfig
from sensor.entity.artifacts_entity import DataIngestionArtifacts
from sensor.exceptions import sensorException
from pandas import DataFrame
import sys
from sensor.constants import *
from sklearn.model_selection import train_test_split


class DataIngestion:
    def __init__(self, data_ingestion_config:DataIngestionConfig,
                 mongo_op:MongoDBOperation):
        self.data_ingestion_config=data_ingestion_config
        self.mongo_op=mongo_op


    def get_data_from_mongodb(self)->DataFrame:
        try:
            df = self.mongo_op.get_collection_as_dataframe(
                self.data_ingestion_config.DB_NAMES,
                self.data_ingestion_config.COLLECTION_NAMES
            )
            return df
        except Exception as e:
            raise sensorException(e,sys)

    def split_data_as_train_test(self, df:DataFrame)->Tuple[DataFrame, DataFrame]:
        try:
            os.makedirs(self.data_ingestion_config.DATA_INGESTION_ARTIFACT_DIR, exist_ok=True)
            train_set, test_set = train_test_split(df, test_size=TEST_SIZE)
            os.makedirs(self.data_ingestion_config.DATA_INGESTION_TRAIN_ARTIFACT_DIR, exist_ok=True)
            os.makedirs(self.data_ingestion_config.DATA_INGESTION_TEST_ARTIFACT_DIR, exist_ok=True)
            train_set.to_csv(self.data_ingestion_config.DATA_INGESTION_TRAIN_ARTIFACT_FILE_NAME,
                             index=False, header=True)
            test_set.to_csv(self.data_ingestion_config.DATA_INGESTION_TEST_ARTIFACT_FILE_NAME,
                            index=False, header=True)
            return train_set, test_set
        except Exception as e:
            raise sensorException(e,sys)


    def initiate_data_ingestion(self)->DataIngestionArtifacts:
        try:
            df = self.get_data_from_mongodb()
            df1 = df.dropna()
            self.split_data_as_train_test(df1)
            data_ingestion_artifacts = DataIngestionArtifacts(
                train_data_file_path=self.data_ingestion_config.DATA_INGESTION_TRAIN_ARTIFACT_FILE_NAME,
                test_data_file_path=self.data_ingestion_config.DATA_INGESTION_TEST_ARTIFACT_FILE_NAME
            )
            return data_ingestion_artifacts
        except Exception as e:
            raise sensorException(e,sys)