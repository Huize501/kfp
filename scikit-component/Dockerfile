
ARG BASE_IMAGE_TAG=1.12.0-py3
FROM tensorflow/tensorflow:$BASE_IMAGE_TAG
COPY requirements.txt /tmp
RUN pip install -r /tmp/requirements.txt
COPY ./trainer /pipelines/component/src
ENTRYPOINT python3 /pipelines/component/src/task.py