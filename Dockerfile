# pull official base image
FROM python:3.12-slim-bullseye

# set environment variables
ENV PIP_DISABLE_PIP_VERSION_CHECK 1
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV POETRY_VIRTUALENVS_CREATE=false

# Create a group with a specific GID
RUN groupadd -g 1000 customgroup

# Create a user with a specific UID and assign to the group
RUN useradd -m -u 1000 -g customgroup customuser

# Set the working directory
WORKDIR /app

# install dependencies
RUN pip install --no-cache-dir poetry
COPY poetry.lock pyproject.toml /app/
RUN poetry install

# Copy the rest of the application code
COPY . .

# Change ownership of the app directory to the new user
RUN chown -R customuser:customgroup /app

# Switch to the non-root user
USER customuser
