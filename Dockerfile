FROM python:3.9-slim

RUN useradd -m smol
WORKDIR /home/smol

RUN pip install poetry

COPY smol ./smol
COPY pyproject.toml .
COPY poetry.lock .

RUN poetry build -f wheel
RUN cd dist && ls | grep .whl | xargs pip install && cd ..
RUN ls | xargs rm -rf

USER smol
ENTRYPOINT ["python", "-m", "awslambdaric"]
CMD ["smol.api.alb_handler"]
