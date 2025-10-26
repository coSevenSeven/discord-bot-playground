FROM python:3.11-slim-bullseye

# setting working directory
WORKDIR /app

COPY ./requirements.txt ./requirements.txt

# install dependencies
RUN pip install -r requirements.txt --no-cache-dir

# copy this project to the working directory
COPY . /app

# run the app by using uvicorn command
CMD ["python", "main.py"]