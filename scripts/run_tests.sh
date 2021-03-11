#!/bin/bash
set -eo pipefail

pip install -U .

black smol/
black tests/

pylint smol/
mypy smol/

pytest
