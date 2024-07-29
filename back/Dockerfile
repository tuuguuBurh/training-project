FROM python:3.12 AS req-stage
WORKDIR /tmp
RUN pip install --upgrade pip
RUN pip install --no-cache-dir poetry
COPY ./back/pyproject.toml ./back/poetry.lock* /tmp/
RUN poetry export -f requirements.txt --output requirements.txt --without-hashes --dev

FROM python:3.12 AS build-stage

WORKDIR /code

RUN pip install --upgrade pip
COPY --from=req-stage /tmp/requirements.txt /code/requirements.txt
RUN pip install --user --no-cache-dir -r /code/requirements.txt

FROM python:3.12-slim
# set env variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set timezone
ENV TZ=Asia/Ulaanbaatar
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

WORKDIR /code

COPY --from=build-stage /root/.local /root/.local

ENV PATH=/root/.local/bin:$PATH
