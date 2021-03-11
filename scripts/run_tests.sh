#!/bin/bash
set -eo pipefail

export CAPTCHA_KEY="mock"

poetry install
poetry run black smol/
poetry run black tests/

poetry run pylint smol/
poetry run mypy smol/

poetry run pytest
