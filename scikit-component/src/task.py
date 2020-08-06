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

import argparse
import time
import os

import model as model
import utils as utils
import metadata as metadata

from sklearn import model_selection
from pathlib import Path

def get_args():
    """
    Parses commandline arguments

    Returns
    -------
       Command line arguments
    """

    parser = argparse.ArgumentParser(
        description='ArgeParser'
        )

    parser.add_argument('--pathdata', 
                        help='GCS path to where the raw data is',
                        type=str,
                        required=False,
                        default=1
                        )

    parser.add_argument('--storage', 
                        help='Where your data is stored: BQ or GCS',
                        type=str,
                        required=True,
                        default=1
                        )

    parser.add_argument('--pathoutput', 
                        help='GCS bucket to output the trained model: model.joblib',
                        required=True,
                        type=str,
                        default=1
                        )

    parser.add_argument('--pathoutputfile', 
                        help='Where to write the local file containing data that needs to be passed',
                        required=True,
                        type=str,
                        default=1
                        )                    

    parser.add_argument('--bqtable', 
                        help='Full path to the BigQuery table: yourproject.dataset.table',
                        type=str,
                        required=False,
                        default=1
                        )

    arguments = parser.parse_args()

    return arguments

def main():
    """
    Main function
    """

    args = get_args()

    output_bucket = args.pathoutput

    storage = args.storage

    full_table_path = args.bqtable

    # Fetch training data from BQ or GCS
    if storage in ['BQ', 'bq' 'bigquery', 'BigQuery', 'bigQuery', 'Bigquery', 'Bq']:
      dataset = utils.read_df_from_bigquery(full_table_path)
    else:
      dataset = utils.get_data_from_gcs(args.pathdata)

    x_train, y_train, x_val, y_val = utils.data_train_test_split(dataset)

    # Get pipeline and fit model
    pipeline = model.get_pipeline()
   
    pipeline.fit(x_train, y_train)

    scores = model_selection.cross_val_score(pipeline, x_val, y_val, cv=3)

    print('model score: %.3f' % pipeline.score(x_val, y_val))
    print('pipeline run done :)')

    # Output results and trained model
    model_output_path = os.path.join(output_bucket,'model/', metadata.MODEL_FILE_NAME)

    metric_output_path = os.path.join(output_bucket, 'experiment', metadata.METRIC_FILE_NAME)

    utils.dump_object(pipeline, model_output_path)
    utils.dump_object(scores, metric_output_path)

    joblib_output_path = os.path.join(output_bucket, 'model/')

    # Write GCS path to local file 
    # This GCS path can be passed to the next component
    Path(args.pathoutputfile).parent.mkdir(parents=True, exist_ok=True)
    Path(args.pathoutputfile).write_text(joblib_output_path)

if __name__ == '__main__':
    main()

    