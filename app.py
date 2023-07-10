from sensor.configuration.mongo_operations import MongoDBOperation
from sensor.pipeline.training_pipeline import TrainingPipeline
from sensor.constants import *
import pandas as pd


# if __name__ == "__main__":
#     mongo_op = MongoDBOperation()
#     df = pd.read_csv("dataset.csv")
#     mongo_op.insert_dataframe_as_record(df, DB_NAME, COLLECTION_NAME)


if __name__ == "__main__":
    pipeline = TrainingPipeline()
    pipeline.run_pipeline()