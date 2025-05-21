# Use the official Python image as the base image
FROM python:3.11-slim

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container
COPY . /app

# Install dependencies (make sure you have a requirements.txt in your project directory)
RUN pip install --no-cache-dir -r requirements.txt

# Expose the port that your app will run on (Azure defaults to 80)
EXPOSE 80

# Set the command to run your application, make sure it's running the correct file (main.py)
CMD ["python", "main.py"]
