FROM python:3
COPY . .
RUN pip install -r requirements.txt
WORKDIR khblog/
EXPOSE 8000
CMD ["runserver"]