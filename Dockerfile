FROM python:3.9-slim

RUN useradd -m smol
WORKDIR /home/smol

RUN pip install -U pip poetry

COPY smol .
COPY pyproject.toml .

RUN poetry config virtualenvs.create false
RUN poetry install --no-dev

USER smol
ENTRYPOINT ["/usr/local/bin/python", "-m", "awslambdaric"]
CMD ["smol.api.alb_handler"]
