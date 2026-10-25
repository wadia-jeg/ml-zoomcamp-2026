FROM python:3.8.12-slim

RUN pip install pipenv

# Creates a working diretory and cds into it
WORKDIR /app

COPY ["Pipfile", "Pipfile.lock", "predict.py", "modelC=1.0.bin", "./"]

# Installing dependencies direclty into the system insteead of a virtual environment 
RUN pipenv install --system --deploy

EXPOSE 9696:9696

ENTRYPOINT ["gunicorn", "--bind=0.0.0.0:9696", "predict:app"]