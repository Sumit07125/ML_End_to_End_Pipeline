import sys
import numpy as np
from dataclasses import dataclass
import pandas as pd

from sklearn.impute import SimpleImputer
from sklearn.preprocessing import OneHotEncoder,StandardScaler
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer

from src.utils import save_object
from src.exception import CustomException
from src.logger import logging
import os

from src.utils import save_object   

@dataclass
class DataTransformationConfig:
    preprocessor_obj_file_path = os.path.join("artifacts","preporcessor.pkl")

class DataTransformation:

    '''This Function is the responsible for data transformation'''

    def __init__(self):
        self.data_transformation_Config = DataTransformationConfig()

    def get_data_transformer_object(self):
        try:
            numerical_columns = ['writing_score','reading_score']
            categorical_columns = ["gender","race_ethnicity"
                                ,"parental_level_of_education",
                                "lunch", "test_preparation_course"
                                ]

            num_pipeline = Pipeline(\
                steps=[
                ("imputer",SimpleImputer(strategy="median")),
                ("scaler",StandardScaler())
            ])

            cat_pipeline = Pipeline(
                steps=[
                ("imputer",SimpleImputer(strategy="most_frequent")),    
                ("one_hot_encoder",OneHotEncoder()),    
                ("scaler",StandardScaler(with_mean=False)) 
                ]) 


            logging.info(f'Categorical Columns: {categorical_columns}')
            logging.info(f'Numerical Columns: {numerical_columns}')


            preprocessor = ColumnTransformer(
                [
                    ("num_pipeline",num_pipeline,numerical_columns),
                    ("cat_pipeline",cat_pipeline,categorical_columns)
                ]
            )

            return preprocessor

        except Exception as e:
            raise CustomException(e, sys)


    def initiate_data_transformation(self,train_path,test_path):
        try:
            train_df = pd.read_csv(train_path)
            test_df = pd.read_csv(test_path)

            logging.info("Read train and test data completed")
            logging.info(f"Train Dataframe Head: \n{train_df.head().to_string()}")
            logging.info(f"Test Dataframe Head: \n{test_df.head().to_string()}")

            processing_obj = self.get_data_transformer_object()

            target_column_name = "math_score"
            numerical_columns = ['writing_score','reading_score']

            input_feature_train_df = train_df.drop(columns=[target_column_name],axis=1) #X_train
            target_feature_train_df = train_df[target_column_name]                      #y_train

            input_feature_test_df = test_df.drop(columns=[target_column_name],axis=1)   #X_test   
            target_feature_test_df = test_df[target_column_name]                        #y_test

            logging.info(f"Applying preprocessing object on training and testing datasets.")


            input_feature_train_arr = processing_obj.fit_transform(input_feature_train_df)
            input_feature_test_arr = processing_obj.transform(input_feature_test_df)

            # Merge processed features with target labels column-wise [ features,Target] ex [a,b,c,d,Target]
            train_arr = np.c_[input_feature_train_arr, np.array(target_feature_train_df)]
            test_arr = np.c_[input_feature_test_arr, np.array(target_feature_test_df)]


            logging.info(f"Saved preprocessing object.")
            save_object(
                file_path=self.data_transformation_Config.preprocessor_obj_file_path,  
                obj=processing_obj)

            return (
                train_arr,
                test_arr,
                self.data_transformation_Config.preprocessor_obj_file_path
            )   
        except Exception as e:
            raise CustomException(e, sys)