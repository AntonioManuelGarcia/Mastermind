FROM python:3.8
ENV PYTHONUNBUFFERED=1
WORKDIR /django
COPY requeriments.txt requeriments.txt

RUN pip3 install -r requeriments.txt
