from dataclasses import dataclass
from from_root import from_root
import os
from sensor.configuration.s3_operations import S3Operation
from sensor.utils.main_utils import MainUtils
from sensor.constants import *


@dataclass
class DataIngestionConfig:
    def __init__(self):
        self.UTILS = MainUtils()
        self.SCHEMA_CONFIG = self.UTILS.read_yaml_file(filename=SCHEMA_FILE_PATH)
        self.DB_NAMES = DB_NAME
        self.COLLECTION_NAMES = COLLECTION_NAME
        self.DATA_INGESTION_ARTIFACT_DIR:str = os.path.join(from_root(),
                                                       ARTIFACTS_DIR, DATA_INGESTION_ARTIFACTS_DIR)
        self.DATA_INGESTION_TRAIN_ARTIFACT_DIR:str = os.path.join(self.DATA_INGESTION_ARTIFACT_DIR,
                                                                  DATA_INGESTION_TRAIN_DIR)
        self.DATA_INGESTION_TEST_ARTIFACT_DIR:str = os.path.join(self.DATA_INGESTION_ARTIFACT_DIR,
                                                                 DATA_INGESTION_TEST_DIR)
        self.DATA_INGESTION_TRAIN_ARTIFACT_FILE_NAME:str = os.path.join(self.DATA_INGESTION_TRAIN_ARTIFACT_DIR,
                                                                        DATA_INGESTION_TRAIN_FILE_NAME)
        self.DATA_INGESTION_TEST_ARTIFACT_FILE_NAME: str = os.path.join(self.DATA_INGESTION_TEST_ARTIFACT_DIR,
                                                                        DATA_INGESTION_TEST_FILE_NAME)

@dataclass
class DataTransformationConfig:
    def __init__(self):
        self.UTILS = MainUtils()
        self.SCHEMA_CONFIG = self.UTILS.read_yaml_file(SCHEMA_FILE_PATH)
        self.DATA_TRANSFORMATION_ARTIFACT_DIR = os.path.join(from_root(), ARTIFACTS_DIR,
                                                             DATA_TRANSFORMATION_ARTIFCATS_DIR)
        self.TRANSFORMED_TRAIN_ARTIFACT_DATA_DIR = os.path.join(self.DATA_TRANSFORMATION_ARTIFACT_DIR,
                                                                TRANSFORMED_TRAIN_DATA_DIR)
        self.TRANSFORMED_TEST_ARTIFACT_DATA_DIR = os.path.join(self.DATA_TRANSFORMATION_ARTIFACT_DIR,
                                                               TRANSFORMED_TEST_DATA_DIR)
        self.TRANSFORMED_TRAIN_ARTIFACT_DATA_FILE_NAME = os.path.join(self.TRANSFORMED_TRAIN_ARTIFACT_DATA_DIR,
                                                                      TRANSFORMED_TRAIN_DATA_FILE_NAME)
        self.TRANSFORMED_TEST_ARTIFACT_DATA_FILE_NAME = os.path.join(self.TRANSFORMED_TEST_ARTIFACT_DATA_DIR,
                                                                     TRANSFORMED_TEST_DATA_FILE_NAME)
        self.PREPROCESSOR_OBJECT_ARTIFACT_FILE_NAME = os.path.join(self.DATA_TRANSFORMATION_ARTIFACT_DIR,
                                                                   PREPROCESSOR_OBJECT_FILE_NAME)