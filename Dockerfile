FROM python:3.9-slim

RUN useradd -m smol
WORKDIR /home/smol

RUN pip install -U pip poetry

COPY smol .
COPY pyproject.toml .
COPY poetry.lock .

RUN poetry install --no-dev --no-interaction

USER smol
ENTRYPOINT ["poetry", "run", "python", "-m", "awslambdaric"]
CMD ["smol.api.alb_handler"]
