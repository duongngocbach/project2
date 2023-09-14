FROM python:3.10
ENV PYTHONUNBUFFERED=1
WORKDIR /code
COPY requirements.txt /code/
RUN pip install --upgrade pip
RUN pip install -r requirements.txt && apt-get update -y && apt-get install -y iputils-ping
COPY . /code/
EXPOSE 8080
CMD ["gunicorn", "inf_be.wsgi:application", "--bind", "0.0.0.0:8080", "--timeout", "200", "--workers", "2"]
