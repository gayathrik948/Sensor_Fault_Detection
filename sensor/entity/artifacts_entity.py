from dataclasses import dataclass


@dataclass
class DataIngestionArtifacts:
    train_data_file_path:str
    test_data_file_path:str


@dataclass
class DataTransformationArtifacts:
    transformed_train_data_file_path:str
    transformed_test_data_file_path:str
    preprocessor_object_file_path:str


@dataclass
class ModelTrainerArtifacts:
    trained_model_file_path: str

@dataclass
class ModelEvaluationArtifacts:
    is_model_accepted: bool
    trained_model_path: str
    changed_accuracy: float


@dataclass
class ModelPusherArtifacts:
    s3_bucket_name:str
    s3_model_path:str