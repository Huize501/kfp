
ARG BASE_IMAGE_TAG=1.12.0-py3
FROM tensorflow/tensorflow:$BASE_IMAGE_TAG
COPY ./src /app/src
WORKDIR /app/trainer/src
ENTRYPOINT python3 /app/src/task.py