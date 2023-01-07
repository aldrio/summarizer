FROM python:3

WORKDIR /usr/src/app

ENV POETRY_VERSION=1.2.0
ENV POETRY_HOME=/opt/poetry
ENV POETRY_VENV=/opt/poetry-venv
ENV POETRY_CACHE_DIR=/opt/.cache

RUN python3 -m venv $POETRY_VENV \
    && $POETRY_VENV/bin/pip install -U pip setuptools \
    && $POETRY_VENV/bin/pip install poetry==${POETRY_VERSION}
ENV PATH="${PATH}:${POETRY_VENV}/bin"


COPY poetry.lock pyproject.toml ./
RUN poetry install
COPY build.py ./
RUN poetry run python build.py

COPY . .

EXPOSE 8000

ENTRYPOINT ["poetry", "run"]
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "wsgi"]
