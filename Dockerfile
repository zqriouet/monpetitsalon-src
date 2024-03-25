# FROM python:3.11
FROM apache/airflow:2.7.3-python3.11
USER root
WORKDIR /app
ADD ./requirements.txt .
RUN apt-get update && apt-get install -y wget unzip && \ 
    wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb && \
    apt install -y ./google-chrome-stable_current_amd64.deb && \
    rm google-chrome-stable_current_amd64.deb && \
    apt-get clean
USER airflow
RUN pip --no-cache-dir install -r requirements.txt && \
    pip --no-cache-dir install -i https://test.pypi.org/simple/ monpetitsalon && \
    pip --no-cache-dir install pytest
ADD ./tests/ .
CMD sleep infinity