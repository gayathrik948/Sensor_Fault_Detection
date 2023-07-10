from dataclasses import dataclass


@dataclass
class DataIngestionArtifacts:
    train_data_file_path:str
    test_data_file_path:str