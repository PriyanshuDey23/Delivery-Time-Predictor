from Delivery_Time_Predictor.logger import logging
from Delivery_Time_Predictor.exception import CustomException
import os, sys
import pickle
from sklearn.metrics import r2_score

def save_obj(file_path, obj):
    try:
        dir_path = os.path.dirname(file_path)
        os.makedirs(dir_path, exist_ok=True)

        with open(file_path, "wb") as file_obj:
            pickle.dump(obj,file_obj)

    except Exception as e:
        raise CustomException(e, sys)
    

# Evluate model    
def evaluate_model(X_train, y_train,X_test, y_test, models):
    try:
        report = {}

        for i in range(len(models)):
            model = list(models.values())[i] # Get the model value

            model.fit(X_train, y_train) # Fit

            y_test_pred = model.predict(X_test) # Predict

            test_model_score = r2_score(y_test,y_test_pred ) # Get r2 score

            report[list(models.keys())[i]] = test_model_score # Sotre in report , find model keys

        return report

    except Exception as e:
        logging.info('Exception occured while saving an object')
        raise CustomException(e,sys)

