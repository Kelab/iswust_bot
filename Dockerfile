FROM python:3.8.2-slim

RUN sed -i 's|http://deb.debian.org|https://mirrors.tuna.tsinghua.edu.cn|g' /etc/apt/sources.list
RUN sed -i 's|http://security.debian.org|https://mirrors.tuna.tsinghua.edu.cn|g' /etc/apt/sources.list

RUN apt-get update
RUN apt-get install -y --no-install-recommends build-essential python3-dev python3-pip curl
RUN curl -sSL https://cdn.jsdelivr.net/gh/python-poetry/poetry/get-poetry.py | python3
ENV PATH "/root/.poetry/bin:/opt/venv/bin:${PATH}"

COPY . /qbot
WORKDIR /qbot
RUN poetry install --no-interaction --no-dev

VOLUME /qbot /coolq
