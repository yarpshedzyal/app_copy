# # Use the official Python base image
# # FROM python:3.9

# FROM selenium/standalone-chrome:latest 

# # # Set the working directory in the container
# # WORKDIR /app

# # # Copy the requirements file
# # COPY requirements.txt .

# # # Install the dependencies
# # RUN pip install -r requirements.txt

# # # Copy the application code
# # COPY . .

# # RUN apt-get update && \
# #     apt-get install -y gnupg wget curl unzip --no-install-recommends && \
# #     wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add - && \
# #     echo "deb http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google.list && \
# #     apt-get update -y && \
# #     apt-get install -y google-chrome-stable && \
# #     CHROMEVER=$(google-chrome --product-version | grep -o "[^\.]*\.[^\.]*\.[^\.]*") && \
# #     DRIVERVER=$(curl -s "https://chromedriver.storage.googleapis.com/LATEST_RELEASE_$CHROMEVER") && \
# #     wget -q --continue -P /chromedriver "http://chromedriver.storage.googleapis.com/$DRIVERVER/chromedriver_linux64.zip" && \
# #     unzip /chromedriver/chromedriver* -d /chromedriver

# # Set the working directory in the container
# WORKDIR /app


# COPY . . 

# # Install the dependencies
# RUN pip install -r requirements.txt


# # # Install Chrome and ChromeDriver
# # RUN apt-get update
# # RUN apt-get install -y wget unzip
# # RUN wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add -
# # RUN echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google-chrome.list
# # RUN apt-get update
# # RUN apt-get install -y google-chrome-stable
# # RUN wget -N https://chromedriver.storage.googleapis.com/$(curl -sS chromedriver.storage.googleapis.com/LATEST_RELEASE)/chromedriver_linux64.zip -P /tmp/
# # RUN unzip /tmp/chromedriver_linux64.zip -d /usr/bin/
# # RUN chmod +x /usr/bin/chromedriver

# # Set the entry point
# # CMD ["python", "app.py"]

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

# Install App dependencies and chrome webdriver
RUN apt install -yqq unzip curl wget python3-pip
RUN DEBIAN_FRONTEND="noninteractive" apt-get -y install tzdata
RUN wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb
RUN apt install -y --no-install-recommends ./google-chrome-stable_current_amd64.deb
RUN wget -O /tmp/chromedriver.zip http://chromedriver.storage.googleapis.com/`curl -sS chromedriver.storage.googleapis.com/LATEST_RELEASE`/chromedriver_linux64.zip
RUN unzip /tmp/chromedriver.zip chromedriver -d /usr/local/bin/

# Install Python dependencies
RUN pip install -r requirements.txt

# # Set the entry point
CMD ["python3", "app.py"]