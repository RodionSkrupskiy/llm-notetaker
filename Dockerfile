# Use an official Python runtime as a parent image
FROM python:3.10

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

RUN pip install -r requirements.txt
RUN python download_resources.py


EXPOSE 5000

CMD ["python", "src/app.py"]