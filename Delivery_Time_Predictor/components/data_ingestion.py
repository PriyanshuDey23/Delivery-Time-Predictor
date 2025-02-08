from Delivery_Time_Predictor.constants import * 
from Delivery_Time_Predictor.config.configuration import  *
import os, sys
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from dataclasses import dataclass
from Delivery_Time_Predictor.logger import logging
from Delivery_Time_Predictor.exception import CustomException
from  Delivery_Time_Predictor.components.data_transformation import DataTransformation
from Delivery_Time_Predictor.components.model_trainer import ModelTrainer



@dataclass # creates some useful methods for the class (like the __init__ method to initialize the data).
class DataIngestionConfig:
    train_data_path:str = TRAIN_FILE_PATH # Folder so in string format
    test_data_path:str = TEST_FILE_PATH
    raw_data_path:str = RAW_FILE_PATH


class DataIngestion:
    def __init__(self):
        self.data_ingestion_config = DataIngestionConfig() # For calling the class


    def initiate_data_ingestion(self):
        try:
            df = pd.read_csv(DATASET_PATH) # Read the dataset

            os.makedirs(os.path.dirname(self.data_ingestion_config.raw_data_path), exist_ok=True) # Directory making

            df.to_csv(self.data_ingestion_config.raw_data_path, index = False) # Save the dataset

            # Split the data
            train_set, test_set = train_test_split(df, test_size = 0.20, random_state= 42)

            # Save the train file
            os.makedirs(os.path.dirname(self.data_ingestion_config.train_data_path),exist_ok=True )
            train_set.to_csv(self.data_ingestion_config.train_data_path, header = True)

            # Save the test file
            os.makedirs(os.path.dirname(self.data_ingestion_config.test_data_path),exist_ok=True )
            test_set.to_csv(self.data_ingestion_config.test_data_path, header = True)

            # Return 
            return(
                self.data_ingestion_config.train_data_path,
                self.data_ingestion_config.test_data_path

            )

        except Exception as e:
            raise CustomException( e, sys)
        


# Run Data Ingestion
# if __name__ == "__main__":
#     obj = DataIngestion()
#     train_data_path,test_data_path=obj.initiate_data_ingestion()


# Data Transformation
# if __name__ == "__main__":
#     obj = DataIngestion()
#     train_data_path,test_data_path=obj.initiate_data_ingestion()
#     data_transformation = DataTransformation()
#     train_arr,test_arr,_ = data_transformation.inititate_data_transformation(train_data_path,test_data_path)


# Model Training 
if __name__ == "__main__":
    obj = DataIngestion()
    train_data_path,test_data_path=obj.initiate_data_ingestion()
    data_transformation = DataTransformation()
    train_arr,test_arr,_ = data_transformation.inititate_data_transformation(train_data_path,test_data_path)
    model_trainer = ModelTrainer()
    print(model_trainer.initate_model_training(train_arr,test_arr))


