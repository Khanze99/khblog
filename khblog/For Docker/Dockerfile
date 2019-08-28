FROM python:3
COPY mysite/requirements.txt ./
RUN pip install -r requirements.txt
COPY mysite mysite
WORKDIR mysite/
EXPOSE 8000
CMD python3 manage.py runserver 0.0.0.0:8000