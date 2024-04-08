FROM python:3.10-alpine

RUN pip3 install --upgrade pip
WORKDIR /app
COPY requirements.txt /app
RUN pip3 --no-cache-dir install -r requirements.txt
COPY . /app

RUN python3 manage.py collectstatic --noinput

EXPOSE 8000
