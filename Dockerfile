FROM python:3.10

COPY requirements.txt requirements.txt

RUN pip install -r requirements.txt

COPY . /app

WORKDIR /app

CMD ["python", "manage.py", "runserver", "0:8000"]
