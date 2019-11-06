
ARG BASE_IMAGE_TAG=1.12.0-py3
FROM tensorflow/tensorflow:$BASE_IMAGE_TAG
COPY requirements.txt /tmp
RUN pip install -r /tmp/requirements.txt
COPY ./src /pipelines/component/src
ENTRYPOINT python3 /pipelines/component/src/task.py --pathdata gs://erwinh-public-data/scikit/data/scikit-marketing-data.csv \
--storage GCS --pathoutput gs://kfp-scikit/model/output/ \
--pathoutputfile fileoutput