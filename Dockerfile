FROM python:3.9-slim

RUN useradd -m smol
WORKDIR /home/smol

RUN pip install -U pip poetry

COPY smol .
COPY pyproject.toml .
COPY poetry.lock .

USER smol
RUN poetry install --no-dev
ENTRYPOINT ["poetry", "run", "python", "-m", "awslambdaric"]
CMD ["smol.api.alb_handler"]
