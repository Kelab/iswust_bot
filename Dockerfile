FROM python:3.8.2-slim

RUN sed -i 's|http://deb.debian.org|https://mirrors.tuna.tsinghua.edu.cn|g' /etc/apt/sources.list
RUN sed -i 's|http://security.debian.org|https://mirrors.tuna.tsinghua.edu.cn|g' /etc/apt/sources.list

RUN apt-get update
RUN apt-get install -y --no-install-recommends build-essential python3-dev python3-pip curl

RUN curl -sSL https://cdn.jsdelivr.net/gh/python-poetry/poetry/get-poetry.py | python3
ENV PATH "/root/.poetry/bin:/opt/venv/bin:${PATH}"

# Only copying these files here in order to take advantage of Docker cache. We only want the
# next stage (poetry install) to run if these files change, but not the rest of the app.
COPY pyproject.toml poetry.lock /qbot/
WORKDIR /qbot

# Currently poetry install is significantly slower than pip install, so we're creating a
# requirements.txt output and running pip install with it.
# Follow this issue: https://github.com/python-poetry/poetry/issues/338
# Setting --without-hashes because of this issue: https://github.com/pypa/pip/issues/4995
RUN poetry config virtualenvs.create false \
  && poetry export --without-hashes -f requirements.txt \
  |  poetry run pip install -r /dev/stdin \
  && poetry debug

COPY . /qbot

# Because initially we only copy the lock and pyproject file, we can only install the dependencies
# in the RUN above, as the `packages` portion of the pyproject.toml file is not
# available at this point. Now, after the whole package has been copied in, we run `poetry install`
# again to only install packages, scripts, etc. (and thus it should be very quick).
# See this issue for more context: https://github.com/python-poetry/poetry/issues/1899
RUN poetry install --no-interaction --no-dev

VOLUME /qbot /coolq /root/.cache/pypoetry


ENTRYPOINT ["poetry", "run"]
