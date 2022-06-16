FROM ubuntu:22.04 AS base-all

RUN --mount=type=cache,target=/var/lib/apt/lists --mount=type=cache,target=/var/cache \
    apt-get update \
    && DEBIAN_FRONTEND=noninteractive apt-get install --yes --no-install-recommends python3-pip binutils

# Used to convert the locked packages by poetry to pip requirements format
# We don't directly use `poetry install` because it force to use a virtual environment.
FROM base-all as poetry

# Install poetry
WORKDIR /tmp
COPY requirements.txt ./
RUN --mount=type=cache,target=/root/.cache \
    python3 -m pip install --disable-pip-version-check --requirement=requirements.txt \
    && rm requirements.txt

# Do the conversion
COPY poetry.lock pyproject.toml ./
RUN poetry export --output=requirements.txt \
    && poetry export --dev --output=requirements-dev.txt

# Base, the biggest thing is to install the Python packages
FROM base-all as base

WORKDIR /app

RUN --mount=type=cache,target=/root/.cache \
    --mount=type=bind,from=poetry,source=/tmp,target=/poetry \
    python3 -m pip install --disable-pip-version-check --no-deps --requirement=/poetry/requirements.txt

FROM base AS checker

RUN --mount=type=cache,target=/root/.cache \
    --mount=type=bind,from=poetry,source=/tmp,target=/poetry \
    python3 -m pip install --disable-pip-version-check --no-deps --requirement=/poetry/requirements-dev.txt

FROM base AS run

SHELL ["/bin/bash", "-o", "pipefail", "-c"]

RUN --mount=type=cache,target=/var/lib/apt/lists --mount=type=cache,target=/var/cache \
    . /etc/os-release \
    && apt-get update \
    && apt-get --assume-yes upgrade \
    && apt-get install --assume-yes --no-install-recommends apt-transport-https gnupg curl \
    && echo "deb https://deb.nodesource.com/node_16.x ${VERSION_CODENAME} main" > /etc/apt/sources.list.d/nodesource.list \
    && curl --silent https://deb.nodesource.com/gpgkey/nodesource.gpg.key | apt-key add - \
    && apt-get update \
    && apt-get install --assume-yes --no-install-recommends nodejs

RUN python3 -m compileall -q -- *

COPY . ./
RUN --mount=type=cache,target=/root/.cache \
    cd c2cciutils && npm install && cd - \
    && sed --in-place 's/enable = true # disable on Docker/enable = false/g' pyproject.toml \
    && python3 -m pip install --disable-pip-version-check --no-deps --editable=. \
    && python3 -m compileall -q /app/c2cciutils
