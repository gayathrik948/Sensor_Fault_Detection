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