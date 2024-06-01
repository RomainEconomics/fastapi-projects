
FROM python:3.10-slim-buster

ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1

RUN apt-get update \
  # dependencies for building Python packages
  && apt-get install -y build-essential \
  # cleaning up unused files
  && apt-get purge -y --auto-remove -o APT::AutoRemove::RecommendsImportant=false \
  && rm -rf /var/lib/apt/lists/*

WORKDIR /code

COPY requirements.txt /code/requirements.txt

# to use when "uv" fixes the issue related to private packages
# ENV VIRTUAL_ENV=/usr/local
# RUN pip install uv && uv pip install --no-cache -r requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

COPY . /code/
