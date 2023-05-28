# use Multi-stage Docker build
# pull official base image
FROM python:3.11-slim as builder

# set work directory
WORKDIR /app

# set environment variables
# prevent Python from writing pyc files to disc
ENV PYTHONDONTWRITEBYTECODE 1
# prevent Python from buffering stdout and stderr
ENV PYTHONUNBUFFERED 1

# install system dependencies
RUN apt-get update && apt-get install -y \
    python3-all-dev \
    build-essential \
    libpq-dev

# install dependencies
COPY /requirements .
RUN pip wheel --no-cache-dir --no-deps --wheel-dir /app/wheels -r dev.txt


###############
# FINAL STAGE
#

FROM python:3.11-slim

ENV APP_HOME=/home/app
WORKDIR $APP_HOME

# install dependencies
COPY --from=builder /app/wheels /wheels
RUN pip install --no-cache /wheels/*

COPY . .

# create the app user
RUN addgroup --system app && adduser --system --group app

# chown all the files to the app user
RUN chown -R app:app $APP_HOME

# change to the app user
USER app
