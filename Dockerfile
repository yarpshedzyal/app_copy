# Base Image
FROM ubuntu:20.04

# Environment variables, setting app home path and copy of the python app in the container
ENV PYTHONUNBUFFERED True
ENV APP_HOME /app
WORKDIR $APP_HOME
COPY . ./

# Update/upgrade the system
RUN apt -y update
RUN apt -y upgrade

# Install Python dependencies
RUN apt install -yqq python3-pip

# Install Python dependencies
RUN pip install -r requirements.txt

# Set the entry point
CMD ["python3", "app.py"]
