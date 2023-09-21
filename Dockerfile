# Use an official Python runtime as the base image
FROM python:3.9

# Set the working directory in the container
WORKDIR /home/python/app

# Copy the application code into the container
COPY app /home/python/app

# Install any needed packages or dependencies (e.g., requirements.txt)
COPY requirements.txt /home/python/app/
RUN pip install --no-cache-dir -r /home/python/app/requirements.txt

# Define the command to run your Python application
CMD ["python", "app.py"]
