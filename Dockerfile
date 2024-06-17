FROM python:3.10

# Allow statements and log messages to immediately appear in the Cloud Run logs
ENV PYTHONUNBUFFERED True

# Set the working directory
ENV APP_HOME /app
WORKDIR $APP_HOME
COPY . ./

# Copying this separately prevents re-running pip install on every code change.

# Install the required dependencies
RUN pip install -r requirements.txt
RUN pip install gunicorn

RUN apt-get update && apt-get install ffmpeg libsm6 libxext6  -y

# Run app.py when the container launches
CMD exec gunicorn --bind :$PORT --workers 1 --threads 8 --timeout 0 app:app