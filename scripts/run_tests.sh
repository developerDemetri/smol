#!/bin/bash
set -eo pipefail

poetry install --sync

poetry run ruff format

poetry run ruff check --fix

poetry run mypy smol/

poetry run pytest
