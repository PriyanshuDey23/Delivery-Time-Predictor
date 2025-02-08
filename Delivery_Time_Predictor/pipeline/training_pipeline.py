from Delivery_Time_Predictor.constants import *
from Delivery_Time_Predictor.logger import logging
from Delivery_Time_Predictor.exception import CustomException
import os, sys
from Delivery_Time_Predictor.config.configuration import *
from Delivery_Time_Predictor.components.data_transformation import DataTransformation
from Delivery_Time_Predictor.components.model_trainer import ModelTrainer
from Delivery_Time_Predictor.components.data_ingestion import DataIngestion


class Train:
    def __init__(self):
        self.c = 0  ## Initialize an instance variable 'c' with the value 0
        print(f"-----------{self.c}------------")

    def main(self):
        try:
            logging.info("Starting Data Ingestion...")
            # Step 1: Data Ingestion
            data_ingestion = DataIngestion()
            train_data_path, test_data_path = data_ingestion.initiate_data_ingestion()
            logging.info(f"Data Ingestion complete. Train Data: {train_data_path}, Test Data: {test_data_path}")

            logging.info("Starting Data Transformation...")
            # Step 2: Data Transformation
            data_transformation = DataTransformation()
            train_arr, test_arr, _ = data_transformation.initiate_data_transformation(train_data_path, test_data_path)
            logging.info(f"Data Transformation complete. Train Shape: {train_arr.shape}, Test Shape: {test_arr.shape}")

            logging.info("Starting Model Training...")
            # Step 3: Model Training
            model_trainer = ModelTrainer()
            model_output = model_trainer.initate_model_training(train_arr, test_arr)
            logging.info(f"Model Training complete. Output: {model_output}")

        except CustomException as e:
            logging.error(f"Custom Exception occurred: {str(e)}")
            raise e
        except Exception as e:
            logging.error(f"Unexpected error occurred: {str(e)}")
            print(f"Unexpected error occurred: {str(e)}")  # For better debugging output
            raise e
