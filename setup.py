from setuptools import setup, find_packages
from typing import List

PROJECT_NAME = "Delivery_Time_Predictor"
VERSION = "0.0.1"
DESCRIPTION = "This is our machine learning project in modular coding"
AUTHOR_NAME = "Priyanshu Dey"
AUTHOR_EMAIL = "priyanshudey.ds@gmail.com"

REQUIREMENTS_FILE_NAME = "requirements.txt"

HYPHEN_E_DOT = "-e ."
# Requriments.txt file open
# read
# \n ""
def get_requirements_list()->List[str]:
    with open(REQUIREMENTS_FILE_NAME) as requriment_file:
        requriment_list = requriment_file.readlines()
        requriment_list = [requriment_name.replace("\n", "") for requriment_name in requriment_list]

        if HYPHEN_E_DOT in requriment_list:
            requriment_list.remove(HYPHEN_E_DOT)

        return requriment_list

setup(name=PROJECT_NAME,
      version=VERSION,
      description=DESCRIPTION,
      author=AUTHOR_NAME,
      author_email=AUTHOR_EMAIL,
      packages=find_packages(),
      install_requries = get_requirements_list()
     )