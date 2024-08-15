FROM python:alpine


WORKDIR /app

COPY ../../requirements.txt /app/

RUN pip install --upgrade pip && pip install -r requirements.txt

COPY ../.. /app/


ENV PYTHONUNBUFFERED=1

RUN python manage.py migrate
RUN python manage.py collectstatic --noinput

CMD ["gunicorn" , "--bind" , "0.0.0.0:8000" , "config.wsgi:application"]