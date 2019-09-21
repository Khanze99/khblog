FROM python:3
COPY . /khblog
WORKDIR khblog
RUN pip install -r requirements.txt
