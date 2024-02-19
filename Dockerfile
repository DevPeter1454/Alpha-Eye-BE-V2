# Use an official Python runtime as a parent image
FROM python:3.11

ARG CACHEBUST=1

# Set the working directory to /app
WORKDIR /app

COPY requirements.txt ./


# Copy the current directory contents into the container at /app
COPY . /app

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir --upgrade -r requirements.txt


# Expose the port that FastAPI will run on
EXPOSE 8000

# Command to run the application
CMD ["uvicorn", "src.app.main:app", "--host", "0.0.0.0", "--port", "8000"]


# # --------- requirements ---------

# FROM python:3.11 as requirements-stage

# WORKDIR /tmp

# RUN pip install poetry

# COPY ./pyproject.toml ./poetry.lock* /tmp/

# RUN poetry export -f requirements.txt --output requirements.txt --without-hashes


# # --------- final image build ---------
# FROM python:3.11

# WORKDIR /code

# COPY --from=requirements-stage /tmp/requirements.txt /code/requirements.txt

# RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

# COPY ./src/app /code/app

# # -------- replace with comment to run with gunicorn --------
# CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
# # CMD ["gunicorn", "app.main:app", "-w", "4", "-k", "uvicorn.workers.UvicornWorker". "-b", "0.0.0.0:8000"]
