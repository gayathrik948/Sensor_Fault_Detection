import sys
import pandas as pd
import numpy as np
from pandas import DataFrame
from sensor.exceptions import sensorException
from sensor.entity.config_entity import ModelTrainerConfig
from sensor.entity.artifacts_entity import (
    DataTransformationArtifacts,
    ModelTrainerArtifacts,
)
from typing import List, Tuple
from sensor.constants import *


class CostModel:
    def __init__(self, preprocessing_object: object, trained_model_object: object):
        self.preprocessing_object = preprocessing_object
        self.trained_model_object = trained_model_object

    def predict(self, X) -> float:
        try:
            transformed_feature = self.preprocessing_object.transform(X)
            return self.trained_model_object.predict(transformed_feature)
        except Exception as e:
            raise sensorException(e, sys) from e

    def __repr__(self):
        return f"{type(self.trained_model_object).__name__}()"

    def __str__(self):
        return f"{type(self.trained_model_object).__name__}()"


class ModelTrainer:
    def __init__(
        self,
        data_transformation_artifact: DataTransformationArtifacts,
        model_trainer_config: ModelTrainerConfig
    ):
        self.data_transformation_artifact = data_transformation_artifact
        self.model_trainer_config = model_trainer_config

    def get_trained_models(
        self, x_data: DataFrame, y_data: DataFrame
    ) -> List[Tuple[float, object, str]]:
        try:
            model_config = self.model_trainer_config.UTILS.read_yaml_file(
                filename=MODEL_CONFIG_FILE
            )
            models_list = list(model_config["train_model"].keys())
            x_train, y_train, x_test, y_test = (
                x_data.drop(x_data.columns[len(x_data.columns) - 1], axis=1),
                x_data.iloc[:, -1],
                y_data.drop(y_data.columns[len(y_data.columns) - 1], axis=1),
                y_data.iloc[:, -1],
            )
            tuned_model_list = [
                (
                    self.model_trainer_config.UTILS.get_tuned_model(
                        model_name, x_train, y_train, x_test, y_test
                    )
                )
                for model_name in models_list
            ]
            return tuned_model_list

        except Exception as e:
            raise sensorException(e, sys) from e


    def initiate_model_trainer(self) -> ModelTrainerArtifacts:
        try:
            os.makedirs(
                self.model_trainer_config.MODEL_TRAINER_ARTIFACT_DIR, exist_ok=True
            )
            train_array = self.model_trainer_config.UTILS.load_numpy_array_data(
                self.data_transformation_artifact.transformed_train_data_file_path
            )
            train_df = pd.DataFrame(train_array)
            test_array = self.model_trainer_config.UTILS.load_numpy_array_data(
                self.data_transformation_artifact.transformed_test_data_file_path
            )
            test_df = pd.DataFrame(test_array)
            list_of_trained_models = self.get_trained_models(train_df, test_df)
            (
                best_model,
                best_model_score,
            ) = self.model_trainer_config.UTILS.get_best_model_with_name_and_score(
                list_of_trained_models
            )
            preprocessor_obj_file_path = (
                self.data_transformation_artifact.preprocessor_object_file_path
            )
            preprocessing_obj = self.model_trainer_config.UTILS.load_object(
                preprocessor_obj_file_path
            )
            model_config = self.model_trainer_config.UTILS.read_yaml_file(
                filename=MODEL_CONFIG_FILE
            )
            base_model_score = float(model_config["base_model_score"])

            if best_model_score < base_model_score:
                raise Exception("Model is not good try to do more experimentation.")

            else:
                cost_model = CostModel(preprocessing_obj, best_model)
                trained_model_path = self.model_trainer_config.TRAINED_MODEL_FILE_PATH
                model_file_path = self.model_trainer_config.UTILS.save_object(
                    trained_model_path, cost_model
                )


            model_trainer_artifacts = ModelTrainerArtifacts(
                trained_model_file_path=model_file_path
            )

            return model_trainer_artifacts

        except Exception as e:
            raise sensorException(e, sys) from e
