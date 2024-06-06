FROM public.ecr.aws/lambda/python:3.11

ENV POETRY_VERSION=1.7.1
WORKDIR ${LAMBDA_TASK_ROOT}

RUN curl -sSL https://install.python-poetry.org | python3 -

COPY smol ./smol
COPY pyproject.toml .
COPY poetry.lock .

RUN PATH="/root/.local/bin:$PATH" poetry build -f wheel
RUN cd dist && ls | grep .whl | xargs pip install && cd ..
RUN ls | xargs rm -rf

CMD ["smol.api.http_handler"]
