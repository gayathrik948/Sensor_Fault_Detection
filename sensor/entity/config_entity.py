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

@dataclass
class ModelTrainerConfig:
    def __init__(self):
        self.UTILS = MainUtils()
        self.MODEL_TRAINER_ARTIFACT_DIR:str = os.path.join(from_root(),
                                                           ARTIFACTS_DIR, MODEL_TRAINER_ARTIFACTS_DIR)
        self.TRAINED_MODEL_FILE_PATH:str = os.path.join(self.MODEL_TRAINER_ARTIFACT_DIR, MODEL_FILE_NAME)



@dataclass
class ModelEvaluationConfig:
    def __init__(self):
        self.S3_OPERATION = S3Operation()
        self.UTILS = MainUtils()
        self.S3_BUCKET_NAME:str = BUCKET_NAME


@dataclass
class ModelPusherConfig:
    def __init__(self):
        self.S3_BUCKET_NAME:str = BUCKET_NAME
        self.S3_MODEL_PATH:str = os.path.join(S3_MODEL_NAME)