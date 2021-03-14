#!/bin/bash
set -eo pipefail

poetry install

poetry run black smol/
poetry run black tests/
poetry run black smol_cdk/

poetry run pylint smol/
poetry run pylint smol_cdk/

poetry run mypy smol/
poetry run mypy smol_cdk/

poetry run safety check

poetry run pytest
