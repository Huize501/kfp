# Copyright 2018 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import functools
import metadata
import utils

import numpy as np
from sklearn import compose
from sklearn import impute
from sklearn import pipeline
from sklearn import preprocessing

def get_preprocess_pipeline(feature_columns, categorical_names, numerical_names):
    """
    Creates the preprocessor used to process the data for training. 
    This will be combined with the estimator 
    
    Returns
    -------
       Preprocessor
    """

    numeric_transformer = pipeline.Pipeline([
        ('imputer', impute.SimpleImputer(strategy='median')),
        ('scaler', preprocessing.StandardScaler()),
        ])

    categorical_transformer = pipeline.Pipeline([
        ('onehot', preprocessing.OneHotEncoder(
            handle_unknown='ignore', sparse=False)),
        ])

    feature_columns = metadata.FEATURE_COLUMNS
    numerical_names = metadata.NUMERIC_FEATURES
    categorical_names = metadata.CATEGORICAL_FEATURES

    boolean_mask = functools.partial(utils.boolean_mask, feature_columns)
    numerical_boolean = boolean_mask(numerical_names)
    categorical_boolean = boolean_mask(categorical_names)

    transform_list = []

    if any(numerical_boolean):
             transform_list.extend([('numeric', numeric_transformer, numerical_boolean),
             ])

    if any(categorical_boolean):
            transform_list.extend([
            ('categorical', categorical_transformer, categorical_boolean),
            ])

    preprocessor = compose.ColumnTransformer(transform_list)

    return preprocessor

