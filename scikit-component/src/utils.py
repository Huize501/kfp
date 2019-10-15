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

import os

import src.metadata as metadata

import pandas as pd
from sklearn import model_selection
from sklearn.externals import joblib
import tensorflow as tf
from tensorflow import gfile

def get_data_from_gcs(path_data):
    """
    Reads csv from GCS

    Returns
    -------
       Pandas dataframe
    """
    # make sure to use Pandas >=  0.24
    dataset=pd.read_csv(path_data) 
    print(dataset.head(2))
    return dataset

#TODO REMOVE
def _feature_label_split(data_df, label_column):
    """
    Splits Pandas df in

    Returns
    -------
       Pandas dataframe
    """
    return data_df.loc[:, data_df.columns != label_column], data_df[label_column]

def boolean_mask(columns, target_columns):
    """
      Creates a bboolean mask

      Returns
      -------
        Boolean mask
      """
    target_set = set(target_columns)
    return [x in target_set for x in columns]

def data_train_test_split(data_df):
      """
      Takes Pandas datafram and 
      splits raw data in train and eval

      Returns
      -------
        Train features, train labels, test features, test lables. 
      """
      label_column = metadata.LABEL
      columns_to_use = metadata.FEATURE_COLUMNS + [label_column]

      train, val = model_selection.train_test_split(data_df[columns_to_use])
      x_train, y_train = _feature_label_split(train, label_column)
      x_val, y_val = _feature_label_split(val, label_column)
      
      return x_train, y_train, x_val, y_val

def dump_object(object_to_dump, output_path):
    """
      Writes output trained model pipeline to GCS
    """

    if not tf.io.gfile.exists(output_path):
      gfile.MakeDirs(os.path.dirname(output_path))
    
    with tf.io.gfile.GFile(output_path, 'w') as wf:
      joblib.dump(object_to_dump, wf)

def write_to_file(object_to_dump, output_path):
    """
      Writes output_path (GCS path) to local file
    """
    with gfile.GFile(output_path, "w") as file:
      file.write(object_to_dump)

def read_df_from_bigquery(full_table_path, project_id=None, num_samples=None):
    """
      Reads data from BQ and creates a Pandas dataframe
    Returns
      -------
       Pandas dataframe with raw_data
    """
    query = metadata.QUERY.format(table=full_table_path)

    data_df = pd.read_gbq(query, project_id=project_id, dialect='standard')

    return data_df