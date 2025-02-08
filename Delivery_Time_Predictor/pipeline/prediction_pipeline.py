import os 
import sys
import pandas as pd
from Delivery_Time_Predictor.config.configuration import MODEL_FILE_PATH,PREPROCESSING_OBJ_FILE
from Delivery_Time_Predictor.exception import CustomException
from Delivery_Time_Predictor.logger import logging
from Delivery_Time_Predictor.utils import load_model



class PredictPipeline:
    def __init__(self):
        pass
    
    def predict(self,features):
        try:
            preprocessor_path = PREPROCESSING_OBJ_FILE
            model_path = MODEL_FILE_PATH
            
            preprocessor = load_model(preprocessor_path)
            model = load_model(model_path)
            
            # Scale ths data
            data_scaled = preprocessor.transform(features) # Features are the input values
            
            # Predicted value
            pred = model.predict(data_scaled)
            
            return pred 
        
        except Exception as e:
            logging.info("Error occured in prediction pipeline")
            raise CustomException(e,sys)

# Input variable of all column
# mention the column name along with data type       
class CustomData:
    def __init__(self,
                 Delivery_person_Age:int,  
                 Delivery_person_Ratings:float, 
                 Weather_conditions:str, 
                 Road_traffic_density:str,  
                 Vehicle_condition:int,  
                 multiple_deliveries:int,
                 distance:float,
                 Type_of_order:str,
                 Type_of_vehicle:str,
                 Festival:str,
                 City:str):
        
        self.Delivery_person_Age = Delivery_person_Age
        self.Delivery_person_Ratings = Delivery_person_Ratings
        self.Weather_conditions = Weather_conditions
        self.Road_traffic_density = Road_traffic_density
        self.Vehicle_condition = Vehicle_condition
        self.multiple_deliveries = multiple_deliveries
        self.distance = distance
        self.Type_of_order=Type_of_order
        self.Type_of_vehicle=Type_of_vehicle
        self.Festival=Festival
        self.City=City

    # Convert to data frame 
    def get_data_as_dataframe(self):
        try:
            custom_data_input_dict = {
                'Delivery_person_Age':[self.Delivery_person_Age],
                'Delivery_person_Ratings':[self.Delivery_person_Ratings],
                'Weather_conditions':[self.Weather_conditions],
                'Road_traffic_density':[self.Road_traffic_density],
                'Vehicle_condition':[self.Vehicle_condition],
                'multiple_deliveries':[self.multiple_deliveries],
                'distance':[self.distance],
                'Type_of_order':[self.Type_of_order],
                'Type_of_vehicle':[self.Type_of_vehicle],
                'Festival':[self.Festival],
                'City':[self.City]
            }
            
            df = pd.DataFrame(custom_data_input_dict) # COnvert the dictionary to data frame 
            logging.info("DataFrame gatherd")
            
            return df
        except Exception as e:
            logging.info("Exception occured in Custom data")
            raise CustomException(e,sys)