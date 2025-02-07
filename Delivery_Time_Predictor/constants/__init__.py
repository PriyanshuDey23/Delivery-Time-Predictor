import os, sys
from datetime import datetime

# artifact -> pipeline  folder -> timestamp -> output

ROOT_DIR_KEY = os.getcwd()
DATA_DIR = "Data"
DATA_DIR_KEY = "main.csv"
ARTIFACT_DIR_KEY = "Artifact"

# Data Ingestion related variable
DATA_INGESTION_KEY ="Data_Ingestion" # Folder inside artifact
DATA_INGESTION_RAW_DATA_DIR = "Raw_Data_Dir" # Download data
DATA_INGESTION_INGESTED_DATA_DIR_KEY = "Ingested_Dir" # Train and Test data
RAW_DATA_DIR_KEY = "raw.csv"
TRAIN_DATA_DIR_KEY = "train.csv"
TEST_DATA_DIR_KEY = "test.csv"


# Data Transformation related variable
DATA_TRANSFORMATION_ARTIFACT = "Data_Transformation" # Folder
DATA_PREPROCCED_DIR = "Processor" # Folder
DATA_TRANSFORMTION_PROCESSING_OBJ = "Processor.pkl"  # Save inside Processor
DATA_TRANSFORM_DIR = "Transformation" # Folder
TRANSFORM_TRAIN_DIR_KEY = "train.csv" 
TRANSFORM_TEST_DIR_KEY = "test.csv"
FEATURE_ENGINEERING ="Feature_engg.pkl"




