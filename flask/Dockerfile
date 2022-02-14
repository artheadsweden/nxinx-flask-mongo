FROM python:3.9

WORKDIR /code

ENV FLASK_APP=app

ENV FLASK_RUN_HOST=0.0.0.0

ENV MGDB_HOST=dnfm_mongo

COPY ./flask/requirements.txt requirements.txt

RUN pip install -r requirements.txt

EXPOSE 5000

COPY . .