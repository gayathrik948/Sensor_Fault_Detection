from sensor.components.data_ingestion import DataIngestion
from sensor.components.data_transformation import DataTransformation
from sensor.entity.artifacts_entity import (DataIngestionArtifacts, DataTransformationArtifacts)
from sensor.entity.config_entity import (DataIngestionConfig, DataTransformationConfig)
from sensor.configuration.mongo_operations import MongoDBOperation
from sensor.configuration.s3_operations import S3Operation
from sensor.exceptions import sensorException
import sys

class TrainingPipeline:
    def __init__(self):
        self.data_ingestion_config = DataIngestionConfig()
        self.data_transformation_config = DataTransformationConfig()
        self.mongo_op = MongoDBOperation()

    def start_data_ingestion(self) -> DataIngestionArtifacts:
        try:
            data_ingestion = DataIngestion(data_ingestion_config=self.data_ingestion_config,
                                           mongo_op=self.mongo_op)
            data_ingestion_artifact = data_ingestion.initiate_data_ingestion()
            return data_ingestion_artifact
        except Exception as e:
            raise sensorException(e, sys)

    def start_data_transformation(self, data_ingestion_artifact:DataIngestionArtifacts)->DataTransformationArtifacts:
        try:
            data_transformation = DataTransformation(data_ingestion_artifacts=data_ingestion_artifact,
                                                     data_transformation_config=self.data_transformation_config)
            data_transformation_artifact = data_transformation.initiate_data_transformation()
            return data_transformation_artifact
        except Exception as e:
            raise sensorException(e, sys)

    def run_pipeline(self):
        try:
            data_ingestion_artifact = self.start_data_ingestion()
            data_transformation_artifacts = self.start_data_transformation(
                data_ingestion_artifact=data_ingestion_artifact)
        except Exception as e:
            raise sensorException(e, sys)