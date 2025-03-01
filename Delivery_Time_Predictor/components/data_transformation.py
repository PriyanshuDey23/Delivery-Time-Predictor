from Delivery_Time_Predictor.constants import *
from Delivery_Time_Predictor.logger import logging
from Delivery_Time_Predictor.exception import CustomException
import os, sys
from Delivery_Time_Predictor.config.configuration import *
from dataclasses import dataclass
from sklearn.base import BaseEstimator, TransformerMixin
import numpy as np
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import StandardScaler, OrdinalEncoder, OneHotEncoder
from sklearn.pipeline import Pipeline
from Delivery_Time_Predictor.utils import save_obj

class Feature_Engineering(BaseEstimator, TransformerMixin):
    def __init__(self):
        logging.info(f"\n{'*'*20} Feature Engineering Started {'*'*20}\n\n")

    # Calculate distance based on latitude and longitude
    def distance_numpy(self, df, lat1, lon1, lat2, lon2):
        try:
            p = np.pi / 180
            a = 0.5 - np.cos((df[lat2] - df[lat1]) * p) / 2 + np.cos(df[lat1] * p) * np.cos(df[lat2] * p) * (1 - np.cos((df[lon2] - df[lon1]) * p)) / 2
            df['distance'] = 12742 * np.arcsin(np.sqrt(a))
        except KeyError as e:
            logging.error(f"Missing required columns for distance calculation: {str(e)}")
            raise CustomException(f"Missing required columns: {str(e)}", sys)

    # Transform Data
    def transform_data(self, df):
        try:
            df.drop(['ID'], axis=1, inplace=True, errors='ignore')

            logging.info("Dropping the ID column")

            # Create distance feature
            logging.info("Creating feature on latitude and longitude")
            self.distance_numpy(df, 'Restaurant_latitude', 'Restaurant_longitude', 
                                'Delivery_location_latitude', 'Delivery_location_longitude')

            # Drop unnecessary columns
            # df.drop(['Delivery_person_ID', 'Restaurant_latitude', 'Restaurant_longitude',
            #          'Delivery_location_latitude', 'Delivery_location_longitude', 'Order_Date', 
            #          'Time_Orderd', 'Time_Order_picked'], axis=1, inplace=True)
            # logging.info("Dropped unnecessary columns")

            logging.info(f"Transformed Dataframe Head: \n{df.head().to_string()}")
            return df

        except Exception as e:
            logging.error("Error in transforming data")
            raise CustomException(e, sys) from e

    def fit(self, X, y=None):
        return self
    
    def transform(self, X: pd.DataFrame, y=None):
        try:
            transformed_df = self.transform_data(X)
            return transformed_df
        except Exception as e:
            raise CustomException(e, sys) from e


@dataclass
class DataTransformationConfig:
    proccessed_obj_file_path = PREPROCESSING_OBJ_FILE
    transform_train_path = TRANSFORM_TRAIN_FILE_PATH
    transform_test_path = TRANSFORM_TEST_FILE_PATH
    feature_engg_obj_path = FEATURE_ENGG_OBJ_FILE_PATH


class DataTransformation:
    def __init__(self):
        self.data_transformation_config = DataTransformationConfig()

    def get_data_transformation_obj(self):
        try:
            logging.info('Data Transformation initiated')

            # Defining the ordinal data ranking
            Road_traffic_density = ['Low', 'Medium', 'High', 'Jam']
            Weather_conditions = ['Sunny', 'Cloudy', 'Windy', 'Fog', 'Sandstorms', 'Stormy']

            # Defining the categorical and numerical columns
            categorical_columns = ['Type_of_order', 'Type_of_vehicle', 'Festival', 'City']
            ordinal_encoder = ['Road_traffic_density', 'Weather_conditions']
            numerical_column = ['Delivery_person_Age', 'Delivery_person_Ratings', 'Vehicle_condition',
                                'multiple_deliveries', 'distance']

            # Numerical pipeline
            numerical_pipeline = Pipeline(steps=[
                ('impute', SimpleImputer(strategy='constant', fill_value=0)),
                ('scaler', StandardScaler(with_mean=False))
            ])

            # Categorical pipeline
            categorical_pipeline = Pipeline(steps=[
                ('impute', SimpleImputer(strategy='most_frequent')),
                ('onehot', OneHotEncoder(handle_unknown='ignore')),
                ('scaler', StandardScaler(with_mean=False))
            ])

            # Ordinal pipeline
            ordinal_pipeline = Pipeline(steps=[
                ('impute', SimpleImputer(strategy='most_frequent')),
                ('ordinal', OrdinalEncoder(categories=[Road_traffic_density, Weather_conditions])),
                ('scaler', StandardScaler(with_mean=False))
            ])

            # Apply pipelines on the columns
            preprocessor = ColumnTransformer([
                ('numerical_pipeline', numerical_pipeline, numerical_column),
                ('categorical_pipeline', categorical_pipeline, categorical_columns),
                ('ordinal_pipeline', ordinal_pipeline, ordinal_encoder)
            ])

            logging.info("Pipeline Steps Completed")
            return preprocessor

        except Exception as e:
            logging.error("Error in data transformation")
            raise CustomException(e, sys)

    def get_feature_engineering_object(self):
        try:
            feature_engineering = Pipeline(steps=[("fe", Feature_Engineering())])  # Feature engineering object
            return feature_engineering
        except Exception as e:
            raise CustomException(e, sys) from e

    def initiate_data_transformation(self, train_path, test_path):
        try:
            train_df = pd.read_csv(train_path)
            test_df = pd.read_csv(test_path)

            # Feature Engineering
            logging.info("Obtaining Feature Engineering Object")
            fe_obj = self.get_feature_engineering_object()

            logging.info("Applying Feature Engineering on training and test data")
            train_df = fe_obj.fit_transform(train_df)
            test_df = fe_obj.transform(test_df)

            # Data Preprocessing
            preprocessing_obj = self.get_data_transformation_obj()

            target_columns_name = "Time_taken (min)"
            X_train = train_df.drop(columns=target_columns_name, axis=1)
            y_train = train_df[target_columns_name]

            X_test = test_df.drop(columns=target_columns_name, axis=1)
            y_test = test_df[target_columns_name]

            # Transforming the data
            X_train = preprocessing_obj.fit_transform(X_train)
            X_test = preprocessing_obj.transform(X_test)

            # Combining data and saving
            train_arr = np.c_[X_train, np.array(y_train)]
            test_arr = np.c_[X_test, np.array(y_test)]

            df_train = pd.DataFrame(train_arr)
            df_test = pd.DataFrame(test_arr)

            # Save transformed data
            os.makedirs(os.path.dirname(self.data_transformation_config.transform_train_path), exist_ok=True)
            df_train.to_csv(self.data_transformation_config.transform_train_path, index=False, header=True)

            os.makedirs(os.path.dirname(self.data_transformation_config.transform_test_path), exist_ok=True)
            df_test.to_csv(self.data_transformation_config.transform_test_path, index=False, header=True)

            # Save the feature engineering and preprocessing objects
            save_obj(file_path=self.data_transformation_config.proccessed_obj_file_path, obj=preprocessing_obj)
            save_obj(file_path=self.data_transformation_config.feature_engg_obj_path, obj=fe_obj)

            logging.info("Transformation completed successfully.")

            return train_arr, test_arr, self.data_transformation_config.proccessed_obj_file_path

        except Exception as e:
            logging.error("Error in data transformation")
            raise CustomException(e, sys)
        

if __name__ == "__main__":
    data_transformation = DataTransformation()
    train_arr,test_arr,_ = data_transformation.inititate_data_transformation(TRAIN_FILE_PATH,TEST_FILE_PATH)