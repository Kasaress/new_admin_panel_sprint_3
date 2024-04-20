FROM python:3.11

WORKDIR /app

RUN pip install --upgrade pip
COPY ./requirements.txt .
RUN pip install -r requirements.txt --no-cache-dir

COPY ./movies_admin .

RUN python manage.py collectstatic --noinput

CMD gunicorn config.wsgi:application --bind 0.0.0.0:8000