FROM python:3
ENV PYTHONUNBUFFERED 1
RUN mkdir /code
WORKDIR /code
COPY requirements.txt /code/
RUN apt-get update
RUN pip install -r requirements.txt
COPY requirement.txt /code/
RUN pip install -r requirement.txt
RUN pip install fcm-django
RUN pip list
COPY . /code/