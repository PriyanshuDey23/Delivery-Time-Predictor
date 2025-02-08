import os, sys
from Delivery_Time_Predictor.constants import *
from Delivery_Time_Predictor.logger import logging
from Delivery_Time_Predictor.exception import CustomException
from Delivery_Time_Predictor.config.configuration import *
from dataclasses import dataclass
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import GradientBoostingRegressor
from sklearn.ensemble import RandomForestRegressor
from sklearn.svm import SVR
from sklearn.tree import DecisionTreeRegressor
from Delivery_Time_Predictor.utils import evaluate_model, save_obj


@dataclass 
class ModelTrainerConfig:
    trained_model_file_path = MODEL_FILE_PATH


class ModelTrainer:
    def __init__(self):
        self.model_trainer_config = ModelTrainerConfig()

    def initate_model_training(self,train_array,test_array):
        try:
            logging.info('Splitting Dependent and Independent variables from train and test data')
            # Split the data 
            X_train, y_train, X_test, y_test = (train_array[:,:-1], train_array[:,-1],
                                                test_array[:,:-1],test_array[:,-1])

            # Call the model
            models={
            'LinearRegression':LinearRegression(),
            'DecisionTree':DecisionTreeRegressor(),
            'Gradient Boosting':GradientBoostingRegressor(),
            'Random Forest':RandomForestRegressor(),
            'SVR':SVR()
            
        }
            
           
           
            model_report:dict=evaluate_model(X_train,y_train,X_test,y_test,models)
            print(model_report)
            print('\n====================================================================================\n')
            logging.info(f'Model Report : {model_report}')

            # To get best model score from dictionary (Sort)
            best_model_score = max(sorted(model_report.values()))

            # Get model name and sorted score
            best_model_name = list(model_report.keys())[
                list(model_report.values()).index(best_model_score)
            ]
            
            # Best model
            best_model = models[best_model_name]

            print(f'Best Model Found , Model Name : {best_model_name} , R2 Score : {best_model_score}')
            print('\n====================================================================================\n')
            logging.info(f'Best Model Found , Model Name : {best_model_name} , R2 Score : {best_model_score}')

            # Save the model
            save_obj(
                 file_path=self.model_trainer_config.trained_model_file_path,
                 obj=best_model
            )
          

        except Exception as e:
            logging.info('Exception occured at Model Training')
            raise CustomException(e,sys)


