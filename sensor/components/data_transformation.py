import os
from sensor.entity.artifacts_entity import (DataIngestionArtifacts, DataTransformationArtifacts)
from sensor.entity.config_entity import DataTransformationConfig
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import RobustScaler
from sklearn.pipeline import Pipeline
from sensor.components.output_encoders import TargetValueMapping
from imblearn.combine import SMOTETomek
import pandas as pd
from pandas import DataFrame
import numpy as np
import sys
from sensor.exceptions import sensorException


class DataTransformation:
    def __init__(self,
                 data_ingestion_artifacts: DataIngestionArtifacts,
                 data_transformation_config: DataTransformationConfig):
        self.data_ingestion_artifacts = data_ingestion_artifacts
        self.data_transformation_config = data_transformation_config

        self.train_set = pd.read_csv(self.data_ingestion_artifacts.train_data_file_path)
        self.test_set = pd.read_csv(self.data_ingestion_artifacts.test_data_file_path)

    def get_data_transformer_object(cls) -> Pipeline:
        try:
            robust_scaler = RobustScaler()
            simple_imputer = SimpleImputer(strategy="constant", fill_value=0)
            preprocessor = Pipeline(
                steps=[
                    ("Imputer", simple_imputer),  # replace missing values with zero
                    ("RobustScaler", robust_scaler)  # keep every feature in same range and handle outlier
                ]
            )
            return preprocessor
        except Exception as e:
            raise sensorException(e, sys)

    #
    @staticmethod
    def outlier_capping(col, df:DataFrame)->DataFrame:
        try:
            df[col] = pd.to_numeric(df[col], errors='coerce')
            percentile25 = df[col].quantile(0.25)
            percentile75 = df[col].quantile(0.75)
            iqr = percentile75-percentile25
            upper_limit = percentile75+1.5 * iqr
            lower_limit = percentile25-1.5 * iqr
            df.loc[(df[col] > upper_limit), col]=upper_limit
            df.loc[(df[col] < lower_limit), col]=lower_limit
            return df
        except Exception as e:
            raise sensorException(e, sys)


    def initiate_data_transformation(self)->DataTransformationArtifacts:
        try:
            os.makedirs(self.data_transformation_config.DATA_TRANSFORMATION_ARTIFACT_DIR, exist_ok=True)
            preprocessor = self.get_data_transformer_object()

            self.train_set = self.train_set.replace('na', np.nan)
            self.test_set = self.test_set.replace('na', np.nan)

            numerical_columns = self.data_transformation_config.SCHEMA_CONFIG["numerical_columns"]
            continious_columnns = [feature for feature in numerical_columns if len(self.train_set[feature].unique())>=25]
            [self.outlier_capping(col, self.train_set) for col in continious_columnns]
            [self.outlier_capping(col, self.test_set) for col in continious_columnns]

            input_feature_train_df = self.train_set.iloc[:, :-1]
            target_feature_train_df = self.train_set.iloc[:, -1]
            target_feature_train_df = target_feature_train_df.replace(TargetValueMapping().to_dict())

            input_feature_test_df = self.test_set.iloc[:, :-1]
            target_feature_test_df = self.test_set.iloc[:, -1]
            target_feature_test_df = target_feature_test_df.replace(TargetValueMapping().to_dict())

            input_feature_train_arr = preprocessor.fit_transform(input_feature_train_df)
            smt = SMOTETomek(sampling_strategy="minority")
            input_feature_train_final, target_feature_train_final = smt.fit_resample(
                input_feature_train_arr, target_feature_train_df
            )
            train_arr = np.c_[input_feature_train_final, np.array(target_feature_train_final)]
            os.makedirs(self.data_transformation_config.TRANSFORMED_TRAIN_ARTIFACT_DATA_DIR, exist_ok=True)
            transformed_train_file = self.data_transformation_config.UTILS.save_numpy_array_data(
                self.data_transformation_config.TRANSFORMED_TRAIN_ARTIFACT_DATA_FILE_NAME, train_arr
            )

            input_feature_test_arr = preprocessor.transform(input_feature_test_df)
            input_feature_test_final, target_feature_test_final = smt.fit_resample(
                input_feature_test_arr, target_feature_test_df
            )
            test_arr = np.c_[input_feature_test_final, np.array(target_feature_test_final)]
            os.makedirs(self.data_transformation_config.TRANSFORMED_TEST_ARTIFACT_DATA_DIR, exist_ok=True)
            transformed_test_file = self.data_transformation_config.UTILS.save_numpy_array_data(
                self.data_transformation_config.TRANSFORMED_TEST_ARTIFACT_DATA_FILE_NAME, test_arr
            )
            preprocessor_file = self.data_transformation_config.UTILS.save_object(
                self.data_transformation_config.PREPROCESSOR_OBJECT_ARTIFACT_FILE_NAME, preprocessor)
            data_transformation_artifacts = DataTransformationArtifacts(
                preprocessor_object_file_path=preprocessor_file,
                transformed_train_data_file_path=transformed_train_file,
                transformed_test_data_file_path=transformed_test_file
            )
            return data_transformation_artifacts
        except Exception as e:
            raise sensorException(e, sys)


