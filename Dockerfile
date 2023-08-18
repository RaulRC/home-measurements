# Use an official Python runtime as a parent image
FROM python:3.10.11-slim-buster
RUN apt-get update

# Set the working directory to /app

# Create a non-root user
RUN useradd --create-home appuser
WORKDIR /home/appuser

RUN mkdir -p /app/src

EXPOSE 8000

# Copy the current directory contents into the container at /app
COPY pyproject.toml /app
COPY src /app/src

WORKDIR /app

# Install any needed packages
ENV PYTHONPATH=${PYTHONPATH}:${PWD}
RUN pip3 install poetry
RUN poetry config virtualenvs.create false
RUN poetry install --only main

USER appuser

CMD  poetry run uvicorn src.api.api_handler:app --host 0.0.0.0 --port 8000
# Run app.py when the container launches

