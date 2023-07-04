# Use the official Python base image
FROM python:3.9

# Set the working directory in the container
WORKDIR /app


# Copy the application code
COPY . .

# Copy the requirements file
COPY requirements.txt .

# Install the dependencies
RUN pip install -r requirements.txt

# # Copy the application code
# COPY . .

# # Copy the local library
# COPY libs /app/libs

# Set the entry point
CMD ["python", "app.py"]

