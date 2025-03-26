import sys
from dataclasses import dataclass
import os

import numpy as np
import pandas as pd
from sklearn.compose import ColumnTransformer #to apply all data encoing method in piplines
from sklearn.impute import SimpleImputer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler

from src.exception import CustomException
from src.logger import logging

from src.utils import save_object

@dataclass
class DataTransformationConfig:
    preprocessor_obj_file_path = os.path.join('artifact', 'preprocessor.pkl')

class DataTransformation:
    def __init__(self):
        self.data_transformaton_config = DataTransformationConfig()

    def get_data_transformer_object(self):
        '''
            This function is responsile for data transformation        
        '''
        try:
            numerical_columns = ["writing score", "reading score"]
            categorical_columns = [
                "gender",
                "race/ethnicity",
                "lunch",
                "test preparation course"
            ]
            num_pipeline = Pipeline(
                steps=[
                    ("imputer", SimpleImputer(strategy="median")),# handle missing values
                    ("scaler", StandardScaler(with_mean=False))
                ]
            )
            logging.info(f"Numerical columns :{numerical_columns}")

            cat_pipeline = Pipeline(
                steps=[
                    ("imputer", SimpleImputer(strategy="most_frequent")),
                    ("One_Hot_Encoder", OneHotEncoder(sparse_output=False)),
                    ("Scaler", StandardScaler(with_mean=False))
                ]
            )
            logging.info(f"Categorical columns: {categorical_columns}")

            preprocessor = ColumnTransformer(
                [
                    ("num_pipeline", num_pipeline, numerical_columns),
                    ("cat_pipeline", cat_pipeline, categorical_columns)
                ]
            )
            return preprocessor
        except Exception as e:
            raise CustomException(e, sys)
        
    def initiate_data_transformation(self, train_path, test_path):
        try:
            train_df = pd.read_csv(train_path)
            test_df = pd.read_csv(test_path)

            logging.info("Read train and test data completed")

            logging.info("Obtaining  preprocesso object")

            preprocessor_obj = self.get_data_transformer_object()

            target_column_name = "math score"

            numerical_columns = ["writing score", "reading score"]

            input_feature_train_df = train_df.drop(columns=[target_column_name], axis=1)
            target_feature_train_df = train_df[target_column_name]

            input_feature_test_df = test_df.drop(columns=[target_column_name], axis=1)
            target_feature_test_df = test_df[target_column_name]

            logging.info(f"Applying preprocessor object on training dataframe and testing dataframe")

            input_feature_train_arr = preprocessor_obj.fit_transform(input_feature_train_df)
            input_feature_test_arr = preprocessor_obj.transform(input_feature_test_df)

            train_arr = np.c_[
                input_feature_train_arr, np.array(target_feature_train_df)
            ]#This statement is using NumPy’s np.c_[] to concatenate two arrays column-wise
            test_arr = np.c_[
                input_feature_test_arr, np.array(target_feature_test_df)
                             ]
            
            logging.info(f"saved preprocessing object")

            save_object(
                file_path = self.data_transformaton_config.preprocessor_obj_file_path,
                obj = preprocessor_obj
            )# save pickle file
            return(
                train_arr,
                test_arr,
                self.data_transformaton_config.preprocessor_obj_file_path
            )

        except Exception as e:
            raise CustomException(e, sys)
            