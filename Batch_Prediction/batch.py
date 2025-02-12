# here we will just upload the data and, than we will get the prediction of that data


from Delivery_Time_Predictor.constants import *
from Delivery_Time_Predictor.config.configuration import *
import os, sys
import pandas as pd
import numpy as np
from Delivery_Time_Predictor.logger import logging
from Delivery_Time_Predictor.exception import CustomException
import pickle
from Delivery_Time_Predictor.utils import load_model
from sklearn.pipeline import Pipeline

PREDICTION_FOLDER='Batch_Prediction' # Folder 
PREDICTION_CSV='prediction_csv' # File
PREDICTION_FILE='output.csv' # Output

FEATURE_ENG_FOLDER='Feature_eng' #Folder

ROOT_DIR=os.getcwd() # Find current working directory
FEATURE_ENG=os.path.join(ROOT_DIR,PREDICTION_FOLDER,FEATURE_ENG_FOLDER)
BATCH_PREDICTION=os.path.join(ROOT_DIR,PREDICTION_FOLDER,PREDICTION_CSV)


class batch_prediction:
    def __init__(self,input_file_path, 
                 model_file_path, 
                 transformer_file_path, 
                 feature_engineering_file_path) -> None:
        
        self.input_file_path = input_file_path
        self.model_file_path = model_file_path
        self.transformer_file_path = transformer_file_path
        self.feature_engineering_file_path = feature_engineering_file_path
    
    # Start the batch prediction
    def start_batch_prediction(self):
        try:
            logging.info("Loading the saved pipeline")

            # Load the feature engineering pipeline
            with open(self.feature_engineering_file_path, 'rb') as f:
                feature_pipeline = pickle.load(f)

            logging.info(f"Feature eng Object acessed :{self.feature_engineering_file_path}")
            
            # Load the data transformation pipeline
            with open(self.transformer_file_path, 'rb') as f:
                preprocessor = pickle.load(f)

            logging.info(f"Preprocessor  Object acessed :{self.transformer_file_path}")
            
            # Load the model separately
            model =load_model(file_path=self.model_file_path)

            logging.info(f"Model File Path: {self.model_file_path}")

            # Create the feature engineering pipeline
            feature_engineering_pipeline = Pipeline([
                ('feature_engineering', feature_pipeline)
            ])

            # Read the input file
            df = pd.read_csv(self.input_file_path)
            # Save to csv
            df.to_csv("df_Zomoto_delivery_time.csv")


            # Apply feature engineering
            df = feature_engineering_pipeline.transform(df)
            # Save to csv
            df.to_csv("df_feature_engineering.csv")
            

            # Save the feature-engineered data as a CSV file
            FEATURE_ENG_PATH = FEATURE_ENG  # Specify the desired path for saving the CSV file
            os.makedirs(FEATURE_ENG_PATH, exist_ok=True)
            file_path = os.path.join(FEATURE_ENG_PATH, 'batch_fea_eng.csv')
            df.to_csv(file_path, index=False)
            logging.info("Feature-engineered batch data saved as CSV.")
            
            # Dropping target column
            df=df.drop('Time_taken (min)', axis=1)
            
            # Save
            df.to_csv('dropped_Time_taken (min).csv')
          
            # Tranform The data
            logging.info(f"Columns before transformation: {', '.join(f'{col}: {df[col].dtype}' for col in df.columns)}")
            # Transform the feature-engineered data using the preprocessor
            transformed_data = preprocessor.transform(df)
            logging.info(f"Transformed Data Shape: {transformed_data.shape}")
            
            logging.info(f"Loaded numpy from batch prediciton :{transformed_data}")
            file_path = os.path.join(FEATURE_ENG_PATH, 'preprocessor.csv') # Save
            
            logging.info(f"Model Data Type : {type(model)}")
            

            # Model predict
            predictions = model.predict(transformed_data)
            logging.info(f"Predictions done :{predictions}")

            # Create a DataFrame from the predictions array
            df_predictions = pd.DataFrame(predictions, columns=['prediction'])
            
            # Save the predictions to a CSV file
            BATCH_PREDICTION_PATH = BATCH_PREDICTION  # Specify the desired path for saving the CSV file
            os.makedirs(BATCH_PREDICTION_PATH, exist_ok=True)
            csv_path = os.path.join(BATCH_PREDICTION_PATH,'predictions.csv')
            df_predictions.to_csv(csv_path, index=False)
            logging.info(f"Batch predictions saved to '{csv_path}'.")

        except Exception as e:
            CustomException(e,sys) 



