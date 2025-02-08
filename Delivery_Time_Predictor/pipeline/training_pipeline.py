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
# if __name__=='__main__':
        obj = DataIngestion()
        train_data_path,test_data_path=obj.initiate_data_ingestion()
        data_transformation = DataTransformation()
        train_arr,test_arr,_ = data_transformation.inititate_data_transformation(train_data_path,test_data_path)
        model_trainer = ModelTrainer()
        print(model_trainer.initate_model_training(train_arr,test_arr))