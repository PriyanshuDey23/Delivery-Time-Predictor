# Connect everything
from Delivery_Time_Predictor.constants import *
import os, sys

ROOT_DIR = ROOT_DIR_KEY

# Data Ingestion
# Connect the data (Make all the directories)

DATASET_PATH = os.path.join(ROOT_DIR, DATA_DIR, DATA_DIR_KEY)

RAW_FILE_PATH = os.path.join(ROOT_DIR, ARTIFACT_DIR_KEY, DATA_INGESTION_KEY, 
                             DATA_INGESTION_RAW_DATA_DIR, RAW_DATA_DIR_KEY)


TRAIN_FILE_PATH = os.path.join(ROOT_DIR, ARTIFACT_DIR_KEY, DATA_INGESTION_KEY, 
                               DATA_INGESTION_INGESTED_DATA_DIR_KEY, TRAIN_DATA_DIR_KEY)


TEST_FILE_PATH = os.path.join(ROOT_DIR, ARTIFACT_DIR_KEY, DATA_INGESTION_KEY, 
                               DATA_INGESTION_INGESTED_DATA_DIR_KEY, TEST_DATA_DIR_KEY)


# Data Transformation
## Create all the folders
### Saving preprocessing file
PREPROCESSING_OBJ_FILE = os.path.join(ROOT_DIR, ARTIFACT_DIR_KEY, DATA_TRANSFORMATION_ARTIFACT, 
                                     DATA_PREPROCCED_DIR, DATA_TRANSFORMTION_PROCESSING_OBJ)

## Transform train file  path
TRANSFORM_TRAIN_FILE_PATH = os.path.join(ROOT_DIR, ARTIFACT_DIR_KEY, DATA_TRANSFORMATION_ARTIFACT,
                                         DATA_TRANSFORM_DIR, TRANSFORM_TRAIN_DIR_KEY)

## Transform test file  path
TRANSFORM_TEST_FILE_PATH = os.path.join(ROOT_DIR, ARTIFACT_DIR_KEY, DATA_TRANSFORMATION_ARTIFACT,
                                         DATA_TRANSFORM_DIR, TRANSFORM_TEST_DIR_KEY)


## Save the feature engg pickle file
FEATURE_ENGG_OBJ_FILE_PATH = os.path.join(ROOT_DIR, ARTIFACT_DIR_KEY, DATA_TRANSFORMATION_ARTIFACT,
                                          DATA_PREPROCCED_DIR,FEATURE_ENGINEERING) 


# Model Training
MODEL_FILE_PATH = os.path.join(ROOT_DIR,ARTIFACT_DIR_KEY,
                               MODEL_TRAINER_KEY,MODEL_OBJECT)



