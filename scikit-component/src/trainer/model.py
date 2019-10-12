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

import utils
import preprocess_utils
import metadata

import numpy as np
from sklearn import compose
from sklearn import ensemble
from sklearn import impute
from sklearn import pipeline
from sklearn import preprocessing
import tensorflow as tf
import pandas as pd

def get_estimator():
    """
    Specifies the estimator (model)

    Returns
    -------
       Estimator
    """

    classifier = ensemble.RandomForestClassifier(
        n_estimators=20)

    return classifier

def get_pipeline():
    """
    Creates a pipeline combining the prepprocessor and estimator. 

    Returns
    -------
       Pipeline
    """

    classifier = get_estimator()

    feature_columns = metadata.FEATURE_COLUMNS
    numerical_names = metadata.NUMERIC_FEATURES
    categorical_names = metadata.CATEGORICAL_FEATURES

    preprocessor = preprocess_utils.get_preprocess_pipeline(
                                  feature_columns=feature_columns,
                                  numerical_names=numerical_names,
                                  categorical_names=categorical_names
                                  )

    estimator_pipeline = pipeline.Pipeline([
        ('preprocessor', preprocessor),
        ('classifier', classifier),
        ])

    return estimator_pipeline




