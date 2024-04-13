FROM python:3.11

WORKDIR /app

RUN pip install --upgrade pip
COPY ./requirements.txt .
RUN pip install -r requirements.txt --no-cache-dir

COPY ./etl .


#CMD gunicorn config.wsgi:application --bind 0.0.0.0:8000