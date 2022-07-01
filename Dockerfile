FROM python:3.9.13-slim-buster

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
RUN apt-get update && apt-get -y install libpq-dev gcc
WORKDIR /code
COPY requirements.txt /code/
RUN pip install -r requirements.txt
COPY . /code/
CMD ["calendar_for_you.wsgi", "--bind", "0.0.0.0:8000", "--log-file", "-"]
ENTRYPOINT ["gunicorn"]
EXPOSE 8000
